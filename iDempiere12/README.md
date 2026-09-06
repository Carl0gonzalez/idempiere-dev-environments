# Isolated iDempiere 12 environment

[Spanish version](README.es.md) · [Back to the main guide](../README.md)

This `direnv`-based local development configuration targets the `release-12` branch. It isolates Java 17, Maven 3.9.11, dependencies, P2, Eclipse, the workspace, and sources.

## Technical summary

| Component | Configuration |
|---|---|
| Branch | `release-12` |
| Expected revision | `12.0.0` |
| Java | JDK 17 |
| Maven | local `apache-maven-3.9.11/` distribution |
| Sources | `sources/idempiere/` |
| Workspace | `workspace-12/` |
| Maven repository | `.m2/repository/` |
| P2 configuration | `.p2/configuration/` |
| Git repository | official iDempiere repository |

## Setup

Install `direnv`, Git, and a JDK 17, then enable the `direnv` hook. Inside this directory:

1. Extract Maven 3.9.11 into `apache-maven-3.9.11/`.
2. Install Eclipse in `eclipse/`, with its executable at `eclipse/eclipse`.
3. Authorize and diagnose the environment.

```sh
cd iDempiere12
direnv allow
idempiere-doctor
```

`direnv allow` creates the local structure, generates `.m2/settings.xml` when missing, and rebuilds `.local-bin`. It does not install components or clone the project.

## Clone and build

```sh
idempiere-clone
mvn12 clean verify
```

The helper clones `release-12` from the official repository into `sources/idempiere`. It preserves an existing clone and refuses to write over a destination occupied by other files.

`mvn12` always uses `apache-maven-3.9.11/bin/mvn` together with this environment's `settings.xml` and Maven repository. Java runs in headless mode only during Maven execution.

The environment manages exactly one copy of `-Drevision=12.0.0` in `MAVEN_OPTS`: it removes previous copies before adding one and preserves every other inherited option. The repository location is also passed directly to each `mvn12` invocation.

## Eclipse

```sh
eclipse-start
```

The command fixes Java 17, `workspace-12`, `.p2/configuration`, and `GDK_BACKEND=x11`.

```sh
eclipse-choose
eclipse-here
```

`eclipse-choose` displays the chooser and proposes the isolated workspace. `eclipse-here` is a compatibility alias that delegates to `eclipse-start`; it does not change the workspace according to the current directory.

## Command reference

| Command | Action and conditions |
|---|---|
| `mvn12 [arguments]` | Runs Maven 3.9.11 with isolated Java and repository settings. |
| `eclipse-start` | Opens Eclipse with the fixed workspace. |
| `eclipse-here` | Compatibility alias for `eclipse-start`. |
| `eclipse-choose` | Opens Eclipse with the workspace chooser. |
| `idempiere-root` | Opens a new shell in the sources; requires the clone. |
| `idempiere-clone` | Clones the official branch over the network without overwriting content. |
| `idempiere-fix-maven-config` | Regenerates `.mvn/maven.config` with one argument per line. |
| `idempiere-doctor` | Validates the environment and returns a non-zero status on failures. |

The generated `maven.config` format is compatible with Maven 3.9: the `-s` option, its value, and `-Dmaven.repo.local=...` are written as separate arguments. The command modifies that file inside the clone.

## Diagnosis and maintenance

```sh
idempiere-doctor
```

The doctor checks Java 17, Maven 3.9.11, `settings.xml`, the local repository, Eclipse, Git, `curl`, wrappers, branch, `.mvn`, target platform, revision, and other metadata observable in the POM. POM inspection is static.

After changing `.envrc`, authorize it again. Wrappers are reproducible, so permanent corrections must be made in `.envrc`.

The `.gitignore` excludes `.local-bin`, `.m2`, `.p2`, Maven, Eclipse, sources, `workspace-12`, and the legacy `workspace/` directory.

## Limitations

- The helper uses the official repository and does not automatically configure a fork or `upstream`.
- Maven and Eclipse must be supplied manually.
- The first dependency resolution requires network access.
- [`.envrc`](.envrc) is the source of truth.
