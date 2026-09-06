# Isolated iDempiere 8.2 environment

[Spanish version](README.es.md) · [Back to the main guide](../README.md)

This `direnv`-based local development configuration targets the `release-8.2` branch. It isolates Java 11, Maven 3.6.3, the Maven repository, P2, Eclipse, the workspace, and sources from every other version.

## Technical summary

| Component | Configuration |
|---|---|
| Branch | `release-8.2` |
| Java | JDK 11 |
| Maven | local `apache-maven-3.6.3/` distribution |
| Sources | `sources/idempiere/` |
| Workspace | `workspace-8.2/` |
| Maven repository | `.m2/repository/` |
| P2 configuration | `.p2/configuration/` |
| Git repository | official iDempiere repository |

## Setup

Install `direnv`, Git, and a JDK 11, then enable the `direnv` hook in your shell. Inside this directory:

1. Extract Maven 3.6.3 into `apache-maven-3.6.3/`.
2. Install Eclipse as `eclipse/eclipse` on Linux or `eclipse/Eclipse.app` on macOS.
3. Authorize and diagnose the environment.

```sh
cd iDempiere8.2
direnv allow
idempiere-doctor
```

Loading creates the local directories, generates `.m2/settings.xml` when missing, and rebuilds the wrappers in `.local-bin`. It does not install software or clone sources.

## Clone and build

```sh
idempiere-clone
mvn82 clean verify
```

`idempiere-clone` clones `release-8.2` from the official repository into `sources/idempiere`. If the destination already contains a repository or `pom.xml`, it is preserved; if it contains other files, the command exits without overwriting them.

`mvn82` exclusively runs `apache-maven-3.6.3/bin/mvn`, enables Java headless mode for Maven, and always passes the isolated `settings.xml` and local repository.

The `.envrc` preserves inherited Maven options and manages exactly one copy of `-Dmaven.repo.local=...`; repeated reloads must not accumulate that option.

## Eclipse

```sh
eclipse-start
```

This command fixes Java 11, `workspace-8.2`, and `.p2/configuration`. It sets `GDK_BACKEND=x11` only on Linux; macOS launches the native `Eclipse.app` executable. To choose a different workspace while keeping the isolated one as the proposed default:

```sh
eclipse-choose
```

After sources are available, the environment also prepares the compatibility link for `org.adempiere.server-feature/utils.unix` in the workspace when its target exists in the clone.

## Command reference

| Command | Action and conditions |
|---|---|
| `mvn82 [arguments]` | Runs the isolated local Maven; fails if it is not installed. |
| `eclipse-start` | Opens Eclipse with the fixed environment workspace. |
| `eclipse-choose` | Opens the workspace chooser and proposes `workspace-8.2`. |
| `idempiere-root` | Opens a new shell in `sources/idempiere`; requires the sources. |
| `idempiere-clone` | Clones the official branch over the network without overwriting a non-empty destination. |
| `idempiere-fix-maven-config` | Regenerates `.mvn/maven.config` in the clone with isolated Maven paths. |
| `idempiere-doctor` | Checks the environment and returns a non-zero status when failures are found. |

`idempiere-fix-maven-config` modifies a file inside the clone. Use it when the project's Maven configuration has been removed or no longer points to the local environment.

## Diagnosis and maintenance

```sh
idempiere-doctor
```

The doctor checks Java, Maven, `settings.xml`, the local repository, Eclipse, Git, `curl`, wrappers, branch, `.mvn` configuration, target platform, and metadata available in the POM. POM checks are static; they do not run a build to derive values.

After changing `.envrc`, run `direnv allow` again. Wrappers in `.local-bin` are regenerated on every load, so permanent fixes belong in `.envrc`.

The environment `.gitignore` excludes `.local-bin`, `.m2`, `.p2`, `apache-maven-3.6.3`, Eclipse, sources, and `workspace-8.2`.

On macOS, `.envrc` selects JDK 11 with `/usr/libexec/java_home -v 11`. Run `/usr/libexec/java_home -V` if the JDK is not detected.

## Limitations

- The Git helper only configures the official repository; it does not automatically manage a fork or `upstream` remote.
- Eclipse and Maven must be supplied locally.
- The first build needs network access for dependencies not yet present in `.m2/repository`.
- [`.envrc`](.envrc) is the source of truth.
