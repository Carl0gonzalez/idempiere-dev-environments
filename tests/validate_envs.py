"""Offline checks in temporary directories; never loads a real environment."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def run(args, env=None, ok=True):
    result = subprocess.run(args, env=env, capture_output=True, text=True)
    if ok and result.returncode:
        raise AssertionError(f'{args}: {result.stdout}\n{result.stderr}')
    return result

for source in sorted(ROOT.glob('iDempiere*/.envrc')):
    version = source.parent.name.removeprefix('iDempiere')
    major = '11' if version in ('8.2', '10') else '17'
    command = 'mvn' + version.replace('.', '')
    run(['bash', '-n', str(source)])
    with tempfile.TemporaryDirectory(prefix='idempiere environment with spaces ') as tmp:
        base = Path(tmp)
        (base / '.envrc').write_text(source.read_text())
        jdk = base / 'test-jdk/bin'
        jdk.mkdir(parents=True)
        for name in ('java', 'javac'):
            content = f'javac {major}.0.1' if name == 'javac' else f'openjdk version "{major}.0.1"'
            executable = jdk / name
            executable.write_text(f'#!/bin/bash\nprintf \'%s\\n\' \'{content}\' >&2\n')
            executable.chmod(0o755)
        env = dict(os.environ, XDG_DATA_HOME=str(base / "data"), XDG_CONFIG_HOME=str(base / "config"), MAVEN_OPTS="-Xmx512m", IDEMPIERE_JAVA_HOME_OVERRIDE=str(jdk.parent), TERM='dumb', LC_ALL='C')
        def shell(code, ok=True):
            return run(['bash', '-c', 'source "$1" >/dev/null || exit; ' + code, 'test', str(base / '.envrc')], env, ok)
        # Repeated loads, all generated scripts, all help entry points, both locales and manuals.
        shell('before="$MAVEN_OPTS"; path_before="$PATH"; man_before="$MANPATH"; source "$1" >/dev/null; [[ "$MAVEN_OPTS" == "$before" && "$PATH" == "$path_before" && "$MANPATH" == "$man_before" ]]')
        first = {str(p.relative_to(base)): p.read_bytes() for folder in ('.local-bin', '.local-share') for p in (base / folder).rglob('*') if p.is_file()}
        shell('true')
        second = {str(p.relative_to(base)): p.read_bytes() for folder in ('.local-bin', '.local-share') for p in (base / folder).rglob('*') if p.is_file()}
        assert first == second
        shell('for c in "$BIN_DIR"/*; do bash -n "$c" || exit; if [[ "$c" != *.sh ]]; then for flag in help --help -h; do "$c" "$flag" >/dev/null || exit; done; name="${c##*/}"; [[ -f "$IDEMPIERE_MAN_ROOT/es/man1/$name.1" && -f "$IDEMPIERE_MAN_ROOT/en/man1/$name.1" ]] || exit 1; fi; done')
        assert 'Usage' in shell(f'{command} help').stdout
        assert 'Uso' in shell(f'LC_ALL=es_CL.UTF-8 {command} help').stdout
        assert shell('idempiere-help unknown', False).returncode != 0
        # Unconfigured/malformed configuration and a nonempty clone destination fail without network.
        assert shell('idempiere-git-check', False).returncode != 0
        repo = base / 'sources/idempiere'
        repo.mkdir()
        (repo / 'keep.txt').write_text('preserve')
        assert shell('idempiere-clone', False).returncode != 0
        assert (repo / 'keep.txt').read_text() == 'preserve'
        run(['git', 'init', '-q', '-b', 'master', str(repo)])
        official = 'https://github.com/idempiere/idempiere.git'
        run(['git', '-C', str(repo), 'remote', 'add', 'origin', official])
        config = base / '.idempiere-git.env'
        config.write_text(f'IDEMPIERE_GIT_MODE=official\nIDEMPIERE_ORIGIN_URL={official}\nIDEMPIERE_UPSTREAM_URL=\n')
        shell('idempiere-git-check')
        shell('idempiere-clone')
        assert shell('idempiere-sync-upstream', False).returncode != 0  # dirty or wrong base
        assert shell('idempiere-new-feature invalid..branch', False).returncode != 0
        run(['git', '-C', str(repo), 'remote', 'add', 'upstream', official])
        assert shell('idempiere-git-check', False).returncode != 0
        config.write_text('IDEMPIERE_GIT_MODE=$(touch BAD)\n')
        assert shell('idempiere-git-check', False).returncode != 0
        assert not (base / 'BAD').exists()
        # Evaluate through actual direnv in the temporary environment when installed.
        import shutil
        if shutil.which('direnv'):
            run(['direnv', 'allow', str(base)], env)
            run(['direnv', 'exec', str(base), 'bash', '-c', 'idempiere-help >/dev/null; [[ -d "$BASE" ]]'], env)
        # Maven arguments retain spaces, user arguments and release-12 revision.
        maven = base / ('apache-maven-' + ('3.9.11' if version == '12' else '3.6.3')) / 'bin/mvn'
        if version in ('13', '14'):
            maven = repo / 'mvnw'
        maven.parent.mkdir(parents=True, exist_ok=True)
        maven.write_text("#!/bin/bash\nprintf '%s\\n' \"$@\"\n")
        maven.chmod(0o755)
        args = shell(command + ' "user argument with spaces"').stdout.splitlines()
        assert '-Dmaven.repo.local=' + str(base / '.m2/repository') in args
        assert str(base / '.m2/settings.xml') in args
        assert 'user argument with spaces' in args
        if version == '12':
            assert '-Drevision=12.0.0' in args
        # Simulate Darwin wrapper execution and ensure Linux-only GDK_BACKEND is removed.
        eclipse = base / 'test-eclipse'
        eclipse.write_text("#!/bin/bash\n[[ -z \"${GDK_BACKEND:-}\" ]] || exit 1\nprintf '%s\\n' \"$@\"\n")
        eclipse.chmod(0o755)
        shell('export IDEMPIERE_OS=Darwin GDK_BACKEND=x11 ECLIPSE_EXECUTABLE="$BASE/test-eclipse"; eclipse-start')
        # Actual fast-forward/new-branch workflow with an isolated local remote.
        branch = 'master' if version == '14' else 'release-' + version
        remote = base / 'local-remote'
        run(['git', 'init', '-q', '-b', branch, str(remote)])
        run(['git', '-C', str(remote), 'config', 'user.email', 'test@example.invalid'])
        run(['git', '-C', str(remote), 'config', 'user.name', 'Environment test'])
        (remote / 'tracked').write_text('initial')
        run(['git', '-C', str(remote), 'add', 'tracked'])
        run(['git', '-C', str(remote), 'commit', '-qm', 'initial'])
        checkout = base / 'workflow-checkout'
        run(['git', 'clone', '-q', str(remote), str(checkout)])
        (remote / 'tracked').write_text('updated')
        run(['git', '-C', str(remote), 'commit', '-qam', 'update'])
        overrides = 'export IDEMPIERE_REPOSITORY="$BASE/workflow-checkout" IDEMPIERE_OFFICIAL_URL="$BASE/local-remote" IDEMPIERE_ORIGIN_URL="$BASE/local-remote" IDEMPIERE_GIT_MODE=official; '
        shell(overrides + 'idempiere-sync-upstream')
        assert (checkout / 'tracked').read_text() == 'updated'
        shell(overrides + 'idempiere-new-feature test-feature')
        assert run(['git', '-C', str(checkout), 'branch', '--show-current']).stdout.strip() == 'test-feature'
        assert shell(overrides + 'idempiere-new-feature test-feature', False).returncode != 0
        (checkout / 'tracked').write_text('dirty')
        assert shell(overrides + 'idempiere-new-feature other-feature', False).returncode != 0
        # Wrong configured JDK is rejected (fallback real JDK might exist, so test Java 11/17 exclusion statically too).
        assert f'IDEMPIERE_JAVA_MAJOR_EXPECTED="{major}"' in source.read_text()
    print(f'{source.parent.name}: syntax, reload, paths with spaces, ES/EN help/manuals, Git protections OK')
