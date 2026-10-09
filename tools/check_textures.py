#!/usr/bin/env python3
"""Revisa que cada ítem y bloque de mods tenga modelo y texturas (lo que en el juego sale morado y negro).

Uso: python3 tools/check_textures.py <instancia-cliente> <vanilla-client.jar> <items.txt> <blocks.txt> > problemas.tsv
  - instancia-cliente: carpeta con mods/, resourcepacks/ y config/openloader/resources/ (ops/sync.sh client <carpeta>)
  - items.txt / blocks.txt: un id por línea, del registro real del server (scarpet item_list()/block_list())
Salida TSV: id, tipo (item|block), problema, detalle. Sin modelo propio en el jar no implica error: hay mods
que generan modelos en runtime o usan renderers propios (builtin/entity); eso lo marca como INFO_*.
"""
import io, json, sys, zipfile
from pathlib import Path

assets = {}  # "assets/ns/..." -> bytes (último gana; resource packs al final)
atlas_files = []  # los atlas se fusionan entre packs, no se pisan


def load_zip(zf):
    for n in zf.namelist():
        if n.startswith("META-INF/jars/") and n.endswith(".jar"):
            load_zip(zipfile.ZipFile(io.BytesIO(zf.read(n))))
        elif n.startswith("assets/") and not n.endswith("/"):
            assets[n] = zf.read(n) if n.endswith(".json") else b""
            if n.endswith("/atlases/blocks.json"):
                atlas_files.append(assets[n])


def jread(path):
    try:
        # raw_decode: como Gson, el juego ignora lo que venga después del objeto raíz
        return json.JSONDecoder().raw_decode(assets[path].decode("utf-8-sig").strip())[0]
    except Exception:
        return None


def rl(s, default_ns="minecraft"):
    ns, _, p = s.partition(":") if ":" in s else (default_ns, "", s)
    return ns, p


def atlas_dirs():
    dirs, singles = set(), set()
    for raw in atlas_files:
        try:
            sources = json.loads(raw.decode("utf-8-sig")).get("sources", [])
        except Exception:
            continue
        for src in sources:
            t = src.get("type", "").removeprefix("minecraft:")
            if t == "directory":
                dirs.add(src["source"].rstrip("/") + "/")
            elif t == "single":
                singles.add(rl(src["resource"]))
            elif t == "paletted_permutations":  # p. ej. recortes de armadura: se generan en runtime
                for tex in src.get("textures", []):
                    singles.update(rl(f"{tex}_{k}") for k in src.get("permutations", {}))
    return dirs, singles


def check_model(model_id, out, seen=None):
    """Resuelve padres y texturas; agrega (problema, detalle) a out. Devuelve el modelo combinado o None."""
    seen = seen or set()
    ns, p = rl(model_id)
    textures, elements, chain, cur = {}, None, [], (ns, p)
    while cur:
        if cur in seen:
            break
        seen.add(cur)
        key = f"{cur[0]}:{cur[1]}"
        chain.append(key)
        if cur[1].startswith("builtin/"):
            if cur[1] == "builtin/entity":
                out.append(("INFO_BUILTIN_ENTITY", key))
            break
        m = jread(f"assets/{cur[0]}/models/{cur[1]}.json")
        if m is None:
            out.append(("MISSING_MODEL", key + (f" (padre de {chain[-2]})" if len(chain) > 1 else "")))
            return None
        if "loader" in m or any(k.startswith("fabric") for k in m):
            out.append(("INFO_CUSTOM_LOADER", key))
            return None
        textures = {**m.get("textures", {}), **textures}
        if elements is None and "elements" in m:
            elements = m["elements"]
        cur = rl(m["parent"]) if "parent" in m else None

    def resolve(v, depth=0):
        while v.startswith("#") and depth < 20:
            v, depth = textures.get(v[1:], ""), depth + 1
        return v

    # tamaño de la cara según su dirección; las de área cero no se dibujan
    AXES = {"north": (0, 1), "south": (0, 1), "east": (2, 1), "west": (2, 1), "up": (0, 2), "down": (0, 2)}

    used = {k: v for k, v in textures.items()}
    for el in elements or []:
        size = [abs(b - a) for a, b in zip(el.get("from", [0] * 3), el.get("to", [1] * 3))]
        for d, f in el.get("faces", {}).items():
            a, b = AXES.get(d, (0, 1))
            if "texture" in f and size[a] and size[b]:
                t = f["texture"]  # en caras, "side" sin "#" igual es una variable
                used.setdefault("face:" + t, t if t.startswith("#") else "#" + t)
    if "builtin/generated" in str(chain[-1]) and not any(k.startswith("layer") for k in textures):
        out.append(("MISSING_TEXTURE", f"{model_id}: generado sin layer0"))
    for k, v in used.items():
        r = resolve(v)
        if not r:
            out.append(("MISSING_TEXTURE", f"{model_id}: #{k} -> {v} sin definir"))
            continue
        tns, tp = rl(r)
        if f"assets/{tns}/textures/{tp}.png" not in assets and (tns, tp) not in ATLAS[1]:
            out.append(("MISSING_TEXTURE", f"{model_id}: {tns}:{tp}"))
        elif not any(tp.startswith(d) for d in ATLAS[0]) and (tns, tp) not in ATLAS[1]:
            out.append(("NOT_IN_ATLAS", f"{model_id}: {tns}:{tp}"))
    return True


