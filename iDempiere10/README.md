# Isolated iDempiere 10 environment

[Spanish version](README.es.md) · [Back to the main guide](../README.md)

This `direnv`-based local development configuration targets the `release-10` branch. It keeps Java 11, Maven 3.6.3, dependencies, P2, Eclipse, the workspace, and sources isolated.

## Technical summary

| Component | Configuration |
|---|---|
| Branch | `release-10` |
| Java | JDK 11 |
| Maven | local `apache-maven-3.6.3/` distribution |
| Sources | `sources/idempiere/` |
| Workspace | `workspace-10/` |
| Maven repository | `.m2/repository/` |
| P2 configuration | `.p2/configuration/` |
| Git repository | official iDempiere repository |

## Setup

Install `direnv`, Git, and a JDK 11, then enable the `direnv` hook in your shell. Next:

1. Extract Maven 3.6.3 into `apache-maven-3.6.3/`.
2. Install Eclipse in `eclipse/`, with its executable at `eclipse/eclipse`.
3. Authorize and diagnose the environment.

```sh
cd iDempiere10
direnv allow
idempiere-doctor
```

Loading creates the isolated structure, generates `.m2/settings.xml` when missing, and rebuilds the commands in `.local-bin`. It does not download Maven, Eclipse, or the sources.

## Clone and build

```sh
idempiere-clone
mvn10 clean verify
```

The clone uses the official `release-10` branch and is stored in `sources/idempiere`. The helper refuses to clone over a non-empty directory and does not delete local content.

`mvn10` runs the specified local Maven, uses the selected JDK, enables headless mode only for Maven, and forces `.m2/settings.xml` and `.m2/repository` as the isolated configuration.

The managed `-Dmaven.repo.local=...` option is removed before it is added again. This preserves unrelated inherited options without accumulating duplicates on each reload.

## Eclipse

```sh
eclipse-start
```

Eclipse starts with Java 11, `workspace-10`, `.p2/configuration`, and `GDK_BACKEND=x11`. To display the workspace chooser:

```sh
eclipse-choose
```

The second command proposes the isolated workspace as the default while allowing another one to be selected.

## Command reference

| Command | Action and conditions |
|---|---|
| `mvn10 [arguments]` | Runs Maven 3.6.3 with isolated configuration; fails if it is not installed. |
| `eclipse-start` | Opens Eclipse with the fixed workspace. |
| `eclipse-choose` | Opens Eclipse with the workspace chooser. |
| `idempiere-root` | Opens a new shell in the sources; requires the clone. |
| `idempiere-clone` | Clones the official branch over the network without overwriting a non-empty destination. |
| `idempiere-fix-maven-config` | Regenerates `sources/idempiere/.mvn/maven.config`. |
| `idempiere-doctor` | Inspects the environment and returns a non-zero status when failures are found. |

Repairing `maven.config` deliberately writes inside the clone and fixes both the settings file and Maven repository for this environment.

## Diagnosis and maintenance

```sh
idempiere-doctor
```

The doctor checks Java, Maven, `settings.xml`, the local repository, Eclipse, Git, `curl`, wrappers, branch, `.mvn` files, target platform, and POM metadata. POM inspection is static and does not replace a real build.

After editing `.envrc`, run `direnv allow`. The wrappers in `.local-bin` are regenerated on each load and must not be edited as source files.

The `.gitignore` excludes `.local-bin`, `.m2`, `.p2`, the Maven distribution, Eclipse, sources, and `workspace-10`.

## Limitations

- `idempiere-clone` uses the official repository; this version does not automate a fork/upstream model.
- Maven and Eclipse must be installed manually at their local paths.
- Resolving missing dependencies requires network access.
- [`.envrc`](.envrc) is the source of truth.
