/// Open fonts. Install locally or upload them to the Typst web project.
#let default-fonts = (
  english: "Libertinus Serif",
  chinese: "Noto Serif CJK SC",
  japanese: "Noto Serif CJK JP",
  korean: "Noto Serif CJK KR",
  mono: "DejaVu Sans Mono",
  sans: "Noto Sans CJK SC",
  math: "New Computer Modern Math",
)
#let book-fonts = state("neat-book.fonts", default-fonts)
#let font-list(value) = if type(value) == array { value } else { (value,) }

// Explicit language spans also choose the correct regional Han glyphs.
#let language-span(key, lang, body) = context {
  let fonts = book-fonts.get()
  set text(font: font-list(fonts.at(key)) + font-list(fonts.english), lang: lang)
  body
}
/// Chinese text with the configured Chinese font.
#let zh(body) = language-span("chinese", "zh", body)
/// English text with the configured Latin font.
#let en(body) = language-span("english", "en", body)
/// Japanese text, including Japanese variants of shared Han characters.
#let ja(body) = language-span("japanese", "ja", body)
/// Korean text with the configured Korean font.
#let ko(body) = language-span("korean", "ko", body)
