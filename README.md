# Isolated development environments for iDempiere

[Spanish version](README.es.md)

This repository provides `direnv` configurations for working with multiple iDempiere versions without mixing Java, Maven, dependency repositories, Eclipse installations, or workspaces. Each subdirectory is an independent environment, and its `.envrc` file is the source of truth.

![Isolated development environment for iDempiere 13](assets/idempiere13-entorno-aislado.png)

## Available versions

| Directory | iDempiere branch | Java | Maven | Build command | Assisted Git model |
|---|---|---:|---|---|---|
| [`iDempiere8.2`](iDempiere8.2/README.md) | `release-8.2` | 11 | local 3.6.3 | `mvn82` | official repository |
| [`iDempiere10`](iDempiere10/README.md) | `release-10` | 11 | local 3.6.3 | `mvn10` | official repository |
| [`iDempiere12`](iDempiere12/README.md) | `release-12` | 17 | local 3.9.11 | `mvn12` | official repository |
| [`iDempiere13`](iDempiere13/README.md) | `release-13` | 17 | project Maven Wrapper | `mvn13` | official or fork |

The listed local Maven versions are the distributions expected by each `.envrc`. For version 13, the effective version is determined by `sources/idempiere/.mvn/wrapper/maven-wrapper.properties` after the project has been cloned.

## Requirements

- Linux or macOS and a Bash-compatible shell.
- `direnv`, integrated with the shell.
- Git and network access for cloning and downloading dependencies.
- JDK 11 for iDempiere 8.2 and 10.
- JDK 17 for iDempiere 12 and 13.
- Eclipse installed manually in the `eclipse/` directory of the environment being used.
- Maven extracted manually into `apache-maven-3.6.3/` for 8.2 and 10, or `apache-maven-3.9.11/` for 12.

This project does not install Java, Maven, or Eclipse. It also does not clone sources during `direnv allow`.

Configure the `direnv` hook for your shell once. For example, with Zsh:

```sh
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
exec zsh
```

## Getting started

Clone this repository and enter it:

```sh
git clone git@github.com:Carl0gonzalez/idempiere-dev-environments.git
cd idempiere-dev-environments
```

Choose a version and enter its directory. For example:

```sh
cd iDempiere13
direnv allow
idempiere-doctor
idempiere-clone
direnv reload
mvn13 verify
eclipse-start
```

For another version, change the directory and Maven command according to the table. For 8.2, 10, and 12, first place the expected Maven distribution in the indicated directory. On Linux, install Eclipse as `eclipse/eclipse`; on macOS, place `Eclipse.app` at `eclipse/Eclipse.app`.

`direnv allow` performs local, repeatable setup tasks:

- selects the compatible JDK;
- defines environment paths;
- creates `.m2`, `.p2`, `.local-bin`, `sources`, and the workspace;
- creates a local Maven `settings.xml` when missing;
- regenerates helper commands and temporarily adds them to `PATH`.

It does not download components or modify a global Maven or Eclipse installation.

## Environment layout

```text
iDempiereXX/
├── .envrc                 versioned configuration
├── .gitignore             version-specific local exclusions
├── .local-bin/            generated commands
├── .m2/                   isolated Maven configuration and repository
├── .p2/                   isolated P2 configuration
├── eclipse/               local installation supplied by the user
├── sources/idempiere/     source clone
└── workspace-XX/          Eclipse workspace
```

Generated directories, cloned sources, local tools, and private Git configuration are excluded through `.gitignore`. The `.envrc` files and README documents must remain versioned.

## Common commands

| Command | Purpose |
|---|---|
| `idempiere-clone` | Clones the expected branch into `sources/idempiere`; refuses to overwrite a non-empty destination. |
| `idempiere-root` | Opens a new shell located in the iDempiere sources. |
| `idempiere-doctor` | Checks Java, Maven, Git, Eclipse, paths, and available metadata. Returns a non-zero status when failures are detected. |
| `eclipse-start` | Starts Eclipse with the environment JDK, workspace, and P2 configuration. |
| `eclipse-choose` | Starts Eclipse with the workspace chooser and proposes the isolated workspace. |

Versions 8.2, 10, and 12 also provide `idempiere-fix-maven-config`, which regenerates `sources/idempiere/.mvn/maven.config` with the isolated repository and `settings.xml`. Version 12 additionally preserves `eclipse-here` as an alias for `eclipse-start`.

iDempiere 13 adds a safe Git workflow for an official repository or personal fork: `idempiere-remotes`, `idempiere-sync-upstream`, and `idempiere-new-feature <branch>`. Read its [version-specific guide](iDempiere13/README.md) before synchronizing because, in fork mode, synchronization also pushes the base branch to `origin`.

## Daily workflow

```sh
cd iDempiere12
direnv allow                 # only the first time or after changing .envrc
idempiere-doctor
idempiere-root
```

From the shell opened in the sources, work normally. To build from any location inside the environment, use its version-specific wrapper, for example:

```sh
mvn12 clean verify
```

When you leave the directory, `direnv` removes its variables and `PATH` entries. To switch versions, enter another subdirectory and let `direnv` load that environment.

## Quick diagnosis

Run this first:

```sh
idempiere-doctor
```

Common issues:

- **The environment does not activate:** verify that the `direnv` hook is loaded and run `direnv allow`.
- **Java is missing or incompatible:** install the required JDK in one of the system paths recognized by `.envrc`.
- **Maven does not exist:** for 8.2, 10, or 12, verify the exact distribution directory shown in the table.
- **`mvn13` cannot find `mvnw`:** run `idempiere-clone` first.
- **Eclipse does not start:** verify `eclipse/eclipse` on Linux or `eclipse/Eclipse.app/Contents/MacOS/eclipse` on macOS.
- **The clone destination is not empty:** inspect `sources/idempiere` manually; the helper never deletes or replaces it.
- **`.envrc` changed:** authorize it again with `direnv allow` and rerun the doctor.

## Security and maintenance

- Always review `.envrc` changes before authorizing them: `direnv allow` executes that file in your shell.
- Do not store credentials in `.envrc`, `settings.xml`, or `.idempiere-git.env`.
- Do not share `.m2`, `.p2`, Eclipse installations, or workspaces between versions.
- The wrappers in `.local-bin` are generated; fix their templates in `.envrc`, not the generated files.
- To verify that a modification remains idempotent, reload twice and check that `PATH` and `MAVEN_OPTS` do not accumulate entries.

The detailed documentation for each version describes its differences, commands, and usage conditions. If documentation and implementation disagree, the version's `.envrc` takes precedence.

## macOS notes

The environments detect Darwin automatically, select the required JDK through `/usr/libexec/java_home`, use the executable inside `Eclipse.app`, and avoid the Linux-only `GDK_BACKEND=x11` setting. Homebrew installations of `direnv` and Git are supported. To inspect the JDKs registered by macOS, run `/usr/libexec/java_home -V`.

## License

This project is distributed under the [MIT License](LICENSE). Copyright (c) 2026 Carlo González.
