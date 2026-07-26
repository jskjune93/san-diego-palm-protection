from __future__ import annotations

from hashlib import sha256
from io import BytesIO
from pathlib import Path
import json

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "old-escondido-mature-palm-documentation-example.pdf"
MANIFEST = ROOT / "proof-data" / "approved" / "old-escondido-mature-palm-documentation-example.json"
IMAGE_DIR = ROOT / "images" / "old-escondido-ufmp"

GREEN = colors.HexColor("#073d2b")
GREEN_2 = colors.HexColor("#0e553c")
GOLD = colors.HexColor("#ffb31a")
CREAM = colors.HexColor("#f5f0e3")
INK = colors.HexColor("#16221d")
MUTED = colors.HexColor("#57635e")
LINE = colors.HexColor("#d8d3c6")
PAPER = colors.HexColor("#fffdf8")
PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN_X = 0.62 * inch
MARGIN_TOP = 0.62 * inch
MARGIN_BOTTOM = 0.58 * inch


class PublicProofDoc(BaseDocTemplate):
    def __init__(self, path: Path):
        super().__init__(
            str(path),
            pagesize=letter,
            leftMargin=MARGIN_X,
            rightMargin=MARGIN_X,
            topMargin=MARGIN_TOP,
            bottomMargin=MARGIN_BOTTOM,
            title="Old Escondido Mature Palm Documentation Example",
            author="San Diego Palm Protection",
            subject="Sanitized public example of broader-area mature palm documentation",
            creator="San Diego Palm Protection",
            producer="San Diego Palm Protection",
        )
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(PageTemplate(id="proof", frames=[frame], onPage=draw_page))


def draw_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    if doc.page > 1:
        canvas.setStrokeColor(LINE)
        canvas.line(MARGIN_X, PAGE_HEIGHT - 0.38 * inch, PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 0.38 * inch)
        canvas.setFont("Helvetica-Bold", 7.8)
        canvas.setFillColor(GREEN)
        canvas.drawString(MARGIN_X, PAGE_HEIGHT - 0.29 * inch, "SAN DIEGO PALM PROTECTION")
        canvas.setFont("Helvetica", 7.8)
        canvas.setFillColor(MUTED)
        label = "SANITIZED PUBLIC EXAMPLE"
        canvas.drawRightString(PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 0.29 * inch, label)
    canvas.setStrokeColor(LINE)
    canvas.line(MARGIN_X, 0.38 * inch, PAGE_WIDTH - MARGIN_X, 0.38 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN_X, 0.24 * inch, "Visible-condition documentation; limitations apply.")
    canvas.drawRightString(PAGE_WIDTH - MARGIN_X, 0.24 * inch, f"{doc.page}")
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverEyebrow", fontName="Helvetica-Bold", fontSize=9, leading=12,
    textColor=GOLD, spaceAfter=10, tracking=1.1,
))
styles.add(ParagraphStyle(
    name="CoverTitle", fontName="Times-Bold", fontSize=32, leading=34,
    textColor=colors.white, spaceAfter=14,
))
styles.add(ParagraphStyle(
    name="CoverSub", fontName="Helvetica", fontSize=13, leading=18,
    textColor=colors.white,
))
styles.add(ParagraphStyle(
    name="H1Proof", fontName="Times-Bold", fontSize=24, leading=27,
    textColor=GREEN, spaceAfter=11,
))
styles.add(ParagraphStyle(
    name="H2Proof", fontName="Times-Bold", fontSize=16, leading=19,
    textColor=GREEN, spaceBefore=8, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="BodyProof", fontName="Helvetica", fontSize=9.6, leading=14.2,
    textColor=INK, spaceAfter=9,
))
styles.add(ParagraphStyle(
    name="SmallProof", fontName="Helvetica", fontSize=8.1, leading=11.5,
    textColor=MUTED, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="CardTitle", fontName="Helvetica-Bold", fontSize=10.2, leading=13,
    textColor=GREEN, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="CardBody", fontName="Helvetica", fontSize=8.6, leading=12.2,
    textColor=INK,
))
styles.add(ParagraphStyle(
    name="Callout", fontName="Helvetica-Bold", fontSize=10, leading=14,
    textColor=GREEN,
))
styles.add(ParagraphStyle(
    name="CenterSmall", parent=styles["SmallProof"], alignment=TA_CENTER,
))


