# Entorno aislado de iDempiere 8.2

[English version](README.md) · [Guía general](../README.es.md)

## Requisitos y estructura

Linux o macOS, Bash, Git, direnv integrado con su shell y el JDK correspondiente. Maven y Eclipse se aportan manualmente donde se indica. La red y las credenciales se necesitan sólo al clonar, descargar o publicar.

```text
iDempiere8.2/
├── .envrc
├── .m2/settings.xml
├── .m2/repository/
├── .local-bin/
├── .local-share/man/
├── .p2/configuration/
├── eclipse/
├── sources/idempiere/
├── workspace-8.2/
└── .idempiere-git.env
```

## Funcionalidades actualizadas (2026-10-06)

La base es `release-8.2`, con JDK 11 y Maven local 3.6.3. Se conservan los requisitos propios de esta versión.

- Ayuda común: `idempiere-help`, `idempiere-help mvn82` y `<comando> help`, `--help`, `-h` o `--man`.
- Mensajes y ayuda según `LC_ALL`, después `LC_MESSAGES` y finalmente `LANG`: español para `es`, inglés para los demás idiomas. La selección de JDK y algunos errores de configuración conservan mensajes en español.
- Manuales locales ES/EN en `.local-share/man/`; `MANPATH` elige el idioma durante la carga. Requiere el programa `man`. Cambiar el locale exige `direnv reload` para actualizar esa selección.
- Compatibilidad Linux y macOS. Eclipse: `eclipse/eclipse` o `eclipse/Eclipse.app/Contents/MacOS/eclipse`.
- JDK configurable mediante `IDEMPIERE_JAVA_HOME_OVERRIDE` (también acepta `IDEMPIERE_JAVA_HOME`); se comprueba `javac` de la versión requerida.
- Recargas sin añadir opciones a `MAVEN_OPTS`. Maven recibe settings y repositorio local como argumentos citados.

### Primera carga y fuentes

```sh
cd iDempiere8.2
direnv allow
idempiere-help
idempiere-clone
direnv reload
idempiere-git-check
mvn82 verify
eclipse-start
```

`direnv allow` crea directorios, settings, wrappers y manuales; no instala herramientas ni clona. Instale Maven en `apache-maven-3.6.3/` antes del build. Instale Eclipse en `eclipse/`. Estas configuraciones preparan el entorno; no acreditan un build ni un arranque de iDempiere.

### Git oficial y fork

Todas las versiones permiten elegir repositorio oficial o fork al clonar. En modo `official`, `origin` es `https://github.com/idempiere/idempiere.git` y no hay `upstream`. En modo `fork`, `origin` es el fork y `upstream` es el oficial.

La configuración se lee como datos, sin ejecutar código, desde `.idempiere-git.env`; se escribe de forma atómica con permisos `600`. Es privada y se ignora en Git. Un clon existente requiere una configuración coherente y sólo se valida. Para un clon oficial anterior sin este archivo puede crear:

```dotenv
IDEMPIERE_GIT_MODE=official
IDEMPIERE_ORIGIN_URL=https://github.com/idempiere/idempiere.git
IDEMPIERE_UPSTREAM_URL=
```

Recargue y compruebe los remotos; el asistente no los corrige automáticamente. El destino no vacío se rechaza.

| Comando | Comportamiento |
|---|---|
| `idempiere-help [comando]` | Lista comandos o explica uno, sin ejecutarlo. |
| `mvn82 [argumentos]` | Build aislado; puede descargar dependencias. |
| `eclipse-start` / `eclipse-choose` | Workspace fijo o selector, con JDK y P2 locales. |
| `idempiere-root` | Abre otra shell en las fuentes; `exit` vuelve a la anterior. |
| `idempiere-clone` | Asistente oficial/fork para `release-8.2`; usa red y guarda configuración. |
| `idempiere-remotes` | Muestra remotos reales sin modificarlos. |
| `idempiere-git-check` | Falla si clon, modo o remotos no coinciden. |
| `idempiere-sync-upstream` | Exige `release-8.2` y árbol limpio; fetch/fast-forward local. No hace push. |
| `idempiere-new-feature <rama>` | Valida nombre y existencia, actualiza la base y crea desde la referencia remota; sin push. |
| `idempiere-doctor [--network]` | Diagnóstico local; devuelve error por fallos. SSH sólo con `--network`. |

También conserva `idempiere-fix-maven-config`, que modifica `.mvn/maven.config` del clon; revise su diff antes de conservarlo.

### Contribuir

```sh
idempiere-sync-upstream
idempiere-new-feature IDEMPIERE-1234-descripcion
mvn82 verify
```

Trabaje en una rama por ticket, revise los cambios y publique explícitamente cuando corresponda. El asistente no crea PR ni hace commit. Si hay cambios locales, remotos incoherentes o divergencias, corrija la causa antes de repetir; no se ejecutan reset ni force push.

### Diagnóstico y archivos locales

`idempiere-doctor` distingue fallos y avisos. Clon o Eclipse ausentes pueden aparecer como avisos antes de la instalación. Configuración Git incoherente en un clon existente y Maven local ausente son fallos. Revise el JDK, los permisos del ejecutable y el árbol Git antes de instalar de nuevo.

Se ignoran `.local-share/`, `.local-bin/`, `.m2/`, `.p2/`, `.direnv/`, `.idempiere-git.env`, herramientas, fuentes y workspace. Los wrappers y manuales se regeneran al recargar; edite [`.envrc`](.envrc) para cambios permanentes. No guarde credenciales en las URL.
