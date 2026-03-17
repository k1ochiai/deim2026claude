"""
inject_papers.py
papers.json の論文リストを読み込み、index.html の Publications セクションに反映する。
"""

import json
import re
from pathlib import Path

PAPERS_JSON = Path("papers.json")
INDEX_HTML  = Path("index.html")
TARGET_NAME = "Keiichi Ochiai"   # 太字にする著者名


def build_pub_html(paper: dict) -> str:
    title   = paper.get("title", "")
    authors = paper.get("authors", "")
    venue   = paper.get("journal") or paper.get("conference") or ""

    # TARGET_NAME を <strong> でハイライト
    authors_html = authors.replace(TARGET_NAME, f"<strong>{TARGET_NAME}</strong>")

    return (
        '    <div class="pub">\n'
        '      <div class="pub-thumb">📄</div>\n'
        '      <div class="pub-info">\n'
        f'        <div class="pub-title">{title}</div>\n'
        f'        <div class="pub-authors">{authors_html}</div>\n'
        f'        <div class="pub-venue">{venue}</div>\n'
        '      </div>\n'
        '    </div>\n'
    )


def main():
    papers = json.loads(PAPERS_JSON.read_text(encoding="utf-8"))
    pubs_html = "\n" + "".join(build_pub_html(p) for p in papers)

    html = INDEX_HTML.read_text(encoding="utf-8")

    # <h2>Publications</h2> から </section> の直前までを置換
    pattern = r'(<h2>Publications</h2>).*?(  </section>)'
    replacement = r'\1\n' + pubs_html + r'\2'
    new_html, count = re.subn(pattern, replacement, html, flags=re.DOTALL)

    if count == 0:
        print("ERROR: Publications セクションが見つかりませんでした。")
        return

    INDEX_HTML.write_text(new_html, encoding="utf-8")
    print(f"OK: {len(papers)} 件の論文を index.html に反映しました。")


if __name__ == "__main__":
    main()
