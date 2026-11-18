#!/usr/bin/env python3
"""Bangun ulang file dari export conversation OpenHands.

Pakai:
    python3 rebuild_from_conversation.py conversation.json  -o restored/

Mendukung format event lama (action: write/edit/create) dan format
tool-call baru (file_editor dengan command create/str_replace/insert).
File terakhir yang menang. Aman: tidak menulis di luar folder output.
"""
import argparse
import json
import os
import pathlib
import sys


def walk(node, out):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value, out)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value, out)


def norm_path(p):
    p = str(p).strip().lstrip("./")
    return p


def safe_join(root, rel):
    rel = norm_path(rel)
    target = (root / rel).resolve()
    if not str(target).startswith(str(root.resolve())):
        return None
    return target


def get(d, *keys):
    for k in keys:
        if isinstance(d, dict) and k in d and d[k] is not None:
            return d[k]
    return None


def apply_patch_text(old, new, text):
    if old == "" and new is not None:
        return text + (new or "")
    count = text.count(old)
    if count == 0:
        return None
    return text.replace(old, new or "", 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="conversation.json hasil download")
    ap.add_argument("-o", "--out", default="restored", help="folder hasil")
    args = ap.parse_args()

    root = pathlib.Path(args.out)
    src = pathlib.Path(args.source)

    docs = []
    if src.is_dir():
        for f in sorted(src.glob("*.json")):
            try:
                docs.append(json.loads(f.read_text(errors="ignore")))
            except Exception:
                pass
    else:
        raw = src.read_text(errors="ignore")
        try:
            docs = [json.loads(raw)]
        except Exception:
            for line in raw.splitlines():
                line = line.strip()
                if line.startswith("{"):
                    try:
                        docs.append(json.loads(line))
                    except Exception:
                        pass

    files = {}
    order = 0
    expanded = []
    for doc in docs:
        for node in walk(doc, None):
            expanded.append(node)
            args = node.get("arguments") if isinstance(node, dict) else None
            if isinstance(args, str) and args.strip().startswith("{"):
                try:
                    parsed = json.loads(args)
                except Exception:
                    parsed = None
                if isinstance(parsed, dict):
                    merged = dict(node)
                    merged.update(parsed)
                    expanded.append(merged)

    for node in expanded:
            path = get(node, "path", "file_path", "filename")
            if not path or not isinstance(path, str):
                continue
            if any(path.endswith(s) for s in (".pyc", ".log")):
                pass

            text = get(node, "file_text", "content")
            old = get(node, "old_str", "old_string")
            new = get(node, "new_str", "new_string")
            command = get(node, "command")

            if isinstance(text, str) and (old is None and new is None):
                files[norm_path(path)] = text
                order += 1
            elif isinstance(old, str) and (new is not None or command == "str_replace"):
                current = files.get(norm_path(path))
                if current is None:
                    current = ""
                patched = apply_patch_text(old, new, current)
                if patched is not None:
                    files[norm_path(path)] = patched
                    order += 1
            elif command == "insert" and isinstance(new, str):
                current = files.get(norm_path(path), "")
                files[norm_path(path)] = current + new
                order += 1

    if not files:
        print("Tidak ada operasi tulis-file yang terbaca. Cek apakah export memuat tool call.")
        return 1

    root.mkdir(parents=True, exist_ok=True)
    written = 0
    for rel, content in files.items():
        target = safe_join(root, rel)
        if target is None:
            print("lewati (path aneh):", rel)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, errors="ignore")
        written += 1

    print(f"{written} file ditulis ke {root.resolve()}")
    for rel in sorted(files)[:20]:
        print("  -", rel)
    if len(files) > 20:
        print(f"  ... dan {len(files) - 20} file lain")
    return 0


if __name__ == "__main__":
    sys.exit(main())
