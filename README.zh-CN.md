# LaTeX 论文模板

[English](README.md) | [中文](README.zh-CN.md)

这是 DeePTB-Lab 使用的可复用 LaTeX 论文模板仓库。

本仓库用于作为科研写作项目的起点，包含 REVTeX 4.2 论文骨架、参考文献和图片约定、本地构建命令，以及用于检查常见 LaTeX 和 BibTeX 问题的 pull request 自动检查。

## 仓库结构

- `main.tex`：论文主源文件。
- `ref.bib`：参考文献数据库。
- `figs/`：`main.tex` 引用的图片资源。
- `Makefile`：本地构建入口和 TeX engine 选择。
- `.latexmkrc`：共享的 `latexmk` 默认配置。
- `scripts/detect_tex_engine.py`：`make` 使用的 TeX engine 自动检测脚本。
- `scripts/check_bib.py`：本地和 CI 使用的 BibTeX 重复条目检查脚本。
- `scripts/check_author_comments.py`：临时作者批注检查脚本。
- `scripts/check_latex_log.py`：未解析引用和引用文献的 LaTeX 日志检查脚本。
- `.github/workflows/latex.yml`：push 和 pull request 检查，并上传 PDF artifact。

## 构建

安装包含 `latexmk`、所需 TeX engine、所需宏包和 REVTeX 4.2 类的 TeX 发行版，然后运行：

```sh
make
```

常用命令：

```sh
make                  # 编译 main.tex -> main.pdf
make check            # 检查参考文献、作者批注、编译结果和日志
make check-bib        # 检查重复 BibTeX 条目
make check-comments   # 检查未清理的临时作者批注
make watch            # 源文件变化时自动重新编译
make clean            # 删除 LaTeX 中间文件
make distclean        # 删除中间文件和 main.pdf
```

Makefile 会根据 `main.tex` 自动检测 TeX engine：CJK 文本、`ctex`、`xeCJK` 或 `fontspec` 会选择 XeLaTeX；LuaLaTeX 专用宏包会选择 LuaLaTeX；否则默认使用 pdfLaTeX。必要时可以手动覆盖：

```sh
make ENGINE=xelatex
make ENGINE=pdflatex
make ENGINE=lualatex
```

当前示例使用 `ctex` 和中文文本，因此会自动使用 XeLaTeX 构建。

## 使用这个模板

本仓库推荐采用“一篇论文一个 GitHub 仓库”的方式组织协作写作。新论文使用 GitHub template repository 创建；已有论文仓库只导入共享基础设施。

### 创建新的论文仓库

推荐先在本仓库 GitHub 设置中启用 **Template repository**，以后每篇新论文都通过 **Use this template** 创建仓库。

创建新的论文仓库后：

1. 替换 `main.tex` 中的示例内容。
2. 替换或扩展 `ref.bib` 中的参考文献。
3. 用实际论文图片替换 `figs/placeholder.pdf`，图片统一放在 `figs/` 下。
4. 重写 README，让它描述具体论文，而不是模板本身。
5. 第一次打开 pull request 前运行 `make check`。

模板复制过去的共享基础设施包括 `.github/`、`scripts/`、`.latexmkrc`、`Makefile`、`.gitignore` 和 `.editorconfig`。

### 给已有论文仓库添加模板基础设施

对于已有论文仓库，不要从本地模板仓库手动复制文件。推荐把模板仓库临时加为 remote，只导入共享基础设施：

```sh
git remote add template https://github.com/DeePTB-Lab/latex-manuscript-template.git
git fetch template
git checkout template/main -- .github scripts .latexmkrc .gitignore .editorconfig
git remote remove template
```

这样会避免覆盖文章相关文件，例如 `main.tex`、`ref.bib`、`figs/` 和论文自己的 README。

如果已有论文仓库没有 `Makefile`，也可以导入模板中的 Makefile：

```sh
git checkout template/main -- Makefile
```

如果已有论文仓库已经有自己的 `Makefile`，请手动合并相关 target，不要直接覆盖。

## Pull Request 检查

Pull request 会运行 `LaTeX` GitHub Actions workflow。该 workflow 执行：

```sh
make check
```

它会检查：

- 参考文献中没有重复 key；
- 参考文献中没有相同 DOI 或 title/year 的疑似重复条目；
- 正文中没有残留 `\ZH{}`、`\LZ{}`、`\TODO{}`、`\todo{}` 等临时作者批注；
- `main.tex` 能通过 `latexmk` 使用自动检测或显式指定的 TeX engine 编译；
- `.latexmkrc` 启用 `-halt-on-error`，LaTeX 语法错误会导致编译停止；
- 未解析的引用、未解析的文献引用和选定的 BibTeX warning 会导致检查失败。

workflow 会在成功生成 `main.pdf` 时把它上传为 GitHub Actions artifact。打开或更新 pull request 前，请先在本地运行 `make check`。

## 版本控制说明

仓库会跟踪论文源文件、参考文献文件和图片源资源，例如 `figs/*.pdf`。生成的 LaTeX 文件，例如 `*.aux`、`*.bbl`、`*.log`、`*.synctex.gz` 和 `/main.pdf`，默认被忽略。

如果期刊投稿或 arXiv 打包需要提交生成文件，请在本地生成后用 `git add -f` 明确添加所需文件。

## 论文内容说明

当前 `main.tex` 包含模板文本、示例公式、占位引用和占位图片。正式投稿前请替换为具体论文内容。
