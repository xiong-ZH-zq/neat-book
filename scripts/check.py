#!/usr/bin/env python3
"""Compile user-facing entrypoints and test numbering and reference contracts."""
from pathlib import Path
import json
import re
import shutil
import subprocess
import tomllib
import xml.etree.ElementTree as ET

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


def check_cjk_italics(package_path):
    """Inspect actual vector transforms and glyphs, not just successful compilation."""
    outputs = []
    for native in (False, True):
        output = BUILD / ("cjk-native.svg" if native else "cjk-italics.svg")
        capture("typst", "compile", "--root", ROOT, "--package-path", package_path,
                "--input", f"native={str(native).lower()}", "--format", "svg",
                ROOT / "tests/cjk-italics.typ", output)
        root = ET.parse(output).getroot()
        runs = []
        for el in root.iter():
            transform = el.get("transform", "")
            if transform.startswith("matrix(") and len(el):
                matrix = [float(n) for n in transform[7:-1].split()]
                glyphs = [child.get("{http://www.w3.org/1999/xlink}href") for child in el]
                runs.append((matrix, glyphs))
        assert len(runs) >= 4
        outputs.append(runs)
    synthesized, native = outputs
    # First four runs: upright, oblique, bold, bold oblique of the same Han glyph.
    assert abs(synthesized[0][0][2]) < 1e-6
    assert synthesized[1][0][2] > .2
    assert abs(synthesized[2][0][2]) < 1e-6
    assert synthesized[3][0][2] > .2
    assert synthesized[0][1] == synthesized[1][1], "Oblique must retain the regular font"
    assert synthesized[2][1] == synthesized[3][1], "Bold oblique must retain the bold font"
    assert synthesized[0][1] != synthesized[2][1], "Bold must use a different glyph"
    assert all(abs(matrix[2]) < 1e-6 for matrix, _ in native), "Disabling synthesis must remove shear"
    # Nested emphasis restores upright text between two oblique Han characters.
    assert synthesized[4][0][2] > .2
    assert abs(synthesized[5][0][2]) < 1e-6
    assert synthesized[6][0][2] > .2
    print("PASS rendered CJK oblique, bold oblique, nested emphasis and synthesis opt-out")


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
    check_cjk_italics(package_path)


if __name__ == "__main__":
    main()
