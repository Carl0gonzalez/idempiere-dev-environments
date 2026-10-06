# Isolated environment for iDempiere 10

[Versión en español](README.es.md) · [General guide](../README.md)

## Requirements and layout

Linux or macOS, Bash, Git, direnv integrated with your shell and the required JDK. Supply Maven and Eclipse manually where indicated. Network and credentials are needed for cloning, downloads and publishing.

```text
iDempiere10/
├── .envrc
├── .m2/settings.xml
├── .m2/repository/
├── .local-bin/
├── .local-share/man/
├── .p2/configuration/
├── eclipse/
├── sources/idempiere/
├── workspace-10/
└── .idempiere-git.env
```

## Updated functionality (2026-10-06)

Base branch: `release-10`; JDK 11; local Maven 3.6.3. Version-specific requirements are preserved.

Help is available through `idempiere-help`, `idempiere-help mvn10`, and `help`, `--help`, `-h` or `--man` as the first command argument. Messages/help use `LC_ALL`, then `LC_MESSAGES`, then `LANG`: Spanish for `es`, English otherwise. JDK selection and some configuration errors retain Spanish messages. Local manuals live in `.local-share/man/es/man1` and `en/man1`; `MANPATH` selects a language at load time. Install `man` and reload direnv after changing locale.

Linux and macOS remain supported. Eclipse is expected at `eclipse/eclipse` or `eclipse/Eclipse.app/Contents/MacOS/eclipse`. Override JDK detection with `IDEMPIERE_JAVA_HOME_OVERRIDE` (or `IDEMPIERE_JAVA_HOME`); `javac` must match the required major. Reloads preserve `MAVEN_OPTS`; settings and repository paths are passed as quoted Maven arguments.

```sh
cd iDempiere10
direnv allow
idempiere-help
idempiere-clone
direnv reload
idempiere-git-check
mvn10 verify
eclipse-start
```

Loading creates directories, settings, wrappers and manuals. It does not install tools or clone sources. Install Maven under `apache-maven-3.6.3/`. Install Eclipse under `eclipse/`. Environment checks do not prove a successful build or runtime startup.

### Git workflow and commands

All versions now offer official/fork cloning. Official mode uses official `origin` without `upstream`. Fork mode uses your fork as `origin` and the official repository as `upstream`. `.idempiere-git.env` is parsed as data, written atomically with permissions `600`, and ignored by Git. Existing checkouts require matching configuration; remotes are never silently repaired. Nonempty clone destinations are rejected.

For an existing official checkout without saved configuration, create this local file and reload:

```dotenv
IDEMPIERE_GIT_MODE=official
IDEMPIERE_ORIGIN_URL=https://github.com/idempiere/idempiere.git
IDEMPIERE_UPSTREAM_URL=
```

| Command | Behavior |
|---|---|
| `idempiere-help [command]` | Lists commands or displays help without running them. |
| `mvn10 [arguments]` | Isolated build; may download dependencies. |
| `eclipse-start` / `eclipse-choose` | Fixed workspace or chooser with local JDK and P2. |
| `idempiere-root` | Opens another shell in sources; use `exit` to return. |
| `idempiere-clone` | Interactive official/fork clone of `release-10`; network and saved config. |
| `idempiere-remotes` | Displays actual remotes without changing them. |
| `idempiere-git-check` | Rejects missing checkout, invalid mode or conflicting remotes. |
| `idempiere-sync-upstream` | Requires clean `release-10`; fetch and local fast-forward only, no push. |
| `idempiere-new-feature <branch>` | Validates name/existence, updates base, creates from remote reference; no push. |
| `idempiere-doctor [--network]` | Local checks; nonzero for failures. SSH only with `--network`. |

`idempiere-fix-maven-config` remains available and modifies checkout `.mvn/maven.config`; review its diff.

Use one branch per ticket, run appropriate checks and publish explicitly. Helpers do not create commits or PRs. Dirty worktrees, invalid remotes and non-fast-forward divergence stop the operation; no reset or force push is performed.

Missing sources/Eclipse can be warnings before setup; conflicting Git configuration on an existing checkout and missing local Maven are failures. Diagnose JDK, permissions and Git state before reinstalling.

Generated `.local-share/`, `.local-bin/`, `.m2/`, `.p2/`, `.direnv/`, private `.idempiere-git.env`, tools, sources and workspace are ignored. Reloads regenerate helpers/manuals; edit [`.envrc`](.envrc) for persistent changes. Keep credentials out of URLs.