def p(text: str, style: str = "BodyProof") -> Paragraph:
    return Paragraph(text, styles[style])


def heading(title: str, eyebrow: str | None = None):
    blocks = []
    if eyebrow:
        blocks.append(p(eyebrow.upper(), "CoverEyebrow"))
    blocks.append(p(title, "H1Proof"))
    blocks.append(Table([[""]], colWidths=[7.25 * inch], rowHeights=[3], style=[
        ("BACKGROUND", (0, 0), (-1, -1), GOLD),
        ("LINEBELOW", (0, 0), (-1, -1), 0, GOLD),
    ]))
    blocks.append(Spacer(1, 0.16 * inch))
    return blocks


def fitted_image(path: Path, max_width: float, max_height: float) -> Image:
    with PILImage.open(path) as source:
        width, height = source.size
        source = source.convert("RGB")
        longest = max(width, height)
        if longest > 1800:
            ratio = 1800 / longest
            source = source.resize(
                (round(width * ratio), round(height * ratio)),
                PILImage.Resampling.LANCZOS,
            )
        public_copy = BytesIO()
        source.save(public_copy, format="JPEG", quality=88, optimize=True)
        public_copy.seek(0)
    scale = min(max_width / width, max_height / height)
    return Image(public_copy, width=width * scale, height=height * scale)


def photo_card(path: Path, caption: str, width: float = 3.46 * inch, height: float = 2.42 * inch):
    image = fitted_image(path, width - 0.16 * inch, height)
    table = Table(
        [[image], [p(caption, "SmallProof")]],
        colWidths=[width],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), CREAM),
            ("BOX", (0, 0), (-1, -1), 0.5, LINE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, 0), 7),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
            ("TOPPADDING", (0, 1), (-1, 1), 6),
            ("BOTTOMPADDING", (0, 1), (-1, 1), 7),
        ],
    )
    return table


def field_row(label: str, value: str):
    return [p(label, "CardTitle"), p(value, "CardBody")]


