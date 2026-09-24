#!/usr/bin/env python3
"""Build the public SDPP South American palm weevil prevention guide."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageEnhance
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "sdpp-sapw-prevention-management-guide.pdf"
TMP = ROOT / "tmp" / "pdfs"
LOGO = ROOT / "logo.png"

TREATMENT = ROOT / "images" / "palm-journal" / "september-treatment-day" / "poolside-treatment.webp"
ADULT = ROOT / "images" / "palm-journal" / "when-sapw-became-local" / "01-june-15-adult-sapw.jpg"
DECLINE = ROOT / "images" / "las-palmas" / "09-severe-decline-2026-07-10-las-palmas-declining-palm-central-frond-necrosis-detail-03.jpg"
STUMP = ROOT / "images" / "las-palmas" / "12-stump-20260713-184911.jpg"

GREEN = HexColor("#073b2b")
DARK = HexColor("#031d15")
GOLD = HexColor("#f4ae18")
CREAM = HexColor("#f7f3e9")
INK = HexColor("#14231d")
MUTED = HexColor("#52645c")
LINE = HexColor("#d9d2c3")
PALE = HexColor("#eee7d7")

PAGE_W, PAGE_H = letter
MARGIN = 44


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


def draw_text(c: canvas.Canvas, text: str, x: float, y: float, width: float, *, font="Helvetica", size=10, leading=14, color=INK) -> float:
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_bullets(c: canvas.Canvas, items: list[str], x: float, y: float, width: float, *, size=9.3, leading=12.5, gap=5) -> float:
    for item in items:
        c.setFillColor(GOLD)
        c.circle(x + 3, y + 3, 2.2, fill=1, stroke=0)
        y = draw_text(c, item, x + 14, y, width - 14, size=size, leading=leading)
        y -= gap
    return y


def section_label(c: canvas.Canvas, text: str, x: float, y: float) -> None:
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(x, y, text.upper())


def heading(c: canvas.Canvas, text: str, x: float, y: float, width: float, *, size=24, leading=27) -> float:
    return draw_text(c, text, x, y, width, font="Times-Bold", size=size, leading=leading, color=GREEN)


def page_frame(c: canvas.Canvas, page: int, title: str) -> None:
    c.setFillColor(DARK)
    c.rect(0, PAGE_H - 54, PAGE_W, 54, fill=1, stroke=0)
    c.drawImage(str(LOGO), MARGIN, PAGE_H - 45, width=29, height=29, preserveAspectRatio=True, mask="auto")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9.2)
    c.drawString(MARGIN + 38, PAGE_H - 30, "SAN DIEGO PALM PROTECTION")
    c.setFont("Helvetica", 7.6)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 30, title)
    c.setStrokeColor(LINE)
    c.line(MARGIN, 35, PAGE_W - MARGIN, 35)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.2)
    c.drawString(MARGIN, 22, "sandiegopalmprotection.com  |  262-492-3135")
    c.drawRightString(PAGE_W - MARGIN, 22, str(page))


def crop_image(path: Path, box: tuple[int, int], *, darken=1.0) -> ImageReader:
    image = Image.open(path).convert("RGB")
    target_w, target_h = box
    target_ratio = target_w / target_h
    ratio = image.width / image.height
    if ratio > target_ratio:
        new_w = int(image.height * target_ratio)
        left = (image.width - new_w) // 2
        image = image.crop((left, 0, left + new_w, image.height))
    else:
        new_h = int(image.width / target_ratio)
        top = max(0, (image.height - new_h) // 2)
        image = image.crop((0, top, image.width, top + new_h))
    if darken != 1.0:
        image = ImageEnhance.Brightness(image).enhance(darken)
    # The source photographs are full-resolution originals. Downsample only the
    # in-memory PDF derivative so the public guide stays crisp without becoming
    # a 40+ MB download.
    render_size = (target_w * 2, target_h * 2)
    image = image.resize(render_size, Image.Resampling.LANCZOS)
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=86, optimize=True, progressive=True)
    buffer.seek(0)
    return ImageReader(buffer)


def info_box(c: canvas.Canvas, title: str, text: str, x: float, y: float, width: float, height: float) -> None:
    c.setFillColor(CREAM)
    c.setStrokeColor(LINE)
    c.rect(x, y - height, width, height, fill=1, stroke=1)
    c.setFillColor(GOLD)
    c.rect(x, y - height, 4, height, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(x + 16, y - 22, title)
    draw_text(c, text, x + 16, y - 40, width - 30, size=8.7, leading=11.5, color=INK)


def page_cover(c: canvas.Canvas) -> None:
    hero = crop_image(TREATMENT, (612, 792), darken=0.5)
    c.drawImage(hero, 0, 0, width=PAGE_W, height=PAGE_H, preserveAspectRatio=False, mask="auto")
    c.setFillColor(DARK)
    c.setFillAlpha(0.4)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.drawImage(str(LOGO), 46, 710, width=46, height=46, preserveAspectRatio=True, mask="auto")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(105, 740, "SAN DIEGO PALM PROTECTION")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(46, 653, "FIELD GUIDE  |  SAN DIEGO COUNTY")
    c.setFillColor(white)
    c.setFont("Times-Bold", 34)
    c.drawString(46, 605, "South American Palm Weevil")
    c.drawString(46, 565, "Prevention & Management")
    c.setFont("Times-Bold", 34)
    c.drawString(46, 525, "for Mature Palms")
    draw_text(c, "What palm owners and property managers should know before visible crown failure.", 46, 482, 470, font="Helvetica", size=13.5, leading=18, color=white)
    c.setFillColor(GOLD)
    c.rect(46, 414, 5, 44, fill=1, stroke=0)
    draw_text(c, "Prevention is a program: identify the palm, establish a baseline, monitor it, treat when appropriate, and keep responsibility for the next visit.", 64, 448, 465, font="Helvetica-Bold", size=10.4, leading=14, color=white)
    c.setFillColor(DARK)
    c.setFillAlpha(0.82)
    c.roundRect(46, 64, 520, 108, 3, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(64, 145, "OWNER-LED, LICENSED PALM PROTECTION")
    draw_text(c, "California Pest Control Business License No. 47756  |  California Qualified Applicator License No. 175295  |  Category B - Landscape Maintenance  |  Insured", 64, 124, 470, size=8.5, leading=12, color=white)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(64, 82, "sandiegopalmprotection.com  |  262-492-3135")


def page_history(c: canvas.Canvas) -> None:
    page_frame(c, 2, "What SAPW is and how it reached San Diego")
    section_label(c, "The pest and the local timeline", MARGIN, 712)
    y = heading(c, "This is no longer a distant threat.", MARGIN, 684, 500)
    y = draw_text(c, "South American palm weevil (Rhynchophorus palmarum) is a large invasive snout beetle. Adults lay eggs in wounds, cracks, and protected areas of palms. The larvae feed inside the palm, where they can destroy the growing point and weaken the crown before the full extent of damage is visible.", MARGIN, y - 7, 510, size=10.2, leading=14.3)
    c.drawImage(crop_image(ADULT, (205, 210)), MARGIN, 330, width=205, height=210, preserveAspectRatio=False, mask="auto")
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawString(MARGIN, 318, "Adult SAPW captured and photographed by John Krause in Old Escondido.")
    x = 280
    y = 522
    for year, text in [
        ("2010", "Collected from infested Canary Island date palms in Tijuana."),
        ("2011", "Captured in monitoring traps in San Ysidro, about five miles north of Tijuana."),
        ("2014+", "UC Riverside reports populations likely established in or around San Ysidro by 2014 or earlier."),
        ("2020", "Published flight research reports established populations as far north as San Marcos."),
        ("NOW", "SAPW is established in San Diego County and is killing Canary Island date palms."),
    ]:
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y, year)
        y = draw_text(c, text, x + 48, y, 270, size=8.7, leading=11.5)
        y -= 12
    info_box(c, "Why Canary Island date palms are hit hard", "CIDPs offer a large, protected crown and substantial feeding tissue. Larvae can work inside the growing point while much of the outer canopy still looks green. By the time the center collapses, the useful treatment window may already be narrowing.", MARGIN, 286, 524, 118)
    c.setFillColor(GREEN)
    c.setFont("Times-Bold", 17)
    c.drawString(MARGIN, 140, "The history matters because the direction has been one-way: north.")
    draw_text(c, "Local owners should plan around established pest pressure, not wait for a neighborhood to be declared safe.", MARGIN, 118, 510, size=9.5, leading=13)


def page_damage(c: canvas.Canvas) -> None:
    page_frame(c, 3, "How SAPW damages a palm")
    section_label(c, "Damage and warning signs", MARGIN, 712)
    y = heading(c, "The center can fail while the outside still looks green.", MARGIN, 684, 500)
    c.drawImage(crop_image(DECLINE, (230, 245)), MARGIN, 338, width=230, height=245, preserveAspectRatio=False, mask="auto")
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawString(MARGIN, 326, "Visible central-crown decline before a documented removal in Old Escondido.")
    x = 302
    y = 566
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y, "What may appear")
    y = draw_bullets(c, [
        "Yellowing or failure beginning in the newest, upper leaves",
        "A flattened, thinning, asymmetric, or collapsing crown",
        "Frass, wet material, odor, holes, or tunneling near frond bases",
        "Pupal cases or adult weevils near the palm",
        "Rapid decline in a palm that previously looked stable",
    ], x, y - 23, 260)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y - 3, "What one photograph cannot prove")
    y = draw_text(c, "No single crown symptom confirms SAPW. Drought, irrigation, nutrition, pruning, disease, other pests, and concealed structural problems may overlap. Photographs support comparison; specimen identification or other qualified evaluation may be needed for confirmation.", x, y - 22, 260, size=8.8, leading=11.8)
    info_box(c, "Life cycle in practical terms", "Eggs may hatch in days. Larvae feed internally for roughly two months before pupating in palm-fiber cocoons. Warm conditions can support several generations per year. The hidden larval stage is why visible decline is late information.", MARGIN, 286, 524, 105)
    c.setFillColor(DARK)
    c.roundRect(MARGIN, 62, 524, 88, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Times-Bold", 17)
    c.drawString(MARGIN + 18, 124, "Do not wait for certainty from the sidewalk.")
    draw_text(c, "If the crown changed, record it and arrange an in-person look. Keep people away from a visibly unstable or actively failing palm.", MARGIN + 18, 102, 486, size=9.2, leading=12.5, color=white)


def page_prevention(c: canvas.Canvas) -> None:
    page_frame(c, 4, "The preventive management program")
    section_label(c, "Prevention before visible decline", MARGIN, 712)
    y = heading(c, "Preventive treatment is one part of a continuing program.", MARGIN, 684, 505)
    y = draw_text(c, "UC ANR recommends monitoring susceptible palms and protecting them with systemic insecticide applied to the trunk, crown, or soil. Its current public guidance states that preventive protection may require three to four treatments per year. The actual product, route, interval, and legal use must follow the pesticide label and fit the palm and site.", MARGIN, y - 6, 515, size=9.8, leading=13.5)
    cards = [
        ("1  Identify", "Confirm the species, location, ownership responsibility, access, and the individual palm being managed."),
        ("2  Establish a baseline", "Photograph the whole palm, crown, trunk, base, and property context before obvious decline."),
        ("3  Reduce avoidable stress", "Maintain appropriate irrigation and nutrition. Avoid unnecessary pruning and fresh wounds that may attract weevils."),
        ("4  Treat preventively", "Use a label-compliant systemic protection program when the risk, palm value, condition, and site justify it."),
        ("5  Monitor between visits", "Compare the newest growth, crown fullness, color, frond position, and any owner-reported change."),
        ("6  Keep continuity", "Retain treatment dates, products, application routes, photographs, observations, and the next scheduled action."),
    ]
    card_w = 252
    start_y = 532
    for index, (title, text) in enumerate(cards):
        col = index % 2
        row = index // 2
        x = MARGIN + col * 270
        top = start_y - row * 125
        c.setFillColor(CREAM)
        c.setStrokeColor(LINE)
        c.rect(x, top - 108, card_w, 108, fill=1, stroke=1)
        c.setFillColor(GREEN)
        c.setFont("Helvetica-Bold", 10.2)
        c.drawString(x + 14, top - 22, title)
        draw_text(c, text, x + 14, top - 42, card_w - 28, size=8.3, leading=11.2)
    c.setFillColor(GREEN)
    c.setFont("Times-Bold", 18)
    c.drawString(MARGIN, 132, "The schedule belongs to the label, the site, and the palm.")
    draw_text(c, "A calendar alone is not a program. Slopes, runoff, irrigation, palm height, public access, weather, prior treatment, and crown condition can all change the appropriate route or timing.", MARGIN, 108, 515, size=9.2, leading=12.7)


def page_methods(c: canvas.Canvas) -> None:
    page_frame(c, 5, "Management approaches and tradeoffs")
    section_label(c, "Know what each approach is for", MARGIN, 712)
    y = heading(c, "Different routes solve different parts of the problem.", MARGIN + 4, 684, 496, size=23, leading=26)
    y = draw_text(c, "These are management categories, not do-it-yourself instructions or product recommendations. A licensed professional must select and apply pesticides according to the registered label and site conditions.", MARGIN, y - 7, 515, size=9.5, leading=13.2)
    rows = [
        ("Monitoring", "Repeated crown and whole-palm observations, owner reporting, traps used correctly, and specimen reporting.", "Find change early and decide whether treatment, confirmation, or removal is needed.", "Trapping monitors activity; it does not protect the crown by itself."),
        ("Soil systemic", "Systemic insecticide applied to the root zone and moved upward with new growth.", "Preventive protection where soil, irrigation, slope, and uptake are suitable.", "UC guidance notes that movement to the crown can take 60 days or more."),
        ("Trunk or basal systemic", "Systemic material applied through a label-approved trunk or basal route.", "Faster uptake may be useful where the label, palm, and site permit it.", "UC guidance notes shorter residual periods for some basal approaches, often two to three months."),
        ("Crown treatment", "Insecticide directed to the central growing area under a label-approved program.", "Targets the area where adults and larvae threaten the growing point.", "Palm height, wind, rain, heat, access, and public exposure affect feasibility."),
        ("Combined response", "UC guidance describes crown spraying plus a soil systemic as an effective approach for infested palms.", "Immediate treatment where the palm remains a treatment candidate.", "Advanced internal damage may make treatment impractical or unsafe."),
    ]
    headers = ["Approach", "What it does", "Best role", "Important limit"]
    col_x = [MARGIN, 133, 305, 437]
    col_w = [78, 162, 122, 130]
    top = 565
    c.setFillColor(GREEN)
    c.rect(MARGIN, top, 524, 28, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 7.7)
    for x, header in zip(col_x, headers):
        c.drawString(x + 5, top + 10, header)
    y = top
    for index, row in enumerate(rows):
        height = 79 if index != 4 else 86
        y -= height
        c.setFillColor(CREAM if index % 2 == 0 else white)
        c.setStrokeColor(LINE)
        c.rect(MARGIN, y, 524, height, fill=1, stroke=1)
        for x, width, text in zip(col_x, col_w, row):
            font = "Helvetica-Bold" if x == MARGIN else "Helvetica"
            draw_text(c, text, x + 5, y + height - 17, width - 8, font=font, size=7.25, leading=9.4)
    info_box(c, "Traps belong away from protected palms", "UC ANR says monitoring traps should be placed at least 150 meters from the palms being monitored. Poor placement can attract weevils toward valuable palms. Trapping should be treated as a monitoring tool with a defined service plan.", MARGIN, 142, 524, 82)


def page_decline(c: canvas.Canvas) -> None:
    page_frame(c, 6, "When decline is advanced")
    section_label(c, "Treatment, removal, and sanitation", MARGIN, 712)
    y = heading(c, "Not every palm remains a treatment candidate.", MARGIN, 684, 500)
    y = draw_text(c, "The decision changes when crown failure is advanced, internal damage is extensive, or the palm may be unstable. Treatment cannot rebuild a destroyed growing point or guarantee recovery.", MARGIN, y - 8, 510, size=10, leading=14)
    c.drawImage(crop_image(STUMP, (238, 260)), MARGIN, 303, width=238, height=260, preserveAspectRatio=False, mask="auto")
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawString(MARGIN, 291, "Fresh stump after a documented Old Escondido palm removal.")
    x = 308
    y = 555
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y, "When to escalate")
    y = draw_bullets(c, [
        "Rapid central-crown collapse or a dropped crown",
        "Evidence of advanced internal feeding or decay",
        "A palm leaning, breaking, or presenting an immediate target risk",
        "A dead or badly infested palm that can produce more weevils",
    ], x, y - 24, 252)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y - 4, "Removal is also pest management")
    y = draw_text(c, "UC ANR advises prompt removal when treatment is no longer an option. Infested crown material should be chipped, burned where legally permitted, or deeply buried within 24 hours so adults do not emerge and escape.", x, y - 24, 252, size=8.7, leading=11.8)
    info_box(c, "Do not confuse a removal date with a diagnosis", "A stump proves that the palm is gone. It does not prove why it declined. Preserve photographs, treatment history, specimens, and dismantling findings when available so the final record distinguishes observed facts from attribution.", MARGIN, 248, 524, 100)
    c.setFillColor(DARK)
    c.roundRect(MARGIN, 57, 524, 64, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN + 16, 97, "SAFETY FIRST")
    draw_text(c, "Keep people away from a visibly unstable palm and contact the appropriate tree-risk or emergency professional when life safety may be involved.", MARGIN + 16, 79, 490, size=8.6, leading=11.5, color=white)


def page_action(c: canvas.Canvas) -> None:
    page_frame(c, 7, "Owner action plan and sources")
    section_label(c, "What to do now", MARGIN, 712)
    y = heading(c, "If the palm matters, make the decision before the crown does.", MARGIN, 684, 510)
    left = MARGIN
    right = 320
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left, 590, "For a healthy-looking CIDP")
    draw_bullets(c, [
        "Identify and photograph the palm now.",
        "Review nearby losses and known local pressure.",
        "Correct avoidable irrigation, nutrition, and pruning stress.",
        "Discuss preventive systemic protection before visible decline.",
        "Schedule the next observation and keep treatment history together.",
    ], left, 565, 245, size=8.6, leading=11.4)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(right, 590, "For a palm that changed")
    draw_bullets(c, [
        "Photograph the whole palm and the center of the crown.",
        "Record when the change was first noticed.",
        "Avoid unnecessary pruning before evaluation.",
        "Arrange an in-person assessment promptly.",
        "Escalate immediately if the palm may be unstable.",
    ], right, 565, 245, size=8.6, leading=11.4)
    info_box(c, "Questions to ask a provider", "Have you treated SAPW before? What route and interval fit this palm and label? How will you document the application? What should I watch between visits? What changes would trigger a different response?", MARGIN, 430, 524, 86)
    c.setFillColor(GREEN)
    c.setFont("Times-Bold", 17)
    c.drawString(MARGIN, 320, "Primary sources")
    sources = [
        ("UC ANR - Management Options", "https://www.ucanr.edu/site/south-american-palm-weevil/management-options"),
        ("UC ANR - Frequently Asked Questions", "https://www.ucanr.edu/site/south-american-palm-weevil/frequently-asked-questions"),
        ("UC IPM - Giant Palm Weevils", "https://ipm.ucanr.edu/home-and-landscape/giant-palm-weevils/"),
        ("UC Riverside - South American Palm Weevil", "https://biocontrol.ucr.edu/south-american-palm-weevil"),
        ("UC ANR - What You Can Do", "https://ucanr.edu/site/south-american-palm-weevil/what-you-can-do"),
    ]
    y = 294
    c.setFont("Helvetica", 8.2)
    for label, url in sources:
        c.setFillColor(GREEN)
        c.drawString(MARGIN, y, label)
        c.linkURL(url, (MARGIN, y - 2, MARGIN + stringWidth(label, "Helvetica", 8.2), y + 9), relative=0)
        c.setStrokeColor(GREEN)
        c.line(MARGIN, y - 1, MARGIN + stringWidth(label, "Helvetica", 8.2), y - 1)
        y -= 19
    c.setFillColor(DARK)
    c.roundRect(MARGIN, 57, 524, 126, 3, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(MARGIN + 18, 159, "SAN DIEGO PALM PROTECTION")
    c.setFillColor(white)
    c.setFont("Times-Bold", 20)
    c.drawString(MARGIN + 18, 132, "Protect the palm while you still have choices.")
    draw_text(c, "Owner-led assessment, preventive treatment, monitoring, and continuing care for mature palms in San Diego County.", MARGIN + 18, 109, 470, size=8.8, leading=12, color=white)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN + 18, 75, "sandiegopalmprotection.com  |  262-492-3135")


def build() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    c.setTitle("South American Palm Weevil Prevention & Management Guide")
    c.setAuthor("John Krause, San Diego Palm Protection")
    c.setSubject("South American palm weevil history, warning signs, preventive management, treatment approaches, and removal response for San Diego palm owners")
    for page in (page_cover, page_history, page_damage, page_prevention, page_methods, page_decline, page_action):
        page(c)
        c.showPage()
    c.save()
    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    build()
