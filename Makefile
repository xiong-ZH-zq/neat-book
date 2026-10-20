.PHONY: build preview test thumbnail package
build:
	python3 scripts/build.py
preview: build
	typst watch --root . --package-path build/packages template/main.typ build/neat-book.pdf
test:
	python3 scripts/check.py
thumbnail:
	python3 scripts/build.py --thumbnail
package: test thumbnail
	python3 scripts/package.py