def blockstate_models(bs):
    def models(v):
        for x in v if isinstance(v, list) else [v]:
            if isinstance(x, dict) and "model" in x:
                yield x["model"]
    for v in (bs.get("variants") or {}).values():
        yield from models(v)
    for part in bs.get("multipart") or []:
        yield from models(part.get("apply", {}))


def main():
    inst, vanilla, items_f, blocks_f = sys.argv[1:5]
    load_zip(zipfile.ZipFile(vanilla))
    for j in sorted(Path(inst, "mods").glob("*.jar")):
        load_zip(zipfile.ZipFile(j))
    for rp in sorted(Path(inst, "resourcepacks").glob("*.zip")) + sorted(Path(inst, "config/openloader/resources").glob("*")):
        if rp.is_dir():  # OpenLoader acepta carpetas sueltas
            for f in rp.rglob("*"):
                n = f.relative_to(rp).as_posix()
                if n.startswith("assets/") and f.is_file():
                    assets[n] = f.read_bytes() if n.endswith(".json") else b""
        elif rp.suffix == ".zip":
            load_zip(zipfile.ZipFile(rp))
    global ATLAS
    ATLAS = atlas_dirs()
    w = sys.stdout.write
    w("id\ttipo\tproblema\tdetalle\n")
    for line in Path(blocks_f).read_text().split():
        ns, p = rl(line)
        bs = jread(f"assets/{ns}/blockstates/{p}.json")
        if bs is None:
            w(f"{line}\tblock\tMISSING_BLOCKSTATE\tassets/{ns}/blockstates/{p}.json\n")
            continue
        out = []
        for m in sorted(set(blockstate_models(bs))):
            check_model(m if ":" in m else f"minecraft:{m}", out)
        for prob, det in dict.fromkeys(out):
            w(f"{line}\tblock\t{prob}\t{det}\n")
    for line in Path(items_f).read_text().split():
        ns, p = rl(line)
        out = []
        if f"assets/{ns}/models/item/{p}.json" not in assets:
            out.append(("MISSING_ITEM_MODEL", f"assets/{ns}/models/item/{p}.json"))
        else:
            check_model(f"{ns}:item/{p}", out)
            for o in (jread(f"assets/{ns}/models/item/{p}.json") or {}).get("overrides", []):
                if "model" in o:
                    check_model(o["model"] if ":" in o["model"] else f"minecraft:{o['model']}", out)
        for prob, det in dict.fromkeys(out):
            w(f"{line}\titem\t{prob}\t{det}\n")


if __name__ == "__main__":
    main()
