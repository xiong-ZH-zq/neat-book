#!/usr/bin/env python3
"""Compile user-facing entrypoints and test numbering and reference contracts."""
from pathlib import Path
import json
import re
import shutil
import subprocess
import tomllib

from build import ROOT, BUILD, stage


def capture(*args):
    result = subprocess.run([str(arg) for arg in args], cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        raise AssertionError(result.stderr)
    if "warning:" in result.stderr:
        raise AssertionError(result.stderr)
    return result.stdout


def compact(text):
    return re.sub(r"\s+", "", text).replace("\u2060", "").replace("\ufeff", "")


def main():
    package_path = stage()
    manifest = tomllib.loads((ROOT / "typst.toml").read_text())
    for key in ("name", "version", "entrypoint", "authors", "license", "description", "compiler"):
        assert manifest["package"][key], key
    assert manifest["package"]["license"] == "MIT"
    assert (ROOT / manifest["package"]["entrypoint"]).is_file()
    assert '@preview/neat-book:0.1.0' in (ROOT / "template/main.typ").read_text()

    documents = ("template/main.typ", "examples/minimal.typ", "tests/contracts.typ",
                 "tests/stress.typ", "tests/japanese.typ")
    for source in documents:
        name = "neat-book" if source == "template/main.typ" else Path(source).stem
        capture("typst", "compile", "--root", ROOT, "--package-path", package_path,
                ROOT / source, BUILD / f"{name}.pdf")
        print(f"PASS compile {source}")

    text = compact(capture("pdftotext", "-layout", BUILD / "contracts.pdf", "-"))
    for expected in (
        "BACK-EQ:Equation(1.1)", "BACK-SECOND-EQ:Equation(2.1)",
        "BACK-ALG:Algorithm1.1", "BACK-THM:Theorem1.1",
        "SELF-EQ:Equation(A.1)", "NEXT-EQ:Equation(B.1)",
        "ALPHA-EQ:Equation(A.1)", "SELF-BETA-EQ:Equation(B.1)",
        "FORWARD-EQ:Equation(A.1)", "FORWARD-ALG:AlgorithmA.1",
        "FORWARD-THM:TheoremA.1", "NO-SUPP-EQ:(1.1)",
        "CUSTOM-EQ:Eq.(1.1)", "FIRST-EQ:Equation(1.1)",
        "FIRST-FIG:Figure1.1", "FIRST-TABLE:Table1.1",
        "FIRST-CHAPTER:Chapter1", "FORWARD-APPENDIX:AppendixA",
        "Theorem2.1", "TheoremB.1", "Python", "Rust", "unknown-language",
        "(Knuth1997)",
        "Algorithm1.1Firstalgorithm", "Algorithm2.1Secondalgorithm", "AlgorithmA.1Appendixalgorithm",
    ):
        assert expected in text, f"Missing or incorrect rendered contract: {expected}"
    assert text.count("□") == 5, f"Expected five QEDs, got {text.count('□')}"
    assert text.index("References") < text.index("Appendixalpha")
    assert "STRESS-END" in capture("pdftotext", BUILD / "stress.pdf", "-")
    print("PASS rendered references, chapter resets, appendix order, five QED endings, code languages")

    # Check the actual CLI init workflow, outside the package's project root.
    project = BUILD / "initialized-book"
    if project.exists():
        shutil.rmtree(project)
    capture("typst", "init", "--package-path", package_path,
            "@preview/neat-book:0.1.0", project)
    capture("typst", "compile", "--root", project, "--package-path", package_path,
            project / "main.typ", BUILD / "initialized.pdf")
    print("PASS typst init and independent-project compilation")

    headings = json.loads(capture("typst", "eval", "--in", ROOT / "template/main.typ",
        "--root", ROOT, "--package-path", package_path,
        'query(heading).map(it => (level: it.level, numbering: repr(it.numbering)))'))
    assert {1, 2, 3}.issubset({item["level"] for item in headings})
    print("PASS three heading levels and package manifest")


if __name__ == "__main__":
    main()
