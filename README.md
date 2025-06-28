# html2md

**html2md** 是一个零依赖的纯 Python 脚本，用于把常见 HTML 文件转换为干净、可读性强的 Markdown。（作者本人主要是为了生成输入给大模型的干净Markdown数据源）

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

> 欢迎在使用过程中提出 issue 或 PR，共同完善 html2md。
