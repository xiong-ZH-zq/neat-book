#import "../lib.typ": *
#show: neat-book.with(
  title: "CJK italic regression", cover: false, toc: false,
  cjk-oblique: if sys.inputs.at("native", default: "false") == "true" { none } else { 12deg },
)
#set page(width: 90mm, height: auto, margin: 12pt, header: none, footer: none)
#set par(first-line-indent: 0pt)

// Repeat identical characters to check glyph reuse, weight and affine slant.
#block[中]
#block[_中_]
#block[*中*]
#block[*_中_*]
#block[#emph[中 #emph[中] 中]]
#block[#ja[_日あア_]]
#block[#ko[_한글_]]
#block[#en[Regular _Italic_ *_Bold Italic_*]]

// Long CJK emphasis must wrap inside the narrow page rather than overflow.
_这是用于检查中文斜体自动换行的长句。重复书写以跨越多行，保证逐字倾斜后仍然可以正确换行。_