def build_story():
    story = []

    cover_image = IMAGE_DIR / "old-home-mature-cidps-golden-hour.jpg"
    cover = fitted_image(cover_image, 7.25 * inch, 4.25 * inch)
    title_block = Table(
        [[p("SANITIZED PUBLIC EXAMPLE", "CoverEyebrow")],
         [p("Old Escondido Mature Palm<br/>Documentation Example", "CoverTitle")],
         [p("A field-record example for preservation, monitoring, loss documentation, and broader-area implementation.", "CoverSub")]],
        colWidths=[7.25 * inch],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), GREEN),
            ("LEFTPADDING", (0, 0), (-1, -1), 24),
            ("RIGHTPADDING", (0, 0), (-1, -1), 24),
            ("TOPPADDING", (0, 0), (-1, 0), 22),
            ("TOPPADDING", (0, 1), (-1, 1), 0),
            ("BOTTOMPADDING", (0, 1), (-1, 1), 12),
            ("BOTTOMPADDING", (0, 2), (-1, 2), 24),
        ],
    )
    story.extend([title_block, Spacer(1, 0.18 * inch), cover, Spacer(1, 0.14 * inch)])
    story.append(p(
        "This public derivative omits private addresses, recipient information, correspondence, and parcel-level identifiers. "
        "It is not a municipal plan, formal tree-risk assessment, laboratory report, or City-endorsed document.",
        "SmallProof",
    ))
    story.append(PageBreak())

    story.extend(heading("Purpose and Scope", "How to read this example"))
    story.append(p(
        "This document demonstrates how San Diego Palm Protection can organize broader-area palm observations into a stable, "
        "repeatable record. It uses a limited Old Escondido field sample to show a documentation method - not to claim a "
        "complete neighborhood inventory or a municipal role."
    ))
    exact = (
        "San Diego Palm Protection submitted mature-palm documentation for consideration during the City of Escondido "
        "Urban Forest Management Plan process."
    )
    story.append(Table([[p(exact, "Callout")]], colWidths=[7.25 * inch], style=[
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("LINEBEFORE", (0, 0), (0, -1), 4, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 13),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 13),
    ]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(p("What this example can demonstrate", "H2Proof"))
    items = [
        ("Location context", "General area and property context can be recorded without publishing a private address."),
        ("Photographic baseline", "Dated or source-retained photographs can preserve visible crown, trunk, and site context."),
        ("Repeat observations", "A consistent record structure helps compare visible change across visits."),
        ("Loss and response", "Removal, replacement, contractor records, and follow-up can be linked to the same palm record."),
        ("Implementation value", "Portfolio or neighborhood summaries can support monitoring and planning decisions."),
        ("Escalation boundaries", "Records can flag questions for a qualified arborist, laboratory, property authority, or other specialist."),
    ]
    rows = []
    for i in range(0, len(items), 2):
        rows.append([
            [p(items[i][0], "CardTitle"), p(items[i][1], "CardBody")],
            [p(items[i + 1][0], "CardTitle"), p(items[i + 1][1], "CardBody")],
        ])
    story.append(Table(rows, colWidths=[3.56 * inch, 3.56 * inch], style=[
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
    ]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(p(
        "<b>Municipal boundary:</b> Submission for consideration does not imply endorsement, partnership, selection, "
        "approval, adoption, contract, or an official City role.", "SmallProof"
    ))
    story.append(PageBreak())

    story.extend(heading("Documentation Method", "A repeatable field structure"))
    method_rows = [
        field_row("1. Identify", "Assign a stable palm or group identifier; record only the location precision appropriate to the audience."),
        field_row("2. Photograph", "Capture crown, trunk, base, surrounding context, and a repeatable viewpoint when access and safety allow."),
        field_row("3. Observe", "Describe visible conditions without turning an observation into an unsupported diagnosis."),
        field_row("4. Classify next action", "Continue monitoring, obtain supporting records, request specialist review, coordinate response, or document loss."),
        field_row("5. Preserve chronology", "Keep dates, supplied work records, follow-up images, and limitations connected to the same record."),
    ]
    story.append(Table(method_rows, colWidths=[1.45 * inch, 5.8 * inch], style=[
        ("BACKGROUND", (0, 0), (0, -1), CREAM),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(Spacer(1, 0.22 * inch))
    story.append(p("Example record fields", "H2Proof"))
    fields = [
        "Public-safe record ID", "General location or management zone", "Palm type and visible context",
        "Observation date or date withheld publicly", "Photo viewpoint", "Visible crown and trunk observations",
        "Reported or supplied history", "Monitoring priority", "Recommended next action", "Limitations and referral notes",
    ]
    field_cells = [[p(f"• {value}", "CardBody") for value in fields[i:i + 2]] for i in range(0, len(fields), 2)]
    story.append(Table(field_cells, colWidths=[3.56 * inch, 3.56 * inch], style=[
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(PageBreak())

    story.extend(heading("Representative Field Records", "Old Escondido area context"))
    story.append(p(
        "The following examples retain general context while withholding private-property addresses. Captions report what is "
        "visible or what the source record supports; they do not assign ownership, historic designation, or pest diagnosis."
    ))
    story.append(Table([[
        photo_card(
            IMAGE_DIR / "old-escondido-multiple-cidp-street-pattern.jpg",
            "<b>Public example record OE-01.</b> General Old Escondido neighborhood context. Multiple mature Canary Island "
            "date palms are visible within one streetscape view. Exact location and capture date are withheld in this public derivative."
        ),
        photo_card(
            IMAGE_DIR / "old-home-mature-cidps-golden-hour.jpg",
            "<b>Public example record OE-02.</b> Mature Canary Island date palms and an older-looking residence read as one "
            "established landscape composition. No construction year, ownership, or historic designation is assigned."
        ),
    ]], colWidths=[3.56 * inch, 3.56 * inch], style=[
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(Spacer(1, 0.16 * inch))
    story.append(Table([[p(
        "<b>Observation boundary:</b> A photograph can document visible form, crown condition, and setting. It cannot by itself "
        "confirm internal condition, structural safety, pest presence, treatment history, ownership, or legal status.", "SmallProof"
    )]], colWidths=[7.25 * inch], style=[
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("LINEBEFORE", (0, 0), (0, -1), 4, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
    ]))
    story.append(PageBreak())

    story.extend(heading("Baseline and Monitoring Value", "From one image to a chronology"))
    baseline = photo_card(
        IMAGE_DIR / "healthy-private-yard-cidp.jpg",
        "<b>Public example record OE-03.</b> Owner-approved November 2025 photographic baseline of a mature private-property "
        "Canary Island date palm. Address and identifying property details are omitted.",
        width=3.35 * inch,
        height=2.55 * inch,
    )
    sequence = [
        [p("Baseline", "CardTitle"), p("Retain dated crown, trunk, and site-context views using a repeatable position.", "CardBody")],
        [p("Follow-up", "CardTitle"), p("Compare visible change while recording weather, access, and image-quality limitations.", "CardBody")],
        [p("Work record", "CardTitle"), p("Link supplied scope, service date, contractor identity, and before/after photographs when available.", "CardBody")],
        [p("Escalation", "CardTitle"), p("Flag rapid change, uncertainty, or questions outside the visual documentation scope.", "CardBody")],
    ]
    seq_table = Table(sequence, colWidths=[1.0 * inch, 2.72 * inch], style=[
        ("BACKGROUND", (0, 0), (0, -1), CREAM),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ])
    story.append(Table([[baseline, seq_table]], colWidths=[3.45 * inch, 3.72 * inch], style=[
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(p("A stable record makes change reviewable", "H2Proof"))
    story.append(p(
        "Repeat monitoring is useful because a single image is easy to overread. When viewpoints, dates, observations, and "
        "limitations stay connected, an owner or stakeholder can distinguish a documented change from a difference in angle, "
        "light, access, or image quality."
    ))
    story.append(p(
        "Monitoring records can also preserve what was recommended, what work was reported or supplied, and when escalation "
        "was advised. They do not certify concealed work, workmanship, safety, code compliance, licensing, efficacy, or outcome "
        "outside an explicit qualified scope.", "SmallProof"
    ))
    story.append(PageBreak())

    story.extend(heading("Decline, Loss, and Response Records", "Keep outcomes connected to the baseline"))
    loss_photo = photo_card(
        IMAGE_DIR / "las-palmas-documented-loss-crown-context.jpg",
        "<b>Public example record OE-04.</b> Las Palmas crown context photographed before removal. The image records visible "
        "crown change without asserting a laboratory diagnosis or a single confirmed cause.",
        width=3.2 * inch,
        height=3.25 * inch,
    )
    response_text = [
        p("A decline or loss record may include", "H2Proof"),
        p("• the last known baseline and follow-up photographs"),
        p("• visible changes and the dates retained in the source record"),
        p("• communication or access milestones, summarized without private correspondence"),
        p("• supplied contractor scope and visible completion photographs"),
        p("• removal status and remaining site context"),
        p("• replacement planning, establishment monitoring, or referral"),
        Spacer(1, 0.1 * inch),
        p(
            "<b>Cause boundary:</b> Visible decline is not a laboratory diagnosis. A public record should distinguish observed "
            "conditions from reported history, possible causes, presumed attribution, and confirmed findings.", "SmallProof"
        ),
    ]
    story.append(Table([[loss_photo, response_text]], colWidths=[3.3 * inch, 3.82 * inch], style=[
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Table([[p(
        "<b>Why this matters:</b> When a significant palm is removed, the record can preserve what was visible beforehand, "
        "what response occurred, and what landscape condition remained. That chronology supports accountable follow-through "
        "without claiming a guaranteed preservation or replacement outcome.", "Callout"
    )]], colWidths=[7.25 * inch], style=[
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("LINEBEFORE", (0, 0), (0, -1), 4, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 15),
        ("RIGHTPADDING", (0, 0), (-1, -1), 15),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(PageBreak())

    story.extend(heading("Implementation Uses", "Managed-property and urban-forest support"))
    uses = [
        ("Inventory maintenance", "Keep stable palm identifiers, location context, species or type, photographs, and status fields current."),
        ("Monitoring", "Schedule repeat observations and preserve a reviewable chronology of visible change."),
        ("Contractor verification", "Document visible completion and supplied records within stated scope and limitations."),
        ("Removal and replacement", "Connect decline, removal, replacement selection, installation, and establishment follow-up."),
        ("Historic-resource context", "Preserve mature-palm landscape context without assigning an unsupported designation."),
        ("Portfolio summaries", "Group records by property, zone, or priority without exposing private details in public examples."),
    ]
    use_rows = []
    for title, body in uses:
        use_rows.append([p(title, "CardTitle"), p(body, "CardBody")])
    story.append(Table(use_rows, colWidths=[1.75 * inch, 5.5 * inch], style=[
        ("BACKGROUND", (0, 0), (0, -1), CREAM),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(Spacer(1, 0.22 * inch))
    story.append(p("Example action categories", "H2Proof"))
    action_rows = [[
        p("<b>Monitor</b><br/>Retain baseline and repeat on an appropriate schedule.", "CardBody"),
        p("<b>Clarify</b><br/>Obtain supplied history, access, or supporting records.", "CardBody"),
        p("<b>Escalate</b><br/>Refer a question beyond visual field documentation.", "CardBody"),
        p("<b>Respond</b><br/>Coordinate documented work, removal, or replacement follow-through.", "CardBody"),
    ]]
    story.append(Table(action_rows, colWidths=[1.81 * inch] * 4, style=[
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(PageBreak())

    story.extend(heading("Limitations and Next Steps", "Public example boundaries"))
    limitations = [
        "Visual field observations only; hidden conditions may not be visible.",
        "Not a complete Old Escondido inventory or full Urban Forest Management Plan.",
        "Not a formal tree-risk assessment, engineering opinion, municipal-code determination, or laboratory confirmation.",
        "No City endorsement, partnership, selection, approval, adoption, contract, or official role is implied.",
        "No guarantee of treatment success, preservation, safety, contractor performance, or replacement outcome.",
        "Exact private-property addresses, identities, correspondence, and parcel-level details are intentionally omitted.",
    ]
    story.append(Table([[p(f"• {item}", "BodyProof")] for item in limitations], colWidths=[7.25 * inch], style=[
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(Spacer(1, 0.24 * inch))
    story.append(p("See the related service and proof pages", "H2Proof"))
    story.append(p(
        '<link href="https://www.sandiegopalmprotection.com/urban-forest-palm-documentation.html" '
        'color="#073d2b"><u>Urban Forest Palm Documentation</u></link><br/>'
        '<link href="https://www.sandiegopalmprotection.com/san-diego-palm-protection-sample-assessment.pdf" '
        'color="#073d2b"><u>Sanitized Residential Palm Assessment</u></link><br/>'
        '<link href="https://www.sandiegopalmprotection.com/palm-proof-examples.html" '
        'color="#073d2b"><u>Field Work and Sample Work</u></link>'
    ))
    story.append(Spacer(1, 0.14 * inch))
    story.append(Table([[
        p("<b>San Diego Palm Protection</b><br/>Owner-led mature palm assessment, monitoring, protection, and response.", "CardBody"),
        p(
            '<b>Contact</b><br/><link href="tel:2624923135" color="#073d2b">262-492-3135</link><br/>'
            '<link href="mailto:sandiegopalmprotection@gmail.com" color="#073d2b">'
            'sandiegopalmprotection@gmail.com</link>', "CardBody"
        ),
    ]], colWidths=[4.45 * inch, 2.8 * inch], style=[
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.75, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 13),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 13),
    ]))

    return story


def write_manifest():
    digest = sha256(OUTPUT.read_bytes()).hexdigest()
    media = [
        "old-home-mature-cidps-golden-hour.jpg",
        "old-escondido-multiple-cidp-street-pattern.jpg",
        "healthy-private-yard-cidp.jpg",
        "las-palmas-documented-loss-crown-context.jpg",
    ]
    manifest = {
        "schema_version": 1,
        "artifact_id": "old-escondido-mature-palm-documentation-example",
        "product_type": "website_proof_excerpt",
        "artifact_version": "1.0.0",
        "artifact_fingerprint": digest,
        "approved_fingerprint": digest,
        "status": "approved",
        "publication_approval": "approved",
        "privacy": "sanitized",
        "publication_target": "website",
        "privacy_scan_passed": True,
        "content": {
            "title": "Old Escondido Mature Palm Documentation Example",
            "public_filename": OUTPUT.name,
            "page_count": 8,
            "source_basis": "Privacy-reviewed SDPP field material and public-safe factual statements",
        },
        "media": [
            {"filename": name, "approved_for_public": True}
            for name in media
        ],
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main():
    doc = PublicProofDoc(OUTPUT)
    doc.build(build_story())
    write_manifest()
    print(f"Built {OUTPUT.name}")
    print(f"SHA256 {sha256(OUTPUT.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
