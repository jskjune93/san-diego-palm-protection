from __future__ import annotations

from html import escape
from pathlib import Path
import json

from site_components import ROOT, BASE_URL, page, three_pillars, credentials


def section(eyebrow: str, heading: str, intro: str, content: str, classes: str = "") -> str:
    return f'<section class="section {classes}"><div class="section-intro"><p class="eyebrow">{escape(eyebrow)}</p><h2>{escape(heading)}</h2><p>{escape(intro)}</p></div>{content}</section>'


def cards(items: list[tuple[str, str]], cls: str = "service-grid") -> str:
    return f'<div class="{cls}">' + "".join(f'<article class="service-card"><h3>{escape(h)}</h3><p>{escape(p)}</p></article>' for h, p in items) + "</div>"


def process(items: list[tuple[str, str]]) -> str:
    return '<div class="process">' + "".join(f'<div><h3>{escape(h)}</h3><p>{escape(p)}</p></div>' for h, p in items) + "</div>"


PAGES: dict[str, dict] = {
    "index.html": {
        "title": "San Diego Palm Protection | Assessment, Monitoring & Response",
        "description": "Qualified and insured palm assessment, documentation, monitoring, protection, treatment, decline response, removal coordination, and replacement planning.",
        "eyebrow": "Mature palm decisions begin with a record",
        "h1": "Know what is changing. Protect what matters. Plan the next step.",
        "lede": "SDPP assesses, photographs, documents, monitors, protects, and responds to significant palms across North County San Diego—from a residential baseline to managed-property reporting and decline coordination.",
        "image": "background.jpg",
        "body": section("One connected lifecycle", "Three services. One palm record.", "A dated baseline anchors protection decisions, contractor response, documented loss, and replacement planning.", three_pillars()) +
        section("Primary service", "Records & Monitoring", "Schedule a Palm Assessment, establish a condition baseline, and keep the next decision connected to dated evidence.", '<p><a class="button" href="./palm-records-monitoring-verification.html">Schedule a Palm Assessment</a> <a href="./report-a-palm.html">Report a Palm</a></p>') +
        section("Clear starting points", "Choose the pathway that matches the property.", "Each pathway produces a practical record, not a vague promise.", cards([
            ("Residential Mature Palm Assessment", "A site visit focused on visible condition, context, risk factors, photographs, and written next steps."),
            ("Recurring Palm Monitoring", "Comparable dated visits that help distinguish a stable feature from visible change over time."),
            ("Managed-property Inventory & Reporting", "Stable palm IDs, baseline photographs, priority findings, and portfolio-level reporting for responsible stakeholders."),
            ("Palm decline and urgent response", "Document visible change, establish what is known and unknown, and coordinate the appropriate contractor or next action."),
        ])) +
        section("Evidence before claims", "Written reporting makes the work usable.", "Every assessment separates observation from interpretation and records access, evidence, certainty, limitations, and recommendations.", process([
            ("Assess", "Define the property, palms, question, and access available."),
            ("Document", "Create dated photographs and a visible-condition baseline."),
            ("Monitor or protect", "Compare change or carry out an authorized protection plan."),
            ("Respond", "Coordinate urgent work, verification, removal, loss records, or replacement."),
        ]), "section-tint") +
        section("Continue exploring", "Preservation, loss, and replacement resources.", "Valuable field and planning resources remain connected to the service architecture.", '<p><a href="./palm-sourcing-installation.html">Palm sourcing and installation</a> · <a href="./specimen-palms-cycads.html">Specimen palms and cycads</a> · <a href="./palm-journal/documented-loss/">Documented Loss</a></p>'),
    },
    "residential-palm-assessment.html": {
        "title": "Residential Mature Palm Assessment | San Diego Palm Protection",
        "description": "A clear residential palm assessment with baseline photographs, visible-condition findings, limitations, and written next steps.",
        "eyebrow": "Residential pathway", "h1": "Residential Mature Palm Assessment",
        "lede": "A defined visit for owners who need a reliable starting point before treatment, monitoring, pruning, a property decision, or concern about visible change.",
        "image": "mature_healthy_cidp_poway_mansion.jpg",
        "body": section("Core deliverable", "Palm Condition Baseline", "The baseline fixes a date, palm identity, viewing context, and set of comparable images so future change has a reference.", cards([
            ("Site and palm context", "Location, species when supportable, landscape role, access, and the question prompting the visit."),
            ("Dated photographic record", "Consistent overview, crown, trunk, ground, and concern-detail views when access safely permits."),
            ("Visible-condition findings", "Observed features are separated from reported information, possible concerns, and confirmed findings."),
            ("Written Palm Condition Report", "A concise record of findings, certainty, limitations, recommendations, and an appropriate monitoring interval."),
        ])) + section("What it is not", "Useful because its limits are explicit.", "A visual assessment cannot promise tree safety, uncover hidden conditions, replace laboratory confirmation, or guarantee a treatment outcome. Referral is recommended where the question exceeds the documented scope.", '<p class="note">Urgent structural or life-safety concerns may require a qualified arborist, emergency contractor, property authority, or other specialist. Regulated work is offered only when current credentials, authorization, label, site, and scope support it.</p>', "section-tint") +
        section("Next step", "From one visit to a monitoring record.", "When change over time matters, the baseline becomes visit one of a recurring monitoring timeline.", process([("Scope", "Identify the decision and palms."), ("Visit", "Observe and photograph accessible conditions."), ("Report", "Receive a dated written record."), ("Revisit", "Compare at a useful interval.")]))
    },
    "palm-records-monitoring-verification.html": {
        "title": "Palm Assessment, Monitoring & Documentation Services | SDPP",
        "description": "Palm condition baselines, written reporting, recurring monitoring, managed-property inventories, contractor-work verification, protection, and decline response.",
        "eyebrow": "Service architecture", "h1": "Assessment, documentation, protection, and response—connected.",
        "lede": "SDPP organizes palm work around a durable record: what was visible, what changed, what was recommended, what work was reported, and what decision comes next.",
        "image": "journal-monitoring.jpg",
        "body": section("The complete service map", "Three pillars support the full palm lifecycle.", "Start with documentation, move into qualified protection when justified, and preserve the record through response or replacement.", three_pillars()) +
        section("Monitoring & Documentation", "Services with a defined output.", "These are stand-alone services, not incidental paperwork.", cards([
            ("Residential Mature Palm Assessment", "A structured site visit with visible-condition findings and written next steps."),
            ("Palm Condition Baseline", "Dated, repeatable photographs and context for future comparison."),
            ("Recurring Palm Monitoring", "Scheduled revisits with change-over-time comparison and updated recommendations."),
            ("Managed-property Palm Inventory & Reporting", "Stable asset IDs, property overview, priority findings, and portfolio reporting."),
            ("Written Palm Condition Reporting", "A usable summary of evidence, certainty, limitations, and recommended next action."),
            ("Contractor-Work Verification", "A record of visible completion and supplied documentation—not certification of hidden work, workmanship, code compliance, or efficacy."),
        ]), "section-tint") +
        section("Request", "Schedule a Palm Assessment", "Use the inquiry to identify a residential, monitoring, managed-property, protection, or response need.", f'{credentials("BUSINESS_CREDENTIALS_CONTACT")}<form class="inquiry-form" action="mailto:sandiegopalmprotection@gmail.com" method="get"><label for="service-request">Service needed</label><select id="service-request" name="subject"><option>Residential Mature Palm Assessment</option><option>Recurring Palm Monitoring</option><option>Managed-property Palm Inventory and Reporting</option><option>Protection or treatment planning</option><option>Decline, removal, or replacement coordination</option></select><button class="button" type="submit">Prepare email inquiry</button></form>') +
        section("Related decisions", "From evidence to outcome.", "Follow the appropriate path without losing the record.", '<p><a href="./palm-removal-coordination.html">Decline, removal, and replacement</a> · <a href="./palm-sourcing-installation.html">Sourcing and installation</a> · <a href="./specimen-palms-cycads.html">Specimen palms and cycads</a> · <a href="./palm-journal/documented-loss/">Documented Loss</a></p>')
    },
    "quarterly-palm-care-san-diego.html": {
        "title": "Recurring Palm Monitoring | San Diego Palm Protection",
        "description": "Recurring palm monitoring with comparable photographs, condition timelines, written visit reports, and clear escalation triggers.",
        "eyebrow": "Monitoring pathway", "h1": "Recurring Palm Monitoring",
        "lede": "A monitoring plan turns isolated photographs into comparable evidence—at an interval selected for the palm, concern, season, property, and decision.",
        "image": "journal-seasonal.jpg",
        "body": section("Repeatable by design", "Each visit extends the baseline.", "The same palm ID, useful viewpoints, visible-condition fields, and known limitations carry forward.", process([
            ("Baseline", "Create the first dated condition record."),
            ("Revisit", "Photograph comparable views and record new observations."),
            ("Compare", "Identify stable features, visible change, and evidence gaps."),
            ("Report", "Update priorities, interval, and escalation recommendations."),
        ])) + section("Not necessarily quarterly", "The interval follows the decision.", "A calendar-quarter schedule can be useful, but it is not automatically appropriate for every palm. SDPP records the recommended interval and the reason for it.", cards([
            ("Residential monitoring", "Follow a significant palm after baseline, treatment, pruning, storm exposure, or a visible concern."),
            ("Managed-property monitoring", "Maintain an auditable multi-palm timeline with priority changes and work-status notes."),
            ("Escalation", "Recommend closer review, specialist referral, treatment consideration, or response when documented change supports it."),
        ]), "section-tint")
    },
    "managed-property-palm-services.html": {
        "title": "Managed-property Palm Inventory & Reporting | SDPP",
        "description": "Palm inventory, condition baselines, recurring monitoring, written reporting, and work coordination for HOAs, apartments, managers, institutions, commercial and municipal stakeholders.",
        "eyebrow": "Managed-property pathway", "h1": "Know every palm. Track every decision.",
        "lede": "A dedicated inventory and reporting pathway for HOAs, apartment communities, property managers, institutions, commercial properties, and municipal stakeholders.",
        "image": "Las Palmas_Appartments_Healthy-CIDP.jpg",
        "body": section("Portfolio clarity", "Managed-property Palm Inventory & Reporting", "The inventory gives each palm a stable identity and connects location, baseline photographs, visible condition, priority, work history, and next review.", cards([
            ("Palm inventory", "Stable asset IDs, mapped or described locations, species fields, and property context."),
            ("Condition baseline", "Dated views and visible-condition notes for each accessible palm."),
            ("Priority reporting", "A property-level view of immediate, near-term, routine, and watch-list decisions."),
            ("Monitoring timeline", "Repeat observations and image comparisons without losing the prior record."),
            ("Contractor coordination", "Share defined work scopes and record supplied completion information."),
            ("Stakeholder reporting", "Clear summaries for boards, managers, institutions, commercial owners, or municipal reviewers."),
        ])) + section("Verification boundary", "Contractor-work verification records evidence; it does not certify the unknowable.", "SDPP can document visible completion, dates, supplied records, and discrepancies within an agreed scope.", '<p class="note"><strong>Limitations:</strong> verification does not certify concealed work, workmanship, structural safety, legal or code compliance, pesticide efficacy, contractor licensing, or outcomes unless a separately qualified party and explicit scope support that conclusion.</p>', "section-tint") +
        section("Municipal context", "Accurate participation wording.", "San Diego Palm Protection submitted mature-palm documentation for consideration during the City of Escondido Urban Forest Management Plan process.", '<p class="note">This statement describes a submission for consideration. It does not state or imply City endorsement, partnership, selection, approval, or adoption.</p>')
    },
    "palm-removal-coordination.html": {
        "title": "Palm Decline, Removal & Replacement Coordination | SDPP",
        "description": "Document palm decline, coordinate urgent response and removal, preserve the loss record, and plan appropriate replacement.",
        "eyebrow": "Response pathway", "h1": "Decline, Removal & Replacement Coordination",
        "lede": "When a palm changes quickly or cannot reasonably remain, SDPP organizes the evidence, communication, contractor handoff, documented outcome, and next landscape decision.",
        "image": "dead-cidp-healthy-cidp-poway.jpg",
        "body": section("Response without overclaiming", "Separate what is visible from what is known.", "Decline may have multiple causes. The response record identifies observations, reported information, certainty, limitations, urgent concerns, and needed referrals.", process([
            ("Document", "Record current condition and immediate context."),
            ("Triage", "Identify urgency, access limits, and the appropriate responsible party."),
            ("Coordinate", "Prepare a clear contractor or specialist handoff."),
            ("Close the record", "Document visible completion, removal, loss, or replacement plan."),
        ])) + section("After decline", "The record continues.", "A removal is not the end of responsible documentation.", cards([
            ("Removal coordination", "Organize scope, site information, access, contractor communications, and outcome evidence."),
            ("Documented Loss", "Preserve confirmed outcome while keeping cause and attribution within the evidence."),
            ("Replacement planning", "Consider site constraints, long-term scale, sourcing, installation responsibilities, and monitoring."),
        ]), "section-tint")
    },
    "palm-proof-examples.html": {
        "title": "Sanitized Palm Assessment & Monitoring Examples | SDPP",
        "description": "Public presentation structure for approved sanitized sample assessments, inventories, monitoring timelines, report excerpts, case studies, and managed-property examples.",
        "eyebrow": "Public proof library", "h1": "See the structure of the work—without exposing a client.",
        "lede": "This page is ready to display only separately approved, sanitized exports from the canonical SDPP Machine. No private report or client record is copied into website source.",
        "image": "evidence.jpg",
        "body": section("Approved-export boundary", "Private source. Sanitized derivative. Separate public approval.", "Proof appears here only after the Machine produces a versioned public bundle that passes privacy, evidence, quality, metadata, media-use, and current-fingerprint gates.", cards([
            ("Sample assessment", "Public property descriptor, assessment purpose, visible-condition structure, limitations, and redacted deliverable excerpt."),
            ("Palm inventory", "Sanitized asset IDs, allowed fields, portfolio summary, and approved public imagery only."),
            ("Monitoring timeline", "Comparable dated events and change summaries without private identity, address, access, or contact details."),
            ("Written report excerpt", "A bounded example of reporting language, certainty, recommendations, and limitations."),
            ("Case study", "Approved facts and outcomes with source-property identity removed or generalized."),
            ("Managed-property example", "A neutral property descriptor, inventory logic, priorities, and stakeholder-ready summary."),
        ], "proof-grid")) + section("Current publication state", "The presentation slots are ready; no client proof bundle is installed.", "This is an intentional privacy-safe empty state. It does not invent performance claims or imply that a private assessment has public approval.", '<p class="note"><span class="proof-status">Awaiting separately approved sanitized export</span><br>The approved sanitized Karrie assessment can populate the sample-assessment and monitoring-proof areas only after the canonical Machine exports the public derivative. Private client identity, address, contact, access details, unapproved photos, and private report source remain outside this repository.</p>', "section-tint")
    },
    "report-a-palm.html": {
        "title": "Report a Palm or Request Review | San Diego Palm Protection",
        "description": "Qualified and insured private palm observation and photo-review inquiry with explicit permissions.",
        "eyebrow": "Private inquiry", "h1": "Report a Palm or Request Review",
        "lede": "Prepare a private email handoff. Nothing is published automatically, and this page does not upload or store photographs.",
        "image": "evidence1.jpg",
        "body": section("Private handoff", "Prepare the record before opening email.", "The report is not delivered until you send it from your configured email application.", f'''{credentials("BUSINESS_CREDENTIALS_CONTACT")}
<form id="observation-form" novalidate>
<fieldset><legend>About you</legend><div class="form-grid"><div><label for="name">Name</label><input id="name" name="name" required></div><div><label for="email">Email</label><input id="email" name="email" type="email" required></div></div></fieldset>
<fieldset><legend>The observation</legend><div class="form-grid"><div><label for="city">City</label><input id="city" name="city" required></div><div><label for="category">Category</label><select id="category" name="category" required><option value="">Choose one</option><option>Baseline</option><option>Visible decline</option><option>Removal or loss</option><option>Other</option></select></div><div class="full"><label for="description">Observation and chronology:</label><textarea id="description" name="description" required></textarea></div></div></fieldset>
<fieldset><legend>Permissions</legend><label class="check"><input type="checkbox" name="contact_permission" required> SDPP may contact me to clarify this observation.</label><label class="check"><input type="checkbox" name="private_retention_permission" required> SDPP may retain this submission privately for review.</label><label class="check"><input type="checkbox" name="public_use_permission"> Separately and optionally, SDPP may ask about public editorial use.</label></fieldset>
<p class="note">Nothing is published automatically; identifiable private-property details remain private unless separately agreed. This page does not upload or store photographs. Review status: needs_review.</p>
<button class="button" type="submit">Prepare Email Report</button> <span id="form-status" role="status" aria-live="polite"></span></form>
<script>(()=>{{const form=document.getElementById('observation-form'),status=document.getElementById('form-status');form.addEventListener('submit',e=>{{e.preventDefault();if(!form.checkValidity()){{form.reportValidity();return;}}const data=new FormData(form),v=k=>String(data.get(k)||'').trim();const body=['REPORT A PALM — NEEDS REVIEW',`Name: ${{v('name')}}`,`Email: ${{v('email')}}`,`City: ${{v('city')}}`,`Category: ${{v('category')}}`,'Observation and chronology:',v('description'),'Contact permission: yes','Private retention permission: yes',`Optional public-use follow-up permission: ${{data.has('public_use_permission') ? 'yes' : 'no'}}`,'Review status: needs_review'].join('\\n');status.textContent='Opening your configured email application. Attach photographs there, then send; nothing has been delivered yet.';location.href=`mailto:sandiegopalmprotection@gmail.com?subject=${{encodeURIComponent('Palm observation')}}&body=${{encodeURIComponent(body)}}`;}});}})();</script>''')
    },
}


