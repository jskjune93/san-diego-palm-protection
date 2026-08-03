from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import json

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "site-config" / "ufmp_resource.json"
OUTPUT = ROOT / "old-escondido-urban-forest-documentation.pdf"
MANIFEST = ROOT / "proof-data" / "approved" / "old-escondido-urban-forest-documentation.json"
IMAGE_DIR = ROOT / "images" / "old-escondido-urban-forest-documentation"

GREEN = colors.HexColor("#073d2b")
GOLD = colors.HexColor("#ffb31a")
INK = colors.HexColor("#16221d")
MUTED = colors.HexColor("#57635e")
PAPER = colors.HexColor("#fffdf8")


def draw_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
    canvas.setStrokeColor(colors.HexColor("#d8d3c6"))
    canvas.line(0.65 * inch, 0.42 * inch, letter[0] - 0.65 * inch, 0.42 * inch)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(0.65 * inch, 0.25 * inch, "San Diego Palm Protection | Independent civic documentation")
    canvas.drawRightString(letter[0] - 0.65 * inch, 0.25 * inch, f"Page {doc.page}")
    canvas.restoreState()


def fitted_image(path: Path, max_width: float, max_height: float) -> Image:
    with PILImage.open(path) as source:
        width, height = source.size
    scale = min(max_width / width, max_height / height)
    return Image(str(path), width=width * scale, height=height * scale)


def build_story(resource: dict) -> list:
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitleSDPP", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=27, leading=31, textColor=GREEN, spaceAfter=18,
    ))
    styles.add(ParagraphStyle(
        name="DeckSDPP", parent=styles["BodyText"], fontSize=12.5,
        leading=18, textColor=INK, spaceAfter=16,
    ))
    styles.add(ParagraphStyle(
        name="HeadingSDPP", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=16, leading=20, textColor=GREEN, spaceBefore=10, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="BodySDPP", parent=styles["BodyText"], fontSize=10.5,
        leading=15.5, textColor=INK, spaceAfter=9,
    ))
    styles.add(ParagraphStyle(
        name="CaptionSDPP", parent=styles["BodyText"], fontSize=9,
        leading=13, textColor=MUTED, spaceBefore=8,
    ))

    story: list = [
        Spacer(1, 0.45 * inch),
        Paragraph("SAN DIEGO PALM PROTECTION", styles["HeadingSDPP"]),
        Spacer(1, 0.1 * inch),
        Paragraph(resource["title"], styles["TitleSDPP"]),
        Paragraph(resource["summary"], styles["DeckSDPP"]),
        Spacer(1, 0.08 * inch),
        Paragraph("Independent Old Escondido palm documentation", styles["HeadingSDPP"]),
        Paragraph(
            "A limited owner/SDPP record. No City of Escondido endorsement, partnership, selection, approval, adoption, affiliation, or authority is claimed.",
            styles["BodySDPP"],
        ),
        PageBreak(),
    ]

    for section in resource["sections"]:
        story.append(Paragraph(section["heading"], styles["HeadingSDPP"]))
        story.append(Paragraph(section["body"], styles["BodySDPP"]))
    story.append(Spacer(1, 0.08 * inch))
    story.append(Paragraph(
        '<link href="https://www.sandiegopalmprotection.com/urban-forest-palm-documentation.html" color="#073d2b"><u>Read the current website resource</u></link>',
        styles["BodySDPP"],
    ))

    for item in resource["media"]:
        path = IMAGE_DIR / item["filename"]
        if not path.is_file():
            raise FileNotFoundError(path)
        story.extend([
            PageBreak(),
            Paragraph(item["caption"], styles["HeadingSDPP"]),
            Spacer(1, 0.12 * inch),
            fitted_image(path, 7.0 * inch, 7.15 * inch),
            Paragraph(item["alt"], styles["CaptionSDPP"]),
        ])
    return story


def main() -> None:
    resource = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter, leftMargin=0.65 * inch, rightMargin=0.65 * inch,
        topMargin=0.62 * inch, bottomMargin=0.58 * inch,
        title=resource["title"], author="San Diego Palm Protection",
        subject=resource["summary"], creator="San Diego Palm Protection",
    )
    document.build(build_story(resource), onFirstPage=draw_page, onLaterPages=draw_page)

    digest = sha256(OUTPUT.read_bytes()).hexdigest()
    resource["pdf"]["sha256"] = digest
    resource["pdf"]["page_count"] = 2 + len(resource["media"])
    CONFIG_PATH.write_text(json.dumps(resource, indent=2) + "\n", encoding="utf-8")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["artifact_fingerprint"] = digest
    manifest["approved_fingerprint"] = digest
    manifest["content"]["page_count"] = resource["pdf"]["page_count"]
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Built {OUTPUT.name}")
    print(f"pages={resource['pdf']['page_count']} sha256={digest}")


if __name__ == "__main__":
    main()
