# Define $JAVA apuntando a Java 21. Se usa con: . ops/java.sh
if [ -x /opt/homebrew/opt/openjdk@21/bin/java ]; then JAVA=/opt/homebrew/opt/openjdk@21/bin/java
elif [ -x /usr/lib/jvm/java-21-amazon-corretto/bin/java ]; then JAVA=/usr/lib/jvm/java-21-amazon-corretto/bin/java
elif [ -x /usr/lib/jvm/java-21-openjdk-amd64/bin/java ]; then JAVA=/usr/lib/jvm/java-21-openjdk-amd64/bin/java
elif [ -x /usr/lib/jvm/java-21-openjdk-arm64/bin/java ]; then JAVA=/usr/lib/jvm/java-21-openjdk-arm64/bin/java
else JAVA=java
fi