GENERIC = {
    "palm-stewardship-plans.html": ("Protection & Treatment Planning", "Protection & Treatment", "Qualified protection planning connects observations, diagnosis boundaries, site constraints, label requirements, authorization, treatment records, and monitoring.", "treatment.jpg"),
    "sapw.html": ("South American Palm Weevil: Evidence & Next Steps", "Palm risk education", "Learn observable warning signs, evidence limits, urgent response considerations, and when a qualified site assessment is appropriate.", "south-american-palm-weevil-cidp-poway.jpg"),
    "south-american-palm-weevil-treatment-san-diego.html": ("South American Palm Weevil Protection & Treatment", "Protection & Treatment", "Treatment decisions require a supported scope, current authorization, label compliance, site context, and a documented monitoring plan.", "treatment.jpg"),
    "canary-island-date-palm-care-san-diego.html": ("Canary Island Date Palm Assessment & Care", "Species pathway", "Assessment, baseline documentation, monitoring, protection planning, and response for significant Canary Island date palms.", "CIDP_big.jpg"),
    "cidp-risk-checklist.html": ("Canary Island Date Palm Risk Checklist", "Educational checklist", "A practical observation checklist to prepare for an assessment without substituting a diagnosis or safety evaluation.", "poway-what-does-sapw-look-like-cidp.jpg"),
    "old-escondido-palm-preservation.html": ("Old Escondido Mature Palm Documentation", "Community documentation", "A preservation-focused pathway for baseline records, monitoring, managed-property coordination, and accurate municipal context.", "beautiful-old_escondido-cidp.jpg"),
    "palm-care-escondido.html": ("Palm Assessment & Monitoring in Escondido", "Local service pathway", "Residential and managed-property palm assessment, baselines, monitoring, protection planning, and decline response in Escondido.", "Old-Escondido_full-CIDP.jpg"),
    "palm-care-poway.html": ("Palm Assessment & Monitoring in Poway", "Local service pathway", "Residential and managed-property palm assessment, baselines, monitoring, protection planning, and decline response in Poway.", "Healthy-CIDP-Poway.jpg"),
    "palm-care-rancho-santa-fe.html": ("Palm Assessment & Monitoring in Rancho Santa Fe", "Local service pathway", "Discreet residential and estate palm assessment, condition baselines, monitoring, protection planning, and decline response.", "RSF1.jpg"),
    "palm-faq-san-diego.html": ("Palm Assessment & Monitoring FAQ", "Education & decision support", "Clear answers about assessments, monitoring, treatment boundaries, reporting, managed properties, decline, and proof privacy.", "journal-overview.jpg"),
    "palm-sourcing-installation.html": ("Palm Sourcing, Installation & Replacement Planning", "Response, Removal & Replacement", "Replacement planning connects site constraints, appropriate selection, sourcing questions, installation responsibilities, baseline documentation, and establishment monitoring.", "Bismarck-Specimen-Escondido.jpg"),
    "specimen-palms-cycads.html": ("Specimen Palms & Cycads", "Replacement planning", "Explore significant palm and cycad landscape possibilities with realistic site, sourcing, installation, documentation, and establishment considerations.", "Bismarck.jpg"),
}


