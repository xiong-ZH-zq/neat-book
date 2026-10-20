#import "../lib.typ": *
#show: neat-book.with(title: "Long content", cover: false, toc: false)

= 跨页排版
#introduction[
  #for n in range(18) { [本章提要 #n。] + parbreak() }
]

// Opt in to page breaks for environments larger than a page.
#theorem(breakable: true, title: "跨越多页的定理")[
  #for n in range(60) {
    [这是定理正文的第 #n 段。长框应跨页，正文不应超出页面边界。]
    parbreak()
  }
]
#proof[
  #for n in range(45) { [证明步骤 #n：根据前述定义，结论成立。] + parbreak() }
]

// Codly 2 uses scoped show rules; keep long code blocks breakable.
#show: codly.set_(breakable: true)
#codeblock(range(85).map(n => "print(" + str(n) + ")").join("\n"), lang: "python")

#algorithm(title: "Long algorithm", {
  import algorithmic: *
  for n in range(65) { Line[Step #n.] }
})
STRESS-END
