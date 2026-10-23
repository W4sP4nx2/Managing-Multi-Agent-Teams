#!/usr/bin/env bash
set -euo pipefail

# Local teaching exercise only: no package installation, remote, provider, or deploy.
if [[ ${BASH_VERSINFO[0]} -lt 3 ]]; then
    printf 'Bash 3 or newer is required.\n' >&2
    exit 2
fi
for factory_tool in bash git python3 semgrep; do
    if ! command -v "$factory_tool" >/dev/null 2>&1; then
        printf 'Missing prerequisite: %s. See extensions/live_software_factory.md.\n' \
            "$factory_tool" >&2
        exit 2
    fi
done

factory_script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
factory_guide="$(cd -- "$factory_script_dir/.." && pwd)/live_software_factory.md"
export SEMGREP_ENABLE_VERSION_CHECK=0
export SEMGREP_SEND_METRICS=off
git --version
python3 --version
semgrep --version

# Use /tmp explicitly so even a custom TMPDIR cannot put this in the course repo.
factory_workspace=$(mktemp -d /tmp/software-factory.XXXXXX)
printf 'Disposable workspace: %s\n' "$factory_workspace"
mkdir "$factory_workspace/repo"
cd "$factory_workspace/repo"
git init -b main
git config user.name "Factory Exercise"
git config user.email "factory-exercise@example.invalid"
git config commit.gpgsign false
git config core.hooksPath .githooks
mkdir .githooks app

cat > .gitignore <<'EOF'
.env
.env.*
!.env.example
.venv/
__pycache__/
evidence/
EOF
cat > backlog.md <<'EOF'
# Local exercise queue
- [ ] FEAT-001: Add a safe numeric conversion helper
- [ ] FEAT-002: Add a second acceptance test

Budget and deployment services are not connected.
EOF
cat > app/calculate.py <<'EOF'
def parse_integer(text: str) -> int:
    return int(text)
EOF
cat > .semgrep.yml <<'EOF'
rules:
  - id: teaching-no-eval
    languages: [python]
    message: Do not evaluate supplied expressions; use a narrow parser.
    severity: ERROR
    pattern: eval(...)
EOF
git add .gitignore backlog.md app/calculate.py .semgrep.yml
git commit -m "Initialize disposable factory exercise"

cat > .githooks/commit-msg <<'EOF'
#!/bin/sh
set -eu
message_file=${1:?Git must supply the candidate message file}
if ! git interpret-trailers --parse "$message_file" |
    grep -Fxq 'Security-Reviewed: true'; then
    echo 'BLOCKED: a Security-Reviewed: true trailer is required.' >&2
    exit 1
fi
exit 0
EOF

cat > .githooks/pre-commit <<'EOF'
#!/bin/sh
set -eu
if ! command -v semgrep >/dev/null 2>&1; then
    echo 'BLOCKED: Semgrep is unavailable; activate the scanner environment.' >&2
    exit 2
fi
scan_snapshot=$(mktemp -d)
trap 'rm -rf "$scan_snapshot"' EXIT
trap 'exit 2' HUP INT TERM
git checkout-index --all --prefix="$scan_snapshot/"
if (
    cd "$scan_snapshot"
    semgrep scan --config=.semgrep.yml --error --strict \
        --metrics=off --disable-version-check app
); then
    exit 0
else
    scan_status=$?
    echo "BLOCKED: scanner returned $scan_status; inspect findings or errors." >&2
    exit "$scan_status"
fi
EOF
chmod +x .githooks/pre-commit .githooks/commit-msg
git add .githooks
git commit -m "Add independent scan and message gates" \
    -m "Security-Reviewed: true"

git worktree add -b codex/feat-001 ../feat-001 main
git worktree add -b codex/feat-002 ../feat-002 main
git worktree list

printf '\nLocal gate exercise ready. No remote or deployment was configured.\n'
printf 'Repository: %s/repo\n' "$factory_workspace"
printf 'Worktree 1: %s/feat-001\n' "$factory_workspace"
printf 'Worktree 2: %s/feat-002\n' "$factory_workspace"
printf '\nRun this next in your shell:\n  cd %q\n' "$factory_workspace/feat-001"
printf 'Then follow “Prove the behavior” in:\n  %s#prove-the-behavior\n' "$factory_guide"
printf 'This script does not run the negative proof cases or any live agent service.\n'
