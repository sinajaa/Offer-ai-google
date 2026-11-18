#!/usr/bin/env bash
# Simpan pekerjaan tiap beberapa menit: commit + push + zip.
# Pakai: ./autosave.sh [menit]   (default 10, 0 = sekali jalan)
set -uo pipefail

INTERVAL="${1:-10}"
REPO_DIR="${REPO_DIR:-$PWD}"
BRANCH="${BRANCH:-$(git -C "$REPO_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)}"
BACKUP_DIR="${BACKUP_DIR:-/workspace/backup}"

mkdir -p "$BACKUP_DIR"

log() { printf '[%s] %s\n' "$(date -u +%H:%M:%S)" "$*"; }

save_once() {
  cd "$REPO_DIR" || return 1

  if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    git add -A
    git -c user.name="${GIT_NAME:-openhands}" \
        -c user.email="${GIT_EMAIL:-openhands@all-hands.dev}" \
        commit -qm "wip: autosave $(date -u +%Y-%m-%dT%H:%M:%SZ)" || true
    log "commit dibuat"
  else
    log "tidak ada perubahan"
  fi

  if git remote get-url origin >/dev/null 2>&1; then
    for i in 1 2 3; do
      if git push -q origin "$BRANCH" 2>/dev/null; then log "push ok ($BRANCH)"; break; fi
      log "push gagal, coba lagi ($i/3)"; sleep 5
    done
  else
    log "remote origin belum ada, hanya commit lokal"
  fi

  local stamp zip
  stamp=$(date -u +%Y%m%d-%H%M%S)
  zip="$BACKUP_DIR/$(basename "$REPO_DIR")-$stamp.zip"
  if command -v zip >/dev/null 2>&1; then
    zip -qr "$zip" . -x ".git/*" >/dev/null 2>&1 && log "zip: $zip"
  else
    python3 - "$zip" <<'PY' 2>/dev/null && log "zip(py): $zip"
import sys, pathlib, zipfile
out = pathlib.Path(sys.argv[1]); root = pathlib.Path(".")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in root.rglob("*"):
        if p.is_file() and ".git" not in p.parts:
            z.write(p, p.relative_to(root))
PY
  fi

  # simpan 20 backup terakhir saja
  ls -1t "$BACKUP_DIR"/*.zip 2>/dev/null | tail -n +21 | xargs -r rm -f
}

if [ "$INTERVAL" = "0" ]; then
  save_once
else
  log "autosave tiap ${INTERVAL} menit di $REPO_DIR (Ctrl+C untuk stop)"
  while true; do
    save_once
    sleep $((INTERVAL * 60))
  done
fi
