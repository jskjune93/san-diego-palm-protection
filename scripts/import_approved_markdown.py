#!/usr/bin/env python3
"""Mechanically import an approved Markdown artifact into Palm Journal sources."""
from __future__ import annotations

import argparse, html, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inline(text: str) -> str:
    value = html.escape(text)
    value = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", value)
    return value


def convert(markdown: str) -> tuple[dict[str, str], str, list[str]]:
    front, body = markdown.split("---", 2)[1:]
    metadata = {}
    for line in front.strip().splitlines():
        key, value = line.split(":", 1); metadata[key.strip()] = value.strip().strip('"')
    body = body.strip().replace("â€”", "—").replace("Â·", "·")
    body = body.replace("[Related monitoring entry — add published Palm Journal URL]", "[Related monitoring entry](./monitoring-mature-cidp-after-palm-weevil-activity.html)")
    body = body.replace("https://sandiegopalmprotection.com/palm-journal/documented-loss/", "../palm-journal/documented-loss/")
    body = body.replace("https://sandiegopalmprotection.com/palm-journal/", "../palm-journal-new.html")
    lines=body.splitlines(); out=[]; images=[]; paragraph=[]
    def flush():
        if paragraph: out.append("      <p>"+inline(" ".join(paragraph))+"</p>"); paragraph.clear()
    for line in lines:
        line=line.strip()
        if not line: flush(); continue
        if line == f"# {metadata['title']}": continue
        image=re.fullmatch(r"!\[(.*?)\]\((.*?)\)",line)
        if image:
            flush(); name=Path(image.group(2)).name; images.append(name)
            out.append(f'      <figure><img src="../images/las-palmas/{html.escape(name)}" alt="{html.escape(image.group(1))}" loading="lazy" decoding="async">')
            continue
        if line.startswith("*") and line.endswith("*") and out and out[-1].startswith("      <figure"):
            out.append(f'        <figcaption class="image-caption">{inline(line[1:-1])}</figcaption></figure>'); continue
        if line.startswith("## "): flush(); out.append(f"      <h2>{inline(line[3:])}</h2>"); continue
        paragraph.append(line)
    flush()
    return metadata,"\n".join(out)+"\n",images


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("markdown",type=Path); parser.add_argument("assets",type=Path); args=parser.parse_args()
    metadata,fragment,images=convert(args.markdown.read_text(encoding="utf-8"))
    slug="las-palmas-no-reply-then-the-saws"
    (ROOT/"journal-data/articles"/f"{slug}.html").write_text(fragment,encoding="utf-8")
    target=ROOT/"images/las-palmas"; target.mkdir(parents=True,exist_ok=True)
    for name in dict.fromkeys(images): shutil.copy2(args.assets/name,target/name)
    manifest=ROOT/"journal-data/journal_entries.json"; entries=json.loads(manifest.read_text(encoding="utf-8"))
    entries=[e for e in entries if e.get("slug")!=slug]
    entries.insert(0,{"slug":slug,"title":metadata["title"],"date":"2026-07-13","date_label":"Old Escondido | July 13, 2026","location":"Old Escondido","category":"Documented Loss","topic":"Las Palmas Canary Island date palm removal","excerpt":metadata["meta_description"],"page":True,"substantial":True,"review":"final owner-approved publication artifact","related":["monitoring-mature-cidp-after-palm-weevil-activity","old-escondido-cidp-collection"],"legacy_anchor":"las-palmas-documented-loss","status":"published","canonical_url":"https://www.sandiegopalmprotection.com/palm-journal/las-palmas-no-reply-then-the-saws.html","primary_image":"./images/las-palmas/01-property-context-laspalmas-escondido-cidp.jpg","primary_image_alt":"Las Palmas apartment frontage in Old Escondido with mature Canary Island date palms and property signage","gallery_images":[],"classification":"Documented Loss"})
    manifest.write_text(json.dumps(entries,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

if __name__=="__main__": main()
