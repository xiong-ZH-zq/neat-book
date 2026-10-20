# 发布 Neat Book 到 Typst Universe

当前版本：0.1.0。当前状态：本地实现与验证，尚未向 Universe 或远程 Git 仓库提交。

## 提交前的元数据

1. 确认 `neat-book` 在 Universe 和待审 PR 中可用；如需改名，同时更改 manifest、全部版本化导入和脚本中的测试字符串。
2. `typst.toml` 的 `authors = ["xzqbear"]` 与 LICENSE 当前使用工作区用户名。正式提交时确认署名，可补充 `<@github-handle>`。
3. 创建真实仓库后，在 manifest 添加 `repository = "https://github.com/实际用户/实际仓库"`。当前有意省略，避免虚构地址。
4. 确认版权年份和 MIT 许可符合作者意愿。

## 验证与打包

```sh
make test
make thumbnail
python3 scripts/package.py
```

将生成：

- `build/neat-book.pdf`：完整示例书。
- `thumbnail.png`：模板初始化后封面的 PNG，150 PPI，长边大于 1080 px。
- `dist/packages/preview/neat-book/0.1.0/`：可复制到官方包仓库的目录。
- `dist/neat-book-0.1.0.tar.gz`：不包含依赖源代码和构建产物的包归档。

发布包显式包含 `lib.typ`、`src/`、`template/`、`typst.toml`、`README.md`、`LICENSE`、`thumbnail.png`。
模板主入口及所有章节均使用 `@preview/neat-book:0.1.0` 导入；初始化得到的项目可独立编译。
字体通过系统或项目安装，不捆绑大型字体文件。

官方检查器尚未安装在本工作区，本地 `make test` 不等于官方检查器通过。
正式提交前根据 [官方安装方法](https://github.com/typst/package-check) 安装并运行：

```sh
cargo install --git https://github.com/typst/package-check.git
cd dist/packages/preview/neat-book/0.1.0
typst-package-check check
```

若检查器需要本地包仓库，使用其官方文档中在 `typst/packages/packages` 下运行
`typst-package-check check @preview/neat-book:0.1.0` 的方式。
需要 CJK 字体的模板还应在 Typst 网页项目中验证字体可用性，必要时按 README 上传字体。

## 提交

按 [官方提交指南](https://github.com/typst/packages/tree/main/docs) fork `typst/packages`，
把上述目录放到 `packages/preview/neat-book/0.1.0/`，提交 PR。
PR 中说明原创设计、ElegantBook 的视觉参考、依赖、最低编译器版本与字体要求。
仓库中的 `make package` 仅准备本地文件，不执行上传。

更新版本时同步 `typst.toml`、`template/**/*.typ`、README、测试和变更日志中的版本号。
已发布版本应保持不变，修正通过新版本提交。
