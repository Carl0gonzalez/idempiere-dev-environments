# Entorno aislado de iDempiere 8.2

[English version](README.md) · [Volver a la guía general](../README.es.md)

Configuración de desarrollo local basada en `direnv` para la rama `release-8.2`. Aísla Java 11, Maven 3.6.3, el repositorio Maven, P2, Eclipse, el workspace y las fuentes del resto de versiones.

## Resumen técnico

| Componente | Configuración |
|---|---|
| Rama | `release-8.2` |
| Java | JDK 11 |
| Maven | distribución local `apache-maven-3.6.3/` |
| Fuentes | `sources/idempiere/` |
| Workspace | `workspace-8.2/` |
| Repositorio Maven | `.m2/repository/` |
| Configuración P2 | `.p2/configuration/` |
| Repositorio Git | oficial de iDempiere |

## Preparación

Instale `direnv`, Git y un JDK 11. Integre `direnv` con su shell. Después, dentro de este directorio:

1. Descomprima Maven 3.6.3 en `apache-maven-3.6.3/`.
2. Instale Eclipse en `eclipse/`, con el ejecutable en `eclipse/eclipse`.
3. Autorice el entorno y ejecute el diagnóstico.

```sh
cd iDempiere8.2
direnv allow
idempiere-doctor
```

La carga crea los directorios locales, genera `.m2/settings.xml` si falta y reconstruye los wrappers de `.local-bin`. No instala software ni clona las fuentes.

## Clonar y construir

```sh
idempiere-clone
mvn82 clean verify
```

`idempiere-clone` clona la rama `release-8.2` desde el repositorio oficial en `sources/idempiere`. Si el destino ya contiene un repositorio o un `pom.xml`, lo conserva; si contiene otros archivos, termina sin sobrescribirlos.

`mvn82` ejecuta exclusivamente `apache-maven-3.6.3/bin/mvn`, fuerza Java en modo headless para Maven y pasa siempre el `settings.xml` y el repositorio local aislados.

El `.envrc` conserva las opciones Maven heredadas y administra una sola copia de `-Dmaven.repo.local=...`; las recargas no deben acumular esa opción.

## Eclipse

```sh
eclipse-start
```

Este comando fija Java 11, `workspace-8.2`, `.p2/configuration` y `GDK_BACKEND=x11`. Para elegir otro workspace sin perder el predeterminado aislado:

```sh
eclipse-choose
```

Tras disponer de las fuentes, el entorno también prepara en el workspace el enlace de compatibilidad para `org.adempiere.server-feature/utils.unix` cuando su destino existe en el clon.

## Comandos disponibles

| Comando | Acción y condiciones |
|---|---|
| `mvn82 [argumentos]` | Ejecuta el Maven local aislado; falla si no está instalado. |
| `eclipse-start` | Abre Eclipse con el workspace fijo del entorno. |
| `eclipse-choose` | Abre el selector de workspace y propone `workspace-8.2`. |
| `idempiere-root` | Abre una shell nueva en `sources/idempiere`; requiere las fuentes. |
| `idempiere-clone` | Clona por red la rama oficial prevista, sin sobrescribir un destino no vacío. |
| `idempiere-fix-maven-config` | Regenera `.mvn/maven.config` dentro del clon con las rutas Maven aisladas. |
| `idempiere-doctor` | Verifica el entorno y devuelve estado no cero si hay fallos. |

`idempiere-fix-maven-config` modifica un archivo dentro del clon. Úselo si la configuración Maven del proyecto fue eliminada o dejó de apuntar al entorno local.

## Diagnóstico y mantenimiento

```sh
idempiere-doctor
```

El doctor comprueba, entre otros puntos, Java, Maven, `settings.xml`, repositorio local, Eclipse, Git, `curl`, wrappers, rama, configuración `.mvn`, plataforma objetivo y metadatos disponibles en el POM. Las comprobaciones del POM son estáticas; no ejecutan una construcción para deducirlos.

Si cambia `.envrc`, ejecute otra vez `direnv allow`. Si modifica manualmente un wrapper generado, la siguiente recarga lo reemplazará: haga la corrección en `.envrc`.

Los directorios `.local-bin`, `.m2`, `.p2`, `apache-maven-3.6.3`, `eclipse`, `sources` y `workspace-8.2` están excluidos por el `.gitignore` de este entorno.

## Límites

- El asistente Git de esta versión sólo configura el repositorio oficial; no gestiona automáticamente un fork ni un remoto `upstream`.
- Eclipse y Maven deben suministrarse localmente.
- La primera construcción necesita red para resolver dependencias que aún no estén en `.m2/repository`.
- La fuente de verdad es [`.envrc`](.envrc).
