# Entorno aislado de iDempiere 13

Configuración reproducible de desarrollo local para la rama `release-13`, basada en `direnv`. Mantiene separados Java 17, Maven Wrapper, repositorio de dependencias, P2, Eclipse, workspace, fuentes y configuración Git.

[Volver a la guía general](../README.md)

## Qué resuelve

- Selecciona un JDK 17 compatible entre rutas conocidas del sistema.
- Usa siempre el Maven Wrapper incluido en el clon de iDempiere.
- Aísla la caché y configuración Maven en `.m2/`.
- Aísla Eclipse, P2 y el workspace de la versión 13.
- Genera comandos reproducibles en `.local-bin/`.
- Permite clonar el repositorio oficial o un fork personal.
- Valida remotos y evita sincronizaciones destructivas.
- Tolera rutas del entorno que contengan espacios.
- Evita duplicar en `MAVEN_OPTS` la opción administrada del repositorio local al recargar.

La carga del entorno no instala Java o Eclipse, no clona las fuentes y no ejecuta una construcción Maven.

## Resumen técnico

| Componente | Configuración |
|---|---|
| Rama | `release-13` |
| Java | JDK 17 |
| Maven | `sources/idempiere/mvnw` |
| Maven esperado por el doctor | 3.9.10 en `maven-wrapper.properties` |
| Fuentes | `sources/idempiere/` |
| Workspace | `workspace-13/` |
| Usuario/caché Maven | `.m2/` |
| Repositorio Maven | `.m2/repository/` |
| Configuración P2 | `.p2/configuration/` |
| Configuración Git local | `.idempiere-git.env` |

La versión efectiva de Maven no puede confirmarse hasta que exista el clon y se pueda leer su archivo de propiedades del wrapper. El entorno no instala una distribución Maven independiente.

## Requisitos

- Linux y shell compatible con Bash.
- `direnv` integrado con la shell.
- Git.
- JDK 17 en una ruta detectada por `.envrc`.
- Eclipse aportado por el usuario si se utilizará el IDE.
- Red para clonar, sincronizar o descargar dependencias.
- Credenciales Git cuando el fork o una publicación las requieran.

Un ejemplo de integración de `direnv` con Zsh:

```sh
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
exec zsh
```

Revise siempre `.envrc` antes de autorizarlo, ya que `direnv allow` permite ejecutar su contenido en la shell.

## Primera carga

```sh
cd iDempiere13
direnv allow
idempiere-doctor
```

Durante la carga se crean, si faltan:

```text
.local-bin/
.m2/
.m2/repository/
.m2/settings.xml
.p2/
sources/
workspace-13/
```

También se regeneran los nueve wrappers documentados más abajo. `eclipse/` se usa como ruta esperada, pero el entorno no crea ni instala allí una distribución funcional de Eclipse.

Después de modificar `.envrc`:

```sh
direnv allow
```

Después de que un comando cambie sólo la configuración persistida, como el primer clon:

```sh
direnv reload
```

## Clonar el repositorio

```sh
idempiere-clone
```

El comando pregunta por uno de estos modelos:

### Modo `official`

- `origin` apunta a `https://github.com/idempiere/idempiere.git`.
- No se configura `upstream`.
- Es apropiado para consultar o construir directamente la rama oficial.

### Modo `fork`

- `origin` apunta al fork personal indicado por el usuario.
- `upstream` apunta al repositorio oficial.
- Es el modelo previsto para preparar contribuciones.

La URL del fork debe usar HTTP(S), `ssh://` o la forma SSH `git@host:ruta`. No puede contener espacios ni controles. El asistente clona `release-13` en `sources/idempiere`, configura los remotos y guarda el modelo en `.idempiere-git.env`.

Si el destino ya contiene un repositorio, el comando exige que sus remotos coincidan con la configuración persistida. Si el destino contiene otros archivos, termina sin sobrescribirlos.

## Configuración Git persistida

El archivo local `.idempiere-git.env` tiene formato declarativo:

```dotenv
IDEMPIERE_GIT_MODE=fork
IDEMPIERE_ORIGIN_URL=git@github.com:usuario/idempiere.git
IDEMPIERE_UPSTREAM_URL=https://github.com/idempiere/idempiere.git
```

El escritor usa un archivo temporal, lo mueve de forma atómica y asigna permisos `600`. El lector no evalúa el contenido como código de shell. Por compatibilidad acepta el prefijo histórico `export`, pero el formato nuevo no lo genera.

Este archivo está excluido de Git. No incluya credenciales en las URL; use el gestor de credenciales o las claves SSH del sistema.

Para comprobar el resultado:

```sh
direnv reload
idempiere-remotes
```

## Maven Wrapper y construcción

```sh
mvn13 verify
```

`mvn13`:

1. comprueba que `sources/idempiere/mvnw` sea ejecutable;
2. cambia al directorio del clon;
3. fija `JAVA_HOME` y `MAVEN_USER_HOME` del entorno;
4. activa el modo Java headless para Maven;
5. pasa `.m2/settings.xml` y `.m2/repository` de forma explícita;
6. entrega al wrapper todos los argumentos recibidos.

Otros ejemplos:

```sh
mvn13 validate
mvn13 clean verify
mvn13 -DskipTests verify
```

El wrapper puede descargar Maven y dependencias durante la primera ejecución. No utilice un `mvn` global si necesita conservar el aislamiento.

El `.envrc` elimina copias previas de su opción administrada `-Dmaven.repo.local=...` antes de añadir una sola copia a `MAVEN_OPTS`; las demás opciones heredadas se conservan.

## Eclipse

Coloque una instalación compatible de Eclipse en `eclipse/`, de forma que exista:

```text
eclipse/eclipse
```

Para usar siempre el workspace aislado:

```sh
eclipse-start
```

