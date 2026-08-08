#!/usr/bin/env python3
"""Build the canonical one-page SDPP commercial outreach PDF."""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "SDPP-Commercial-Palm-Stewardship.pdf"
HERO = ROOT / "Las Palmas_Appartments_Healthy-CIDP.jpg"
LOGO = ROOT / "logo.png"

GREEN = HexColor("#073b2b")
DARK = HexColor("#031d15")
GOLD = HexColor("#f4ae18")
CREAM = HexColor("#f7f3e9")
INK = HexColor("#14231d")
MUTED = HexColor("#52645c")
LINE = HexColor("#d9d2c3")


def wrap(text: str, font: str, size: float, width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(c: canvas.Canvas, text: str, x: float, y: float, width: float, *, font: str, size: float, leading: float, color=INK) -> float:
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_bullets(c: canvas.Canvas, items: list[str], x: float, y: float, width: float) -> float:
    for item in items:
        lines = wrap(item, "Helvetica", 8.5, width - 15)
        c.setFillColor(GOLD)
        c.circle(x + 3, y + 2.5, 2.1, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica", 8.5)
        for index, line in enumerate(lines):
            c.drawString(x + 13, y, line)
            y -= 10.7
        y -= 3
    return y


def crop_hero() -> Image.Image:
    image = Image.open(HERO).convert("RGB")
    target_ratio = 612 / 282
    ratio = image.width / image.height
    if ratio > target_ratio:
        width = int(image.height * target_ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = int(image.width / target_ratio)
        top = max(0, (image.height - height) // 2)
        image = image.crop((0, top, image.width, top + height))
    overlay = Image.new("RGB", image.size, "#031d15")
    return Image.blend(image, overlay, 0.64)


def build() -> None:
    c = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    c.setTitle("SDPP Commercial Palm Stewardship")
    c.setAuthor("San Diego Palm Protection")
    c.setSubject("Palm Portfolio Baseline and Annual Palm Stewardship Program")
    width, height = letter

    hero = crop_hero()
    c.drawImage(ImageReader(hero), 0, 510, width=width, height=282, preserveAspectRatio=False, mask="auto")
    c.drawImage(str(LOGO), 42, 737, width=38, height=38, preserveAspectRatio=True, mask="auto")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(91, 759, "SAN DIEGO PALM PROTECTION")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(42, 708, "OWNER-LED PALM PORTFOLIO STEWARDSHIP")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(42, 666, "Know each priority palm.")
    c.drawString(42, 632, "Keep the history. Plan what comes next.")
    draw_lines(
        c,
        "A palm-specific system for managed properties: stable identities, condition records, recurring planning, licensed treatment within scope, and coordinated response.",
        42, 596, 510, font="Helvetica", size=11.2, leading=15, color=white,
    )
    c.setFillColor(GOLD)
    c.rect(42, 535, 4, 38, fill=1, stroke=0)
    draw_lines(c, "Standardize the stewardship system; customize the property scope.", 57, 559, 500, font="Helvetica-Bold", size=10.2, leading=13, color=white)

    c.setFillColor(CREAM)
    c.rect(0, 0, width, 510, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(42, 482, "Two ways to engage")
    c.setFont("Helvetica", 9.6)
    c.setFillColor(MUTED)
    c.drawString(42, 465, "Begin with a defined baseline or establish the recurring annual relationship.")

    card_y, card_h, card_w, gap = 247, 202, 252, 24
    for x in (42, 42 + card_w + gap):
        c.setFillColor(white)
        c.setStrokeColor(LINE)
        c.rect(x, card_y, card_w, card_h, fill=1, stroke=1)
        c.setFillColor(GOLD)
        c.rect(x, card_y + card_h - 5, card_w, 5, fill=1, stroke=0)

    left_x = 56
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(left_x, 421, "Palm Portfolio Baseline")
    y = draw_lines(c, "A defined initial engagement for a property without an organized palm record.", left_x, 401, 222, font="Helvetica", size=9.1, leading=12, color=MUTED) - 5
    draw_bullets(c, [
        "Walkthrough, known-history intake, and priority-palm identities",
        "Baseline photographs and visible-condition records",
        "Immediate concerns and preservation priorities",
        "Recommended care, treatment, documentation, and coordination scope",
        "Property-specific proposal for continuing work",
    ], left_x, y, 222)

    right_x = 56 + card_w + gap
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(right_x, 421, "Annual Palm Stewardship Program")
    y = draw_lines(c, "The core recurring relationship, tailored to the palms and management responsibilities.", right_x, 401, 222, font="Helvetica", size=9.1, leading=12, color=MUTED) - 5
    draw_bullets(c, [
        "Maintained palm register and scheduled care visits",
        "Licensed preventive protection and treatment within scope",
        "Dated condition, treatment, and supplied work history",
        "Material-change alerts and preservation priorities",
        "Specialist coordination, portfolio summary, and next-cycle planning",
    ], right_x, y, 222)

    c.setFillColor(GREEN)
    c.rect(42, 176, 528, 54, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 12.2)
    c.drawCentredString(306, 207, "Our goal is to preserve the value of your mature landscape assets.")
    c.setFont("Helvetica", 9.2)
    c.drawCentredString(306, 190, "The baseline can stand alone or become the foundation for annual stewardship.")

    c.setFillColor(GOLD)
    c.roundRect(42, 97, 244, 48, 2, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(164, 116, "Request a Property Walkthrough")
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(312, 132, "sandiegopalmprotection.com")
    c.setFont("Helvetica", 10)
    c.drawString(312, 115, "Call or text 262-492-3135")
    c.drawString(312, 99, "San Diego County")

    c.setStrokeColor(LINE)
    c.line(42, 77, 570, 77)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8.7)
    c.drawCentredString(306, 58, "California Qualified Applicator License No. 175295  |  Category B - Landscape Maintenance  |  Insured")
    c.setFont("Helvetica", 7.8)
    c.drawCentredString(306, 43, "Treatment follows the label, applicable law, site conditions, and agreed scope. No outcome is guaranteed.")

    c.showPage()
    c.save()


if __name__ == "__main__":
    build()
    print(f"WROTE {OUTPUT}")
