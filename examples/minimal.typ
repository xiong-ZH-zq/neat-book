#import "../lib.typ": *
#show: neat-book.with(title: "我的第一本书", author: "作者", date: none)

= 开始
#introduction[本章介绍最小可用写法。]
#theorem(title: "一个结论")[若 $a=b$，则 $a+1=b+1$。] <simple>
#proof[在等式两端同时加上 $1$。]
#example[这是无标题例题。]
#solution[直接代入即可。]

== 一节
=== 一个小节
参见 @simple。
$ E = m c^2. $
