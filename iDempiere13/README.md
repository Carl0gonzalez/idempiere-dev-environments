# Isolated iDempiere 13 environment

[Spanish version](README.es.md) · [Back to the main guide](../README.md)

This reproducible `direnv`-based local development configuration targets the `release-13` branch. It keeps Java 17, Maven Wrapper, the dependency repository, P2, Eclipse, the workspace, sources, and Git configuration isolated.

## What it provides

- Selects a compatible JDK 17 from known Linux paths or the macOS Java registry.
- Always uses the Maven Wrapper included in the iDempiere clone.
- Isolates the Maven cache and configuration in `.m2/`.
- Isolates Eclipse, P2, and the version 13 workspace.
- Generates reproducible commands in `.local-bin/`.
- Supports cloning either the official repository or a personal fork.
- Validates remotes and prevents destructive synchronization.
- Supports environment paths containing spaces.
- Prevents its managed Maven repository option from accumulating in `MAVEN_OPTS` after reloads.

Loading the environment does not install Java or Eclipse, clone the sources, or run a Maven build.

## Technical summary

| Component | Configuration |
|---|---|
| Branch | `release-13` |
| Java | JDK 17 |
| Maven | `sources/idempiere/mvnw` |
| Maven version expected by the doctor | 3.9.10 in `maven-wrapper.properties` |
| Sources | `sources/idempiere/` |
| Workspace | `workspace-13/` |
| Maven user home/cache | `.m2/` |
| Maven repository | `.m2/repository/` |
| P2 configuration | `.p2/configuration/` |
| Local Git configuration | `.idempiere-git.env` |

The effective Maven version cannot be confirmed until the clone exists and its wrapper properties file can be read. The environment does not install a separate Maven distribution.

## Requirements

- Linux or macOS and a Bash-compatible shell.
- `direnv` integrated with the shell.
- Git.
- JDK 17 in a path detected by `.envrc`.
- Eclipse supplied by the user when the IDE is needed.
- Network access for cloning, synchronizing, or downloading dependencies.
- Git credentials when a fork or push operation requires them.

Example `direnv` integration for Zsh:

```sh
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
exec zsh
```

Always review `.envrc` before authorizing it because `direnv allow` permits the file to execute in your shell.

## First load

```sh
cd iDempiere13
direnv allow
idempiere-doctor
```

Loading creates these paths when missing:

```text
.local-bin/
.m2/
.m2/repository/
.m2/settings.xml
.p2/
sources/
workspace-13/
```

It also regenerates the nine wrappers documented below. `eclipse/` is an expected location, but the environment does not create or install a working Eclipse distribution there.

After modifying `.envrc`, run:

```sh
direnv allow
```

After a command changes only persisted configuration, as happens after the first clone, run:

```sh
direnv reload
```

## Clone the repository

```sh
idempiere-clone
```

The command asks you to select one of two models.

### `official` mode

- `origin` points to `https://github.com/idempiere/idempiere.git`.
- No `upstream` remote is configured.
- This is suitable for inspecting or building the official branch directly.

### `fork` mode

- `origin` points to the personal fork supplied by the user.
- `upstream` points to the official repository.
- This is the intended model for preparing contributions.

The fork URL must use HTTP(S), `ssh://`, or the `git@host:path` SSH form. It cannot contain spaces or control characters. The helper clones `release-13` into `sources/idempiere`, configures the remotes, and stores the selected model in `.idempiere-git.env`.

If the destination already contains a repository, the command requires its remotes to match the persisted configuration. If the destination contains other files, it exits without overwriting them.

## Persisted Git configuration

The local `.idempiere-git.env` file uses a declarative format:

```dotenv
IDEMPIERE_GIT_MODE=fork
IDEMPIERE_ORIGIN_URL=git@github.com:user/idempiere.git
IDEMPIERE_UPSTREAM_URL=https://github.com/idempiere/idempiere.git
```

The writer creates a temporary file, moves it atomically, and applies `600` permissions. The reader does not evaluate its contents as shell code. For compatibility it accepts the legacy `export` prefix, but the current writer does not generate it.

This file is excluded from Git. Do not embed credentials in URLs; use the system credential manager or SSH keys.

Verify the resulting setup with:

```sh
direnv reload
idempiere-remotes
```

## Maven Wrapper and builds

```sh
mvn13 verify
```

`mvn13` performs the following operations:

1. verifies that `sources/idempiere/mvnw` is executable;
2. changes to the clone directory;
3. sets the environment's `JAVA_HOME` and `MAVEN_USER_HOME`;
4. enables Java headless mode for Maven;
5. explicitly passes `.m2/settings.xml` and `.m2/repository`;
6. forwards every received argument to the wrapper.

Additional examples:

```sh
mvn13 validate
mvn13 clean verify
mvn13 -DskipTests verify
```

The wrapper may download Maven and dependencies during its first execution. Do not use a global `mvn` command when isolation must be preserved.

The `.envrc` removes previous copies of its managed `-Dmaven.repo.local=...` option before adding exactly one copy to `MAVEN_OPTS`; all other inherited options are preserved.

## Eclipse

Place a compatible Eclipse installation in `eclipse/`. The selected executable depends on the operating system:

