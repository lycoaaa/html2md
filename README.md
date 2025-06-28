# html2md

**html2md** 是一个零依赖（除了解析器）的纯 Python 脚本，用于把常见 HTML 文件转换为干净、可读性强的 Markdown。它在内部利用 BeautifulSoup 和 lxml 解析 HTML，并按规则重建标题、段落、列表、代码块、表格等结构，从而最大限度地保留原始文档的语义与排版。

---

## 特性

* **语义级标题映射**：将 `<h1>`‒`<h6>` 转换为 `#`‒`######`⁠，保持层级清晰。
* **内联样式还原**：粗体、斜体、行内代码、超链接与图片均能正确输出对应的 Markdown 语法。
* **有序 / 无序列表支持**：自动处理嵌套列表，使用缩进维持层级；有序列表序号会递增，无序列表统一为短横线 `-`⁠ 。
* **代码块检测**：对 `<pre><code>` 片段保留原有语言 class（如 `language-python`）并包裹在三反引号中。
* **表格转换**：将 `<table>` 生成对齐良好的管道表，自动补齐列数，首行作为表头。
* **噪声清理**：脚本 / 样式标签在加载阶段即被移除，保证结果纯净和体积最小化。

---

## 安装

```bash
# 建议使用虚拟环境
pip install beautifulsoup4 lxml
```

脚本本身无额外依赖；如需打包或在 CI 中使用，只需确保以上两库可用。

---

## 快速上手

### 1. 命令行

```bash
python html2md.py input.html output.md
# 成功后会在控制台看到 “转换完成: output.md”
```

不提供 output 参数时，脚本会将结果写到与 输入同名、后缀为 `.md` 的文件中。

### 2. 作为模块调用

```python
from pathlib import Path
from html2md import HTMLConverter

HTMLConverter(
    html_path=Path("example.html"),
    md_path  =Path("example.md")
).convert()
```

---

## 目录结构

```
html2md.py         # 主脚本 / 模块，包含转换核心逻辑
README.md          # 使用说明（本文件）
```

（如需集成到更大的项目，可将 `HTMLConverter` 类直接拷贝或通过 pip 内嵌发布。）

---

## 使用小贴士

1. **字符编码**：脚本默认以 UTF-8 读取 HTML 并写入 Markdown；若源文件编码不同，请先自行转换字符集。
2. **语言高亮**：代码块语言取自 `<code class="language-xxx">` ；无 class 时会留下空语言标记，可在后期手动补全。
3. **复杂样式**：对 CSS 布局、行内样式、iframe 等深度依赖样式的片段，本工具只保留纯文本语义，渲染效果可能简化。
4. **表格合并单元格**：`rowspan` / `colspan` 目前按照展开后逐行逐列写入，未特别处理视觉对齐，可按需手工调整。

---

## 许可证

项目暂未指定许可证；若需在生产环境或开源项目中使用，请按实际情况补充 LICENSE 文件并注明出处。

---

> 欢迎在使用过程中提出 issue 或 PR，共同完善 html2md。
