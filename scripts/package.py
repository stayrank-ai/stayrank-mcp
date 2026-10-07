#!/usr/bin/env python3
"""Build both Stayrank plugin packages from the single source in plugins/stayrank/.

  dist/stayrank-chatgpt.zip  OpenAI Agent Plugins format: plugin.json and mcp.json at the root,
                             skills/, assets/. Validated by scripts/build_openai_zip.py (OpenAI's
                             published submission rules) before anything is written.
  dist/stayrank-claude.zip   Claude plugin: .claude-plugin/plugin.json, .mcp.json, skills/,
                             assets/, README.md, LICENSE. The zip root is the plugin itself.

Usage: python scripts/package.py
"""
import os, shutil, subprocess, sys, tempfile, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "plugins", "stayrank")
DIST = os.path.join(ROOT, "dist")
HERE = os.path.dirname(os.path.abspath(__file__))
COMMON = ["skills", "assets", "README.md", "LICENSE"]


def copy(rel, dst):
    src = os.path.join(SRC, rel)
    out = os.path.join(dst, rel)
    if os.path.isdir(src):
        shutil.copytree(src, out)
    else:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copy2(src, out)


def zip_dir(folder, out):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(folder):
            for name in sorted(files):
                full = os.path.join(base, name)
                z.write(full, os.path.relpath(full, folder).replace(os.sep, "/"))


def main():
    os.makedirs(DIST, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        openai = os.path.join(tmp, "openai")
        os.makedirs(openai)
        for rel in COMMON:
            copy(rel, openai)
        shutil.copy2(os.path.join(SRC, ".openai", "plugin.json"), os.path.join(openai, "plugin.json"))
        shutil.copy2(os.path.join(SRC, ".openai", "mcp.json"), os.path.join(openai, "mcp.json"))
        out = os.path.join(DIST, "stayrank-chatgpt.zip")
        if os.path.exists(out):
            os.remove(out)
        if subprocess.call([sys.executable, os.path.join(HERE, "build_openai_zip.py"), openai, out]) != 0:
            sys.exit("ChatGPT package: validation failed, nothing written.")

        claude = os.path.join(tmp, "claude")
        os.makedirs(claude)
        for rel in COMMON + [".claude-plugin", ".mcp.json"]:
            copy(rel, claude)
        zip_dir(claude, os.path.join(DIST, "stayrank-claude.zip"))

    for name in ("stayrank-chatgpt.zip", "stayrank-claude.zip"):
        path = os.path.join(DIST, name)
        with zipfile.ZipFile(path) as z:
            print("%s (%d bytes): %s" % (name, os.path.getsize(path), ", ".join(z.namelist())))


if __name__ == "__main__":
    main()
