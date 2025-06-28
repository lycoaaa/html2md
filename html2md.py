import os
import re
import sys
from pathlib import Path
from typing import List, Tuple
from bs4 import BeautifulSoup, NavigableString, Tag

# ---------- 基础映射 ----------
_HEADING_TAGS = {"h1": "#", "h2": "##", "h3": "###", "h4": "####", "h5": "#####", "h6": "######"}

def _escape_md(text: str) -> str:
    """转义 Markdown 特殊字符"""
    return re.sub(r"([\\`*_{}\[\]()#+\-!|>])", r"\\\1", text)

def _process_inline(el: Tag) -> str:
    """递归处理内联元素，返回 Markdown 文本"""
    if isinstance(el, NavigableString):
        return _escape_md(str(el))
    if not isinstance(el, Tag):
        return ""
    name = el.name.lower()

    if name in ("strong", "b"):
        return f"**{''.join(_process_inline(c) for c in el.children)}**"
    if name in ("em", "i"):
        return f"*{''.join(_process_inline(c) for c in el.children)}*"
    if name == "code":
        return f"`{''.join(_process_inline(c) for c in el.children)}`"
    if name == "a":
        href = el.get("href", "#")
        text = ''.join(_process_inline(c) for c in el.children) or href
        return f"[{text}]({href})"
    if name == "img":
        alt = el.get("alt", "")
        src = el.get("src", "")
        return f"![{alt}]({src})"
    return ''.join(_process_inline(c) for c in el.children)

def _list_prefix(tag: Tag, index: int) -> str:
    return f"{index + 1}." if tag.name.lower() == "ol" else "-"

class HTMLConverter:
    def __init__(self, html_path: Path, md_path: Path):
        self.html_path = html_path
        self.md_path = md_path
        self.soup = BeautifulSoup(self.html_path.read_text(encoding="utf-8"), "lxml")
        for script in self.soup(["script", "style"]):
            script.decompose()

    # ----- 主流程 -----
    def convert(self):
        md_lines = []
        for element in self.soup.body.children:
            self._element_to_md(element, md_lines, 0)

        self.md_path.write_text("\n".join(md_lines), encoding="utf-8")
        print(f"转换完成:{self.md_path}")

    # ----- 核心递归 -----
    def _element_to_md(self, el, out: List[str], indent: int):
        if isinstance(el, NavigableString):
            text = str(el).strip()
            if text:
                out.append(" " * indent + _escape_md(text))
            return
        if not isinstance(el, Tag):
            return

        name = el.name.lower()
        if name in _HEADING_TAGS:
            prefix = _HEADING_TAGS[name]
            content = ''.join(_process_inline(c) for c in el.children).strip()
            out.append(f"{prefix} {content}\n")
        elif name == "p":
            para = ''.join(_process_inline(c) for c in el.children).strip()
            if para:
                out.append(" " * indent + para + "\n")
        elif name in ("ul", "ol"):
            for idx, li in enumerate(el.find_all("li", recursive=False)):
                prefix = _list_prefix(el, idx)
                out.append(" " * indent + f"{prefix} {''.join(_process_inline(c) for c in li.contents).strip()}")
                for child in li.find_all(("ul", "ol"), recursive=False):
                    self._element_to_md(child, out, indent + 2)
            out.append("")
        elif name == "pre":
            code_tag = el.find("code")
            code_lang = code_tag.get("class", [""])[0].replace("language-", "") if code_tag else ""
            code_content = code_tag.get_text() if code_tag else el.get_text()
            out.append(f"```{code_lang}")
            out.append(code_content.rstrip())
            out.append("```")
            out.append("")
        elif name == "table":
            self._table_to_md(el, out)
            out.append("")
        else:
            for child in el.children:
                self._element_to_md(child, out, indent)

    def _table_to_md(self, table: Tag, out: List[str]):
        """
        将 HTML 表格转换为 Markdown 表格
        """
        rows = []
        for tr in table.find_all("tr"):
            cols = [ _process_inline(td).strip() for td in tr.find_all(("td", "th")) ]
            if cols:
                rows.append(cols)
        if not rows:
            return
        # 规范列数
        col_count = max(len(r) for r in rows)
        for r in rows:
            r.extend([""] * (col_count - len(r)))
        # 表头分隔
        header = "| " + " | ".join(rows[0]) + " |"
        splitter = "| " + " | ".join(["---"] * col_count) + " |"
        out.append(header)
        out.append(splitter)
        for r in rows[1:]:
            out.append("| " + " | ".join(r) + " |")
