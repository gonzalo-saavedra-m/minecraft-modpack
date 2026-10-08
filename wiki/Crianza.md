[← Wiki](README.md)

# Crianza

La crianza la agrega el mod **Cobbreeding 2.4.0**. Guía oficial (en inglés):
[Cobbreeding guide](https://docs.google.com/document/d/1Hk5Iqnzm2NqkXGwzUIvPVFKhAwVHSEM3hyP3Qdhl5g4/edit?usp=sharing)
· [Modrinth](https://modrinth.com/mod/cobbreeding).

Las reglas son casi las mismas que en los juegos principales (Escarlata/Púrpura). Esta página explica cómo
funciona en este server y lo que cambia.

## Cómo criar

1. **Pon un Corral** (Pasture Block de Cobblemon). Los Pokémon aparecen detrás del bloque: deja espacio libre y
   que la zona sea segura (sin agua profunda ni lava; pueden debilitarse).
2. **Activa la crianza**: clic derecho al corral y pulsa el botón de arriba a la derecha ("Toggle breeding").
   Viene apagado por defecto.
3. **Mete dos Pokémon compatibles** (ver tabla abajo).
4. **Espera.** Sale un huevo cada **8000 a 14000 ticks (≈ 7 a 12 minutos)** mientras el chunk esté cargado. Si te
   vas y vuelves, el corral calcula el tiempo pasado y genera los huevos que correspondan, hasta llenarse.
5. **Recoge el huevo**: aparece en la parte de abajo del corral; clic derecho para sacarlo. Caben **5 huevos**;
   con el corral lleno no salen más. Una tolva debajo los saca sola.

### Quién puede criar con quién

| Pareja | ¿Cría? | Qué nace |
|---|---|---|
| Macho + hembra que comparten al menos un grupo huevo | Sí | La especie base de la madre |
| Cualquiera (macho, hembra o sin género) + Ditto | Sí | La especie base del que no es Ditto |
| Pokémon sin género sin Ditto | No | — |
| Ditto + Ditto | **No** (desactivado en este server) | — |
| Grupo huevo **Desconocido** (legendarios, singulares, bebés, etc.) | **No**, ni siquiera con Ditto | — |

- Especies con dos líneas (Nidoran♀/♂, Volbeat/Illumise) pueden dar cualquiera de las dos.
- Manaphy + Ditto da un huevo de **Phione**.
- Los Pokémon del corral pueden ser de **distintos jugadores**.
- En el resumen de cada Pokémon hay un botón para marcarlo como **no criable** (solo lo puede usar su
  Entrenador Original).

## Eclosión

- El huevo se eclosiona **llevándolo en el inventario**: tiene un contador que solo avanza mientras está en el
  inventario de un jugador (en un cofre se detiene).
- Duración: **ciclos huevo de la especie × 30 segundos**. Una especie de 20 ciclos tarda ≈ 10 minutos. En este
  server `eggHatchMultiplier` es **1.0** (velocidad normal).
- Tener en el equipo un Pokémon con **Cuerpo Llama, Escudo Magma o Combustible** (Flame Body, Magma Armor, Steam
  Engine) **reduce el tiempo a la mitad**.
- Al llegar a 0 el Pokémon sale y entra a tu equipo. Si el contador del cliente marca 0 y no pasa nada, espera:
  manda el reloj del server.
- El contenido del huevo está cifrado: no se puede ver qué hay dentro antes de que nazca. Todo (especie, IVs,
  shiny…) se decide **cuando se crea el huevo**, no al eclosionar.

## Qué se hereda

| Qué | Cómo |
|---|---|
| **IVs** | 3 IVs al azar de los padres (cada uno, de cualquiera de los dos). Con **Lazo Destino** (Destiny Knot) en cualquiera de los padres: **5**. Con un **objeto Recio** (Power Weight, Bracer, Belt, Lens, Band, Anklet), ese IV se hereda seguro del padre que lo lleva. |
| **Naturaleza** | Al azar. Si un padre lleva **Piedra Eterna** (Everstone), pasa la suya; si ambos la llevan, la de uno al azar. |
| **Habilidad** | 80 % de mantener la habilidad (el "slot") de la madre si es normal; 60 % si es su habilidad oculta. El resto se reparte entre las demás habilidades. Con Ditto cuenta el otro padre. |
| **Habilidad oculta** | Activada (`hiddenAbilitiesEnabled`): puede salir **aunque la madre no la tenga**: ≈ 10 % si la especie tiene 3 habilidades, ≈ 20 % si tiene 2. |
| **Movimientos huevo** | Todos los que conozcan los padres, **incluidos los movimientos guardados** (no hace falta tenerlos equipados). Si uno no pasa, muévelo a los guardados. Pichu con Bola Luz en un padre aprende Placaje Eléctrico. |
| **Hierba Copia** (Mirror Herb) | Si un Pokémon del corral la lleva, aprende los movimientos huevo de su compañero (no necesitan compartir grupo huevo). Se revisa cada vez que el corral intenta generar un huevo (`mirrorHerbTimeInTicks` = 600, 30 s). |
| **Poké Ball** | La de la madre (o la del que no es Ditto). Si ambos son de la misma especie, la de cualquiera. Master Ball y Gloria Ball pasan como Poké Ball normal. |
| **Forma regional y variantes** | Se heredan **directamente de la madre**, sin Piedra Eterna: Alola, Galar, Hisui, Paldea, sesgo regional, patrones de Magikarp, estilo de Oricorio, color, rayas, Mooshtank, Tauros de Paldea, Tatsugiri, Wooper, etc. Algunas formas no se heredan (Rotom sale normal, Flabébé con flor al azar). |
| **Alfa** | 5 % de que nazca **Alfa** (`alphaChances` 0.05). No se hereda de la madre (`inheritAlpha` desactivado). |

## Shinies: Método Masuda

En Cobbreeding el Masuda **no depende del idioma del juego**. Se activa cuando **los dos padres tienen distinto
Entrenador Original (EO/OT)**: el jugador que capturó al Pokémon. Si un Pokémon no tiene EO registrado, se usa su
dueño actual. Intercambiar un Pokémon **no** le cambia el EO.

| | Probabilidad shiny por huevo |
|---|---|
| Base (Cobblemon, `shinyRate` 8192) | 1 / 8192 |
| **Masuda (padres de distinto EO, ×4)** | **1 / 2048** |

**En la práctica, entre amigos:** pídele a un amigo un Pokémon que **él haya capturado** (o que lo meta él mismo
en tu corral) y crúzalo con uno tuyo. Cada huevo de esa pareja tiene **4 veces más** probabilidad de ser shiny.
Si los dos padres los capturaste tú, no hay bonus. Un Ditto capturado por otro jugador sirve para cualquier
especie.

### Método Cristal (desactivado)

Multiplica la probabilidad shiny **por cada padre shiny** (dos padres shiny = se aplica dos veces). En este server
está en **×1.0**, o sea **apagado**: que los padres sean shiny no ayuda. Los multiplicadores se combinan
multiplicándose, así que si algún día se activa se sumaría al Masuda.

## Recetas con huevos

Cobbreeding no agrega bloques ni objetos aparte del **Huevo Pokémon**. Ojo: los Huevos Pokémon entran en la
etiqueta `c:eggs`, igual que el huevo de gallina, así que las recetas de **torta** y **pastel de calabaza**
aceptan un Huevo Pokémon. **No cocines tus huevos por error**: usa huevos de gallina.
