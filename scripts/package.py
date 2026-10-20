#!/usr/bin/env python3
"""Create a small, explicit Universe submission directory and tarball."""
import shutil
import tarfile
import tomllib
from build import ROOT, stage


def main():
    meta = tomllib.loads((ROOT / "typst.toml").read_text())["package"]
    stage_root = stage() / "preview" / meta["name"] / meta["version"]
    assert (stage_root / "thumbnail.png").exists(), "Run make thumbnail first"
    target = ROOT / "dist" / "packages" / "preview" / meta["name"] / meta["version"]
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(stage_root, target)
    archive = ROOT / "dist" / f"{meta['name']}-{meta['version']}.tar.gz"
    with tarfile.open(archive, "w:gz") as output:
        for source in sorted(target.rglob("*")):
            if source.is_file():
                output.add(source, arcname=str(source.relative_to(target)))
    print(f"Universe submission directory: {target}")
    print(f"Package archive: {archive} ({archive.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
