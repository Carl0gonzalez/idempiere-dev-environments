# Entorno aislado de iDempiere 12

[English version](README.md) · [Volver a la guía general](../README.es.md)

Configuración de desarrollo local basada en `direnv` para la rama `release-12`. Aísla Java 17, Maven 3.9.11, dependencias, P2, Eclipse, workspace y fuentes.

## Resumen técnico

| Componente | Configuración |
|---|---|
| Rama | `release-12` |
| Revisión esperada | `12.0.0` |
| Java | JDK 17 |
| Maven | distribución local `apache-maven-3.9.11/` |
| Fuentes | `sources/idempiere/` |
| Workspace | `workspace-12/` |
| Repositorio Maven | `.m2/repository/` |
| Configuración P2 | `.p2/configuration/` |
| Repositorio Git | oficial de iDempiere |

## Preparación

Instale `direnv`, Git y un JDK 17, y active el hook de `direnv`. Dentro de este directorio:

1. Descomprima Maven 3.9.11 en `apache-maven-3.9.11/`.
2. Instale Eclipse como `eclipse/eclipse` en Linux o `eclipse/Eclipse.app` en macOS.
3. Autorice y compruebe el entorno.

```sh
cd iDempiere12
direnv allow
idempiere-doctor
```

`direnv allow` crea la estructura local, genera `.m2/settings.xml` si falta y reconstruye `.local-bin`. No instala componentes ni clona el proyecto.

## Clonar y construir

```sh
idempiere-clone
mvn12 clean verify
```

El asistente clona `release-12` desde el repositorio oficial en `sources/idempiere`. Conserva un clon existente y se niega a escribir sobre un destino ocupado por otros archivos.

`mvn12` usa siempre `apache-maven-3.9.11/bin/mvn`, el `settings.xml` y el repositorio Maven de este entorno. Java se ejecuta en modo headless sólo durante Maven.

El entorno administra una sola copia de `-Drevision=12.0.0` en `MAVEN_OPTS`: primero elimina las copias previas y luego añade una, manteniendo intactas las demás opciones heredadas. La ubicación del repositorio también se pasa directamente en cada invocación de `mvn12`.

## Eclipse

```sh
eclipse-start
```

El comando fija Java 17, `workspace-12` y `.p2/configuration`. `GDK_BACKEND=x11` se aplica sólo en Linux; macOS usa el ejecutable nativo de `Eclipse.app`.

```sh
eclipse-choose
eclipse-here
```

`eclipse-choose` muestra el selector y propone el workspace aislado. `eclipse-here` es un alias de compatibilidad que delega en `eclipse-start`; no cambia el workspace según el directorio actual.

## Comandos disponibles

| Comando | Acción y condiciones |
|---|---|
| `mvn12 [argumentos]` | Ejecuta Maven 3.9.11 con Java y repositorio aislados. |
| `eclipse-start` | Abre Eclipse con el workspace fijo. |
| `eclipse-here` | Alias compatible de `eclipse-start`. |
| `eclipse-choose` | Abre Eclipse con selector de workspace. |
| `idempiere-root` | Abre una shell nueva en las fuentes; requiere el clon. |
| `idempiere-clone` | Clona por red la rama oficial, sin sobrescribir contenido. |
| `idempiere-fix-maven-config` | Regenera `.mvn/maven.config` con un argumento por línea. |
| `idempiere-doctor` | Valida el entorno y devuelve estado no cero ante fallos. |

El formato de `maven.config` generado es compatible con Maven 3.9: la opción `-s`, su valor y `-Dmaven.repo.local=...` se escriben como argumentos separados. El comando modifica ese archivo dentro del clon.

## Diagnóstico y mantenimiento

```sh
idempiere-doctor
```

El doctor revisa Java 17, Maven 3.9.11, `settings.xml`, repositorio local, Eclipse, Git, `curl`, wrappers, rama, `.mvn`, plataforma objetivo, revisión y otros metadatos observables en el POM. El análisis del POM es estático.

Tras cambiar `.envrc`, autorícelo otra vez. Los wrappers son regenerables: cualquier corrección permanente debe hacerse en `.envrc`.

El `.gitignore` excluye `.local-bin`, `.m2`, `.p2`, Maven, Eclipse, fuentes, `workspace-12` y el antiguo `workspace/`.

En macOS, `.envrc` selecciona JDK 17 mediante `/usr/libexec/java_home -v 17`. Ejecute `/usr/libexec/java_home -V` si el JDK no se detecta.

## Límites

- El asistente usa el repositorio oficial y no configura automáticamente un fork o `upstream`.
- Maven y Eclipse se aportan manualmente.
- La primera resolución de dependencias requiere red.
- La fuente de verdad es [`.envrc`](.envrc).
