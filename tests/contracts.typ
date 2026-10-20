#import "../lib.typ": *
#show: neat-book.with(
  title: "Contract tests", author: "Neat Book", lang: "en",
  cover: false, toc: false,
  fonts: (english: "Noto Serif", mono: "Noto Sans Mono"),
  references: bibliography("../template/references.bib", title: [References]),
  appendix: [
    = Appendix alpha <appendix-a>
    $ a = a $ <eq-a>
    #theorem(title: "Appendix theorem")[Alpha.] <thm-a>
    #algorithm(title: "Appendix algorithm", { import algorithmic: *; Return[$a$] }) <alg-a>
    BACK-EQ: @eq-first.
    BACK-SECOND-EQ: @eq-second.
    BACK-ALG: @alg-first.
    BACK-THM: @thm-first.
    SELF-EQ: @eq-a.
    NEXT-EQ: @eq-b.
    = Appendix beta
    $ b = b $ <eq-b>
    #theorem[Beta.] <thm-b>
    ALPHA-EQ: @eq-a.
    SELF-BETA-EQ: @eq-b.
  ],
)

#outline(target: figure.where(kind: "algorithm"), title: [Algorithms])

= First chapter <chapter-first>
#introduction[An overview with *bold*, _italic_, $x$ and a list:
  - English.
  - #zh[中文粗体：*字体*。] #ja[日本語の*字体*。] #ko[한국어。]
]

== Section
=== Subsection
==== Unlisted fourth level

#theorem(title: "Named")[Content.] <thm-first>
#theorem[Unnamed.]
#definition(title: "Definition")[Content.]
#example[Content.]
#lemma[Content.]
#proposition[Content.]
#corollary[Content.]
#axiom[Content.]
#postulate[Content.]
#assumption[Content.]
#property[Content.]
#conjecture[Content.]
#remark[Content.]
#note[Content.]
#exercise[Content.]
#problem[Content.]
#note-block[Note.]
#tip-block[Tip.]
#important-block[Important.]
#warning-block[Warning.]
#caution-block[Caution.]
#remark-block[Remark.]
#quote-block[Quote.]
#emph-block[Emphasis.]
#theorem(numbering: none, outlined: false)[Unnumbered.]
#theorion.theorion-restate(filter: <thm-first>)
#proof[Text proof ending.]
#solution[Text solution ending.]
#conclusion[Text conclusion ending.]
#proof[
  #set math.equation(numbering: none)
  Equation ending:
  $ x = x $
]
#solution[
  - First item.
  - Last item. #qedhere
]

$ x = 1 $ <eq-first>
$ x = 2 $ <eq-first-two>
#algorithm(title: "First algorithm", input: [$x$], output: [$x$], {
  import algorithmic: *
  IfElseChain($x > 0$, { Assign[$x$][$x - 1$] }, Return[$0$])
  For($i in {1, 2, 3}$, { Line[Visit $i$.] })
  Return[$x$]
}) <alg-first>

#figure(image("../template/assets/logo.svg", width: 12mm), caption: [An image]) <fig-first>
#figure(table(columns: 2, [a], [b]), caption: [A table]) <table-first>
FORWARD-EQ: @eq-a.
FORWARD-ALG: @alg-a.
FORWARD-THM: @thm-a.
NO-SUPP-EQ: #ref(<eq-first>, supplement: none).
CUSTOM-EQ: @eq-first[Eq.].
PAGE-REF: #ref(<eq-first>, form: "page").
See @knuth1997.

```python
def square(x):
    return x * x
```
#codeblock("fn main() {}", lang: "rust")
#codeblock("an unknown language", lang: "unknown-language")

= Second chapter
$ y = 1 $ <eq-second>
#theorem[Chapter two.] <thm-second>
#algorithm(title: "Second algorithm", { import algorithmic: *; Return[$y$] })
FIRST-EQ: @eq-first.
FIRST-FIG: @fig-first.
FIRST-TABLE: @table-first.
FIRST-CHAPTER: @chapter-first.
FORWARD-APPENDIX: @appendix-a.

#context {
  let expected = ((<eq-first>, 1), (<eq-first-two>, 2), (<eq-second>, 1), (<eq-a>, 1), (<eq-b>, 1))
  for (target, value) in expected {
    assert.eq(counter(math.equation).at(target), (value,))
  }
  assert.eq(outline.depth, 3)
}
