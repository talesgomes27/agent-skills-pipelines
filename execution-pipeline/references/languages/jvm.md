# JVM (Java e Kotlin)

Leia quando o componente da tarefa roda na JVM e usa Maven ou Gradle.

## Descubra no projeto

- Versão do JDK: `maven.compiler.release` no `pom.xml`, ou `java { toolchain { languageVersion = ... } }` no `build.gradle(.kts)`.
- Dependências e build: `pom.xml`, `build.gradle(.kts)`, `settings.gradle(.kts)` e o workflow de CI.
- Wrapper: `mvnw` com `.mvn/wrapper/maven-wrapper.properties`, ou `gradlew` com `gradle/wrapper/gradle-wrapper.properties`. O wrapper baixa a versão do build que o projeto fixou, e as dependências vão para o cache do usuário (`~/.m2` ou `~/.gradle`). O `pom.xml` não é lock: plugins e dependências transitivas não têm hash. Por isso baixar a distribuição do Maven ou do Gradle, as dependências ou um JDK é instalar, um efeito do catálogo do contrato comum, e pede A2 com a versão e o cache. Dispensa o A2 só o que já está na máquina e, como instalar do lock aceito, as dependências listadas na verificação de dependências do Gradle (`gradle/verification-metadata.xml`) que o projeto fixa em modo estrito e o usuário já aceitou; modo `lenient` ou artefato confiável sem checksum não contam. O `distributionSha256Sum` do wrapper só confere o arquivo de um download já aceito e não dispensa o A2 da distribuição. O `-o` e o `--offline` valem para o build, não para o download que o wrapper faz antes dele. Antes do primeiro `./mvnw`, confira se a versão do `maven-wrapper.properties` já está em `~/.m2/wrapper/dists` (ou no `MAVEN_USER_HOME`); antes do primeiro `./gradlew`, confira se a versão do `gradle-wrapper.properties` já está em `~/.gradle/wrapper/dists` (ou no `GRADLE_USER_HOME`, ou no `distributionPath` do arquivo). Se não estiver, peça A2. Depois, rode o Maven com `-o` e o Gradle com `--offline` (sem ele só para baixar as dependências da verificação estrita) e `-Dorg.gradle.java.installations.auto-download=false`, para não buscar dependência nova nem baixar um JDK das toolchains para `~/.gradle/jdks`; JDK que falta pede A2. Mudar a versão fixada ou acrescentar dependência também pede A2.

Use o wrapper e o JDK que o projeto pede. Não instale Maven, Gradle ou JDK global.

## Testes e checks

Exemplos a confirmar no projeto:

- Maven: `./mvnw test`, que roda o Surefire na fase `test`; uma classe com `./mvnw -Dtest=MinhaClasseTest test`.
- Gradle: `./gradlew test` e `./gradlew test --tests MinhaClasseTest`; `./gradlew check` inclui o `test`.
- JUnit: testes Jupiter no Gradle exigem `useJUnitPlatform()` na tarefa `test`. Confira no relatório quantos testes rodaram, não só se o build passou.

## Armadilhas

- JDK diferente do projeto: compilar ou testar com outro JDK muda API disponível e comportamento. Use a versão declarada no build.
- Fuso padrão: `TimeZone.getDefault()` vem de `user.timezone` ou do sistema. Código que depende dele muda de resultado entre a máquina, o CI e o servidor. Passe o fuso explícito.
- Locale padrão: a JVM o define pelo ambiente na inicialização, e formatação de número e data muda com ele. Passe o `Locale` explícito, como `Locale.ROOT`, em saída lida por máquina.
- `BigDecimal` para dinheiro, criado de texto ou com `BigDecimal.valueOf`: `new BigDecimal(0.1)` vale 0.1000000000000000055511151231257827021181583404541015625.
- Arredondamento de `BigDecimal` explícito, como `setScale(2, RoundingMode.HALF_UP)` para meio para cima: `setScale(2)` sem o modo lança `ArithmeticException` quando precisa arredondar.
- `equals` em `BigDecimal` compara também a escala: `2.0` e `2.00` são diferentes por `equals` e iguais por `compareTo`.

## Fontes

Conferido em 08/11/2026:

- https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/math/BigDecimal.html
- https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Locale.html
- https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/TimeZone.html
- https://maven.apache.org/wrapper/
- https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-release.html
- https://maven.apache.org/surefire/maven-surefire-plugin/examples/single-test.html
- https://docs.gradle.org/current/userguide/gradle_wrapper.html
- https://docs.gradle.org/current/userguide/toolchains.html
- https://docs.gradle.org/current/userguide/dependency_verification.html
- https://docs.gradle.org/current/userguide/java_testing.html
- https://docs.junit.org/current/user-guide/
