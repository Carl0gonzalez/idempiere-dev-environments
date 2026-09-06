# Entorno aislado de iDempiere 10

[English version](README.md) · [Volver a la guía general](../README.es.md)

Configuración de desarrollo local basada en `direnv` para la rama `release-10`. Mantiene separados Java 11, Maven 3.6.3, dependencias, P2, Eclipse, workspace y fuentes.

## Resumen técnico

| Componente | Configuración |
|---|---|
| Rama | `release-10` |
| Java | JDK 11 |
| Maven | distribución local `apache-maven-3.6.3/` |
| Fuentes | `sources/idempiere/` |
| Workspace | `workspace-10/` |
| Repositorio Maven | `.m2/repository/` |
| Configuración P2 | `.p2/configuration/` |
| Repositorio Git | oficial de iDempiere |

## Preparación

Instale `direnv`, Git y un JDK 11, y active el hook de `direnv` en su shell. Luego:

1. Descomprima Maven 3.6.3 en `apache-maven-3.6.3/`.
2. Instale Eclipse como `eclipse/eclipse` en Linux o `eclipse/Eclipse.app` en macOS.
3. Autorice y compruebe el entorno.

```sh
cd iDempiere10
direnv allow
idempiere-doctor
```

La carga crea la estructura aislada, genera `.m2/settings.xml` cuando falta y reconstruye los comandos de `.local-bin`. No descarga Maven, Eclipse ni las fuentes.

## Clonar y construir

```sh
idempiere-clone
mvn10 clean verify
```

El clon se obtiene de la rama oficial `release-10` y queda en `sources/idempiere`. El asistente se niega a clonar sobre un directorio no vacío y no elimina contenido local.

`mvn10` ejecuta el Maven local indicado, usa el JDK seleccionado, activa el modo headless únicamente para Maven y fuerza `.m2/settings.xml` y `.m2/repository` como configuración aislada.

La opción `-Dmaven.repo.local=...` administrada por el entorno se elimina antes de volver a añadirse. De ese modo, `MAVEN_OPTS` conserva opciones ajenas sin acumular duplicados en cada recarga.

## Eclipse

```sh
eclipse-start
```

Eclipse se abre con Java 11, `workspace-10` y `.p2/configuration`. `GDK_BACKEND=x11` se aplica sólo en Linux; macOS usa el ejecutable nativo de `Eclipse.app`. Para mostrar el selector de workspace:

```sh
eclipse-choose
```

El segundo comando propone el workspace aislado como valor predeterminado, pero permite escoger otro.

## Comandos disponibles

| Comando | Acción y condiciones |
|---|---|
| `mvn10 [argumentos]` | Ejecuta Maven 3.6.3 con configuración aislada; falla si no está instalado. |
| `eclipse-start` | Abre Eclipse con el workspace fijo. |
| `eclipse-choose` | Abre Eclipse con selector de workspace. |
| `idempiere-root` | Abre una shell nueva en las fuentes; requiere el clon. |
| `idempiere-clone` | Clona por red la rama oficial sin sobrescribir un destino no vacío. |
| `idempiere-fix-maven-config` | Regenera `sources/idempiere/.mvn/maven.config`. |
| `idempiere-doctor` | Inspecciona el entorno y devuelve estado no cero si encuentra fallos. |

La reparación de `maven.config` es una escritura deliberada dentro del clon y fija tanto el archivo de configuración como el repositorio Maven de este entorno.

## Diagnóstico y mantenimiento

```sh
idempiere-doctor
```

El diagnóstico revisa Java, Maven, `settings.xml`, repositorio local, Eclipse, Git, `curl`, wrappers, rama, archivos `.mvn`, plataforma objetivo y metadatos del POM. La lectura del POM es estática y no reemplaza una construcción real.

Después de editar `.envrc`, ejecute `direnv allow`. Los wrappers de `.local-bin` se regeneran con cada carga y no deben editarse como fuente.

El `.gitignore` excluye `.local-bin`, `.m2`, `.p2`, la distribución Maven, Eclipse, las fuentes y `workspace-10`.

En macOS, `.envrc` selecciona JDK 11 mediante `/usr/libexec/java_home -v 11`. Ejecute `/usr/libexec/java_home -V` si el JDK no se detecta.

## Límites

- `idempiere-clone` trabaja con el repositorio oficial; esta versión no automatiza el modelo fork/upstream.
- Maven y Eclipse deben instalarse manualmente en sus rutas locales.
- Resolver dependencias ausentes requiere red.
- La fuente de verdad es [`.envrc`](.envrc).
