#!/usr/bin/env python3
"""Stage a package locally, then compile the real Universe starter template."""
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"


def run(*args):
    subprocess.run([str(arg) for arg in args], cwd=ROOT, check=True)


def stage():
    manifest = tomllib.loads((ROOT / "typst.toml").read_text())
    package = manifest["package"]
    destination = BUILD / "packages" / "preview" / package["name"] / package["version"]
    destination.mkdir(parents=True, exist_ok=True)
    # Explicit allowlist prevents local outputs or editor files entering a release.
    for name in ("lib.typ", "src", "template", "typst.toml", "LICENSE", "README.md",
                 "THIRD_PARTY_NOTICES.md", "docs", "thumbnail.png"):
        source = ROOT / name
        if not source.exists():
            continue
        target = destination / name
        if source.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
    return BUILD / "packages"


def main():
    package_path = stage()
    run("typst", "compile", "--root", ROOT, "--package-path", package_path,
        ROOT / "template/main.typ", BUILD / "neat-book.pdf")
    if "--thumbnail" in sys.argv:
        run("typst", "compile", "--root", ROOT, "--package-path", package_path,
            "--format", "png", "--pages", "1", "--ppi", "150",
            ROOT / "template/main.typ", ROOT / "thumbnail.png")
        stage()
    print(f"Built {BUILD / 'neat-book.pdf'}")


if __name__ == "__main__":
    main()