```text
Linux: eclipse/eclipse
macOS: eclipse/Eclipse.app/Contents/MacOS/eclipse
```

To always use the isolated workspace:

```sh
eclipse-start
```

To display the workspace chooser:

```sh
eclipse-choose
```

Both commands fix the Java 17 executable and `.p2/configuration`. On Linux they also set `GDK_BACKEND=x11`; on macOS they launch the native application without that Linux-specific variable. `eclipse-start` directly uses `workspace-13`; `eclipse-choose` uses `@noDefault` and proposes the isolated workspace.

Before importing projects into Eclipse, it may be useful to materialize the artifacts required by the current build:

```sh
mvn13 validate
```

The exact result of that phase depends on the cloned POM. The environment guarantees isolated execution, not a specific semantic effect for a Maven goal.

## Command reference

| Command | Action | Relevant effects or preconditions |
|---|---|---|
| `mvn13 [arguments]` | Runs `./mvnw` in the clone. | Requires `mvnw`; may use the network and write into `.m2`. |
| `eclipse-start` | Opens Eclipse with `workspace-13`. | Requires the platform-specific Eclipse executable. |
| `eclipse-choose` | Opens Eclipse with the workspace chooser. | Requires the platform-specific Eclipse executable. |
| `idempiere-root` | Opens a new shell in the sources. | Requires `sources/idempiere`. |
| `idempiere-clone` | Configures the Git mode and clones `release-13`. | Interactive; uses the network and writes `.idempiere-git.env`. |
| `idempiere-remotes` | Displays mode, `origin`, and `upstream`. | Fails if there is no clone or the mode is unconfigured. |
| `idempiere-sync-upstream` | Fast-forwards the base branch. | Requires a clean tree on `release-13`; in fork mode it also pushes to `origin`. |
| `idempiere-new-feature <branch>` | Updates the base and creates a branch. | Requires a valid name, clean tree, and consistent remotes; uses the network. |
| `idempiere-doctor` | Runs environment checks. | May test SSH connectivity only when `origin` uses SSH. |

All these files are generated from `.envrc`. Do not edit `.local-bin` for permanent changes.

## Fork contribution workflow

After cloning in `fork` mode and reloading `direnv`:

```sh
idempiere-remotes
idempiere-sync-upstream
idempiere-new-feature fix-payment-validation
```

Work and commit on the new branch. The automation does not create Pull Requests.

`idempiere-sync-upstream` operates only when the current branch is `release-13` and the working tree is clean. It fetches, applies `merge --ff-only` from `upstream/release-13`, and then pushes `release-13` to the fork. It does not use `reset`, force push, or automatic conflict resolution.

`idempiere-new-feature` validates the name, fast-forwards the base branch from the remote appropriate to the selected mode, and creates the new branch. It does not automatically publish that branch.

## Diagnosis

```sh
idempiere-doctor
```

The doctor inspects:

- the JDK and Java version;
- Maven Wrapper and its declared version when the clone exists;
- `settings.xml`, the local repository, and wrapper cache;
- clone, branch, Git mode, and remote consistency;
- POM, revision, target Java, Tycho, and target platform when observable;
- Eclipse installation, workspace, and P2;
- relevant connectivity, including a time-limited SSH test when applicable.

Errors increase the final failure count and result in a non-zero exit status. Informational warnings do not necessarily prevent work.

## Troubleshooting

### `direnv` rejects or does not load the environment

Verify the hook, review the file, and authorize it again:

```sh
direnv allow
```

Loading exits with an error if it cannot find a valid Java 17 executable.

### `mvn13` cannot find `mvnw`

Clone the sources first:

```sh
idempiere-clone
```

If the clone exists but `mvnw` is not executable, inspect its status and permissions before changing them.

### Git mode is invalid or unconfigured

Review `.idempiere-git.env`, reload, and compare the remotes:

```sh
direnv reload
idempiere-remotes
```

Do not synchronize until `origin` and `upstream` match the selected model.

### Synchronization stops

Check the branch and working tree:

```sh
git -C sources/idempiere branch --show-current
git -C sources/idempiere status --short
```

You must be on `release-13` with no uncommitted changes. If a fast-forward is impossible, resolve the divergence manually; the wrapper does not choose a strategy for you.

### Eclipse does not start

Verify `eclipse/eclipse` on Linux or `eclipse/Eclipse.app/Contents/MacOS/eclipse` on macOS. `.envrc` defines the platform-specific path but does not download Eclipse.

## Local files and security

The environment `.gitignore` excludes `.direnv`, `.local-bin`, `.m2`, `.p2`, `.idempiere-git.env`, Eclipse, sources, and `workspace-13`. The project root also excludes agent and skill configuration, editors, and recursive local configuration variants.

Do not version:

- Maven dependencies or caches;
- the Eclipse installation and P2 data;
- sources cloned inside the environment;
- workspaces and IDE metadata;
- local Git configuration or credentials.

Version `.envrc`, `.gitignore`, and this README.

## Scope and source of truth

This environment prepares and validates local tools. It does not install Eclipse, guarantee a successful build, or replace iDempiere functional documentation. Version metadata is only confirmed when present in the clone.

If documentation and implementation disagree, [`.envrc`](.envrc) takes precedence. Update this README in the same change whenever new paths, variables, wrappers, or effects are introduced.