Para mostrar el selector de workspace:

```sh
eclipse-choose
```

Ambos comandos fijan el ejecutable de Java 17, `.p2/configuration` y `GDK_BACKEND=x11`. `eclipse-start` usa directamente `workspace-13`; `eclipse-choose` usa `@noDefault` y lo propone como valor predeterminado.

Antes de importar los proyectos en Eclipse conviene materializar lo que requiera el build actual:

```sh
mvn13 validate
```

El resultado exacto de esa fase depende del POM clonado; el entorno sólo garantiza la ejecución aislada, no un efecto semántico concreto del objetivo Maven.

## Referencia de comandos

| Comando | Acción | Efectos o precondiciones relevantes |
|---|---|---|
| `mvn13 [argumentos]` | Ejecuta `./mvnw` en el clon. | Requiere `mvnw`; puede usar red y escribir en `.m2`. |
| `eclipse-start` | Abre Eclipse con `workspace-13`. | Requiere `eclipse/eclipse`. |
| `eclipse-choose` | Abre Eclipse con selector de workspace. | Requiere `eclipse/eclipse`. |
| `idempiere-root` | Abre una shell nueva en las fuentes. | Requiere `sources/idempiere`. |
| `idempiere-clone` | Configura modo Git y clona `release-13`. | Es interactivo, usa red y escribe `.idempiere-git.env`. |
| `idempiere-remotes` | Muestra modo, `origin` y `upstream`. | Falla si no hay clon o el modo no está configurado. |
| `idempiere-sync-upstream` | Actualiza la rama base con fast-forward. | Exige árbol limpio y estar en `release-13`; en modo fork también hace `push` a `origin`. |
| `idempiere-new-feature <rama>` | Actualiza la base y crea una rama. | Exige nombre válido, árbol limpio y remotos coherentes; usa red. |
| `idempiere-doctor` | Ejecuta las comprobaciones del entorno. | Puede probar conectividad SSH sólo cuando `origin` usa SSH. |

Todos estos archivos se generan desde `.envrc`. No edite `.local-bin` para hacer cambios permanentes.

## Flujo de contribución con fork

Después de clonar en modo `fork` y recargar `direnv`:

```sh
idempiere-remotes
idempiere-sync-upstream
idempiere-new-feature fix-payment-validation
```

Trabaje y confirme los cambios en la rama nueva. La automatización no crea Pull Requests.

`idempiere-sync-upstream` sólo opera si la rama actual es `release-13` y el árbol está limpio. Hace `fetch`, aplica `merge --ff-only` desde `upstream/release-13` y después publica `release-13` en el fork. No usa `reset`, `force push` ni integración automática con conflictos.

`idempiere-new-feature` valida el nombre, actualiza la rama base mediante fast-forward desde el remoto que corresponde al modo y crea la nueva rama. No publica automáticamente esa rama.

## Diagnóstico

```sh
idempiere-doctor
```

El doctor inspecciona:

- JDK y versión de Java;
- Maven Wrapper y versión declarada cuando el clon existe;
- `settings.xml`, repositorio local y caché del wrapper;
- clon, rama, modo Git y coherencia de remotos;
- POM, revisión, Java objetivo, Tycho y plataforma objetivo cuando son observables;
- instalación de Eclipse, workspace y P2;
- conectividad relevante, incluida una prueba SSH con límite de tiempo cuando corresponde.

Los errores incrementan el estado final y producen una salida distinta de cero. Las advertencias informativas no necesariamente bloquean el trabajo.

## Solución de problemas

### `direnv` rechaza o no carga el entorno

Compruebe el hook, revise el archivo y vuelva a autorizar:

```sh
direnv allow
```

La carga termina con error si no encuentra un ejecutable Java 17 válido.

### `mvn13` no encuentra `mvnw`

Clone primero las fuentes:

```sh
idempiere-clone
```

Si el clon existe pero `mvnw` no es ejecutable, compruebe el estado y permisos del archivo antes de modificarlos.

### El modo Git figura como inválido o no configurado

Revise `.idempiere-git.env`, recargue y compare remotos:

```sh
direnv reload
idempiere-remotes
```

No ejecute la sincronización hasta que `origin` y `upstream` coincidan con el modelo elegido.

### La sincronización se detiene

Compruebe la rama y el árbol de trabajo:

```sh
git -C sources/idempiere branch --show-current
git -C sources/idempiere status --short
```

Debe estar en `release-13` y no tener cambios sin guardar. Si el fast-forward no es posible, resuelva la divergencia manualmente; el wrapper no elige una estrategia por usted.

### Eclipse no inicia

Verifique que `eclipse/eclipse` exista y sea ejecutable. El `.envrc` define la ruta, pero no descarga Eclipse.

## Archivos locales y seguridad

El `.gitignore` del entorno excluye `.direnv`, `.local-bin`, `.m2`, `.p2`, `.idempiere-git.env`, Eclipse, las fuentes y `workspace-13`. La raíz del proyecto también excluye configuraciones de agentes, skills, editores y variantes recursivas de configuración local.

No deben versionarse:

- dependencias o cachés Maven;
- instalación de Eclipse y datos P2;
- fuentes clonadas dentro del entorno;
- workspaces y metadatos del IDE;
- configuración Git local o credenciales.

Sí deben versionarse `.envrc`, `.gitignore` y este README.

## Alcance y fuente de verdad

Este entorno prepara y valida herramientas locales; no instala Eclipse, no garantiza el resultado del build y no sustituye la documentación funcional de iDempiere. Los metadatos de versión sólo se confirman cuando existen en el clon.

Ante cualquier discrepancia, prevalece [`.envrc`](.envrc). Este README debe actualizarse en el mismo cambio cuando se añadan rutas, variables, wrappers o efectos nuevos.