def generic_body(name: str) -> str:
    return section("Connected service", "A record before, during, and after the decision.", "This pathway fits inside the same three-pillar system used across the site.", three_pillars()) + section("What to expect", "Defined scope. Usable documentation. Explicit limits.", "The work begins by identifying the property, palm, question, evidence, access, responsible parties, and decision deadline.", cards([
        ("Assessment and baseline", "Document visible condition and establish comparable photographs."),
        ("Written next steps", "Separate observations, possible concerns, recommendations, and limitations."),
        ("Monitoring or response", "Set an appropriate review interval or coordinate the next responsible action."),
    ]), "section-tint")


def write_pages() -> None:
    pages = dict(PAGES)
    for filename, (h1, eyebrow, lede, image) in GENERIC.items():
        pages[filename] = {
            "title": f"{h1} | San Diego Palm Protection",
            "description": lede,
            "eyebrow": eyebrow, "h1": h1, "lede": lede, "image": image,
            "body": generic_body(filename),
        }
    for filename, data in pages.items():
        schema = {
            "@context": "https://schema.org", "@type": "Service",
            "provider": {"@type": "LocalBusiness", "name": "San Diego Palm Protection", "url": BASE_URL},
            "name": data["h1"], "areaServed": "North County San Diego",
            "description": data["description"],
        }
        (ROOT / filename).write_text(page(filename=filename, extra_schema=schema, **data), encoding="utf-8")
    (ROOT / "site-config" / "core_routes.json").write_text(json.dumps(sorted(pages), indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(pages)} canonical core pages.")


if __name__ == "__main__":
    write_pages()
