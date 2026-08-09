from __future__ import annotations

from html import escape
from pathlib import Path
import json

from site_components import ROOT, BASE_URL, page, three_pillars, credentials, compact_credentials, INQUIRY

UFMP_RESOURCE = json.loads((ROOT / "site-config" / "ufmp_resource.json").read_text(encoding="utf-8"))
POSITIONING = json.loads((ROOT / "site-config" / "positioning.json").read_text(encoding="utf-8"))


def section(eyebrow: str, heading: str, intro: str, content: str, classes: str = "") -> str:
    return f'<section class="section {classes}"><div class="section-intro"><p class="eyebrow">{escape(eyebrow)}</p><h2>{escape(heading)}</h2><p>{escape(intro)}</p></div>{content}</section>'


def cards(items: list[tuple[str, str]], cls: str = "service-grid") -> str:
    count_class = f" {cls}--{len(items)}" if cls == "service-grid" else ""
    return f'<div class="{cls}{count_class}">' + "".join(f'<article class="service-card"><h3>{escape(h)}</h3><p>{escape(p)}</p></article>' for h, p in items) + "</div>"


def process(items: list[tuple[str, str]]) -> str:
    return '<div class="process">' + "".join(f'<div><h3>{escape(h)}</h3><p>{escape(p)}</p></div>' for h, p in items) + "</div>"


def commercial_engagement_paths() -> str:
    return '''<section class="section section-tint commercial-engagements" aria-labelledby="commercial-engagements-heading">
  <div class="section-intro"><p class="eyebrow">Two engagement paths</p><h2 id="commercial-engagements-heading">Start with a baseline or build the annual relationship.</h2><p>A property can begin with a defined record before deciding on recurring stewardship. Standardize the stewardship system; customize the property scope.</p></div>
  <div class="audience-grid audience-grid--2">
    <article class="audience-card" data-engagement-path="palm-portfolio-baseline"><h3>Palm Portfolio Baseline</h3><p>A defined first engagement for a property without an organized palm record.</p><ul><li>Property walkthrough and known-history intake</li><li>Priority-palm identities, photographs, and visible conditions</li><li>Immediate concerns and preservation priorities</li><li>Recommended care, treatment, documentation, and coordination scope</li><li>Proposal for continuing work</li></ul></article>
    <article class="audience-card" data-engagement-path="annual-palm-stewardship-program"><h3>Annual Palm Stewardship Program</h3><p>The recurring relationship, tailored to the palms and management responsibilities.</p><ul><li>Maintained palm register and scheduled care</li><li>Licensed preventive protection and treatment within scope</li><li>Dated condition, treatment, and supplied work history</li><li>Material-change alerts and preservation priorities</li><li>Specialist coordination and next-cycle planning</li></ul></article>
  </div>
</section>'''


def inquiry_paths() -> str:
    explanation = escape(INQUIRY["public_explanation"])
    return f'''<div class="inquiry-paths">
<details class="inquiry-panel" id="homeowner-inquiry">
  <summary><span class="eyebrow">For homeowners</span><span class="inquiry-summary-title">Request a Palm Assessment</span><span>For one palm or a small residential group.</span></summary>
  <form data-inquiry-direct data-inquiry-type="homeowner" data-fallback-conversion="homeowner-inquiry-email-prepared" action="/api/inquiry" method="post">
    <input type="hidden" name="inquiry_type" value="homeowner">
    <div class="form-trap" aria-hidden="true"><label for="home-website">Website</label><input id="home-website" name="website" tabindex="-1" autocomplete="off"></div>
    <div class="form-grid">
      <div><label for="home-name">Name</label><input id="home-name" name="name" autocomplete="name" required></div>
      <div><label for="home-email">Email</label><input id="home-email" name="email" type="email" autocomplete="email" required></div>
      <div><label for="home-phone">Phone</label><input id="home-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div><label for="home-city">Property city</label><input id="home-city" name="property_city" autocomplete="address-level2" required></div>
      <div><label for="home-species">Palm type, if known</label><input id="home-species" name="palm_type"></div>
      <div><label for="home-count">Number of palms</label><input id="home-count" name="number_of_palms" inputmode="numeric"></div>
      <div class="full"><label for="home-concern">What are you seeing or trying to decide?</label><textarea id="home-concern" name="concern" required></textarea></div>
      <div><label for="home-contact">Preferred contact method</label><select id="home-contact" name="preferred_contact"><option>Phone</option><option>Text</option><option>Email</option></select></div>
      <div><label for="home-timing">Timing or urgency</label><input id="home-timing" name="timing"></div>
    </div>
    <p class="form-help">Photograph uploads are not enabled. SDPP can request photographs during follow-up.</p>
    <p class="form-help">Information submitted through this form is used to respond to your inquiry and evaluate the requested palm or property service.</p>
    <p class="form-help">{explanation}</p>
    <div data-turnstile-container></div>
    <button class="button" type="submit">Submit Homeowner Inquiry</button>
    <p><a data-conversion="direct-email-fallback" href="mailto:sandiegopalmprotection@gmail.com?subject=Homeowner%20palm%20inquiry">Prefer email? Send your inquiry directly</a><br><small>Your email application will open. Your inquiry is not sent until you send it.</small></p>
    <p class="form-status" data-form-status aria-live="polite"></p>
  </form>
</details>
<details class="inquiry-panel" id="organization-inquiry">
  <summary><span class="eyebrow">For commercial and managed properties</span><span class="inquiry-summary-title">Request a Property Walkthrough</span><span>For managed properties, portfolios, and estates.</span></summary>
  <form data-inquiry-direct data-inquiry-type="organization" data-fallback-conversion="organization-inquiry-email-prepared" action="/api/inquiry" method="post">
    <input type="hidden" name="inquiry_type" value="organization">
    <div class="form-trap" aria-hidden="true"><label for="org-website">Website</label><input id="org-website" name="website" tabindex="-1" autocomplete="off"></div>
    <div class="form-grid">
      <div><label for="org-name">Contact name</label><input id="org-name" name="contact_name" autocomplete="name" required></div>
      <div><label for="org-email">Work email</label><input id="org-email" name="email" type="email" autocomplete="email" required></div>
      <div><label for="org-phone">Phone</label><input id="org-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div><label for="org-organization">Property or organization name</label><input id="org-organization" name="organization" autocomplete="organization" required></div>
      <div><label for="org-role">Your role</label><input id="org-role" name="role" required></div>
      <div><label for="org-property">Property address or city</label><input id="org-property" name="property_or_service_area" required></div>
      <div><label for="org-count">Approximate number of palms</label><input id="org-count" name="approximate_palm_count" inputmode="numeric"></div>
      <div><label for="org-species">Known palm species, if any</label><input id="org-species" name="known_palm_species"></div>
      <div><label for="org-contractor">Existing landscape or tree contractor, if relevant</label><input id="org-contractor" name="existing_contractor"></div>
      <div><label for="org-service">Desired service</label><select id="org-service" name="desired_service" required><option value="">Select one</option><option>Palm portfolio walkthrough</option><option>Palm inventory or baseline</option><option>Preventive treatment</option><option>Recurring monitoring</option><option>Palm stewardship</option><option>Decline or removal coordination</option></select></div>
      <div><label for="org-contact">Preferred contact method</label><select id="org-contact" name="preferred_contact"><option>Phone</option><option>Text</option><option>Email</option></select></div>
      <div class="full"><label for="org-scope">Current concern or property objective</label><textarea id="org-scope" name="support_requested" required></textarea></div>
      <div class="full"><label for="org-timing">Timing or procurement context</label><input id="org-timing" name="timing"></div>
    </div>
    <p class="form-help">Supporting-file uploads are not enabled. SDPP can request photographs or records during follow-up.</p>
    <p class="form-help">Information submitted through this form is used to respond to your inquiry and evaluate the requested palm or property service.</p>
    <p class="form-help">{explanation}</p>
    <div data-turnstile-container></div>
    <button class="button" type="submit">Request a Property Walkthrough</button>
    <p><a data-conversion="direct-email-fallback" href="mailto:sandiegopalmprotection@gmail.com?subject=Managed-property%20palm%20portfolio%20inquiry">Prefer email? Tell me about the palm portfolio</a><br><small>Your email application will open. Your inquiry is not sent until you send it.</small></p>
    <p class="form-status" data-form-status aria-live="polite"></p>
  </form>
</details>
</div>'''


def approved_ufmp_resource() -> str:
    resource = UFMP_RESOURCE
    sections = "".join(
        f'<section class="ufmp-copy-block"><h3>{escape(item["heading"])}</h3><p>{escape(item["body"])}</p></section>'
        for item in resource["sections"]
    )
    figures = "".join(
        f'''<figure>
  <img src="./images/old-escondido-urban-forest-documentation/{escape(item["filename"])}" alt="{escape(item["alt"])}" loading="lazy" decoding="async">
  <figcaption>{escape(item["caption"])}</figcaption>
</figure>'''
        for item in resource["media"]
    )
    capability = "".join(f"<p>{escape(item)}</p>" for item in resource["large_property_civic_capability"])
    journal = "".join(f"<p>{escape(item)}</p>" for item in resource["palm_journal"]["paragraphs"])
    return f'''<section class="section ufmp-approved-resource" id="old-escondido-documentation-method" aria-labelledby="old-escondido-documentation-heading">
  <div class="section-intro">
    <p class="eyebrow">Approved civic documentation resource</p>
    <h2 id="old-escondido-documentation-heading">{escape(resource["title"])}</h2>
    <p>{escape(resource["summary"])}</p>
    <div class="button-row">
      <a class="button" href="./{escape(resource["pdf"]["filename"])}" target="_blank" rel="noopener noreferrer">Download the civic documentation packet <span class="sr-only">(PDF, opens in a new tab)</span></a>
      <a class="sample-request-link" href="{escape(resource["page_action"]["href"])}">{escape(resource["page_action"]["label"])}</a>
    </div>
    <p class="note">{escape(resource["page_action"]["supporting_copy"])}</p>
  </div>
  <div class="ufmp-copy-grid">{sections}</div>
  <div class="ufmp-photo-grid">{figures}</div>
</section>
<section class="section section-tint" id="large-property-civic-capability">
  <div class="section-intro"><p class="eyebrow">Large-property and civic documentation capability</p><h2>Records that keep each palm and decision connected.</h2></div>
  <div class="article-shell">{capability}</div>
</section>
<section class="section" id="old-escondido-palm-journal-fragment">
  <div class="section-intro"><p class="eyebrow">Palm Journal fragment</p><h2>{escape(resource["palm_journal"]["heading"])}</h2></div>
  <div class="article-shell">{journal}</div>
</section>
<section class="section section-tint" aria-labelledby="ufmp-related-resources">
  <div class="section-intro"><p class="eyebrow">Related resources</p><h2 id="ufmp-related-resources">Continue through the existing documentation pathways.</h2></div>
  <div class="field-links">
    <a href="./managed-property-palm-services.html">Commercial &amp; Managed</a>
    <a href="./palm-proof-examples.html">Field Work</a>
    <a href="./palm-journal-new.html">Palm Journal</a>
    <a href="./palm-journal/documented-loss/">Documented Loss</a>
  </div>
</section>'''


PAGES: dict[str, dict] = {
    "index.html": {
        "title": "Palm Portfolio Stewardship & Treatment San Diego | SDPP",
        "description": "Owner-led palm portfolio stewardship, condition records, recurring planning, and licensed treatment for managed properties and valuable mature palms in San Diego.",
        "eyebrow": "Owner-led · San Diego County · Based in Old Escondido",
        "h1": POSITIONING["homepage_headline"],
        "lede": POSITIONING["homepage_supporting_copy"],
        "image": "background.jpg",
        "body": section("Commercial & managed properties", "Palm portfolios, managed with continuity.", "Each priority palm can have an identity, baseline, condition and service history, recurring schedule, and next action. I stay directly involved from the first walkthrough through licensed treatment, documentation, follow-up, and coordination with qualified specialists when needed.", '<p>The starting point is a property walkthrough: understand the palms, the site, the existing landscape team, and the decisions the property is responsible for.</p><div class="button-row"><a class="button" data-conversion="organization-inquiry-initiation" href="./palm-records-monitoring-verification.html#organization-inquiry">Request a Property Walkthrough</a><a class="button button-secondary" href="./managed-property-palm-services.html">See the Stewardship Model</a></div>', "section-tint") +
        section("One stewardship model", "Care, records, and response stay connected.", "The property and agreed scope determine the work.", three_pillars()) +
        section("Who I work with", "Palm protection for valuable properties.", "The work is shaped by the palms, the property, and the decisions that need to be made.", '<div class="audience-grid audience-grid--2"><article class="audience-card"><h3>Commercial &amp; Managed Properties</h3><p>For managed properties, I can build a practical stewardship plan across the palm portfolio—documenting conditions, identifying priorities, scheduling recurring care, supporting budget decisions, and maintaining continuity from one visit to the next.</p><a data-conversion="organization-inquiry-initiation" href="./palm-records-monitoring-verification.html#organization-inquiry">Discuss a multi-palm property</a></article><article class="audience-card"><h3>Residential &amp; Estate Properties</h3><p>For homeowners and estate owners, stewardship means having one knowledgeable person consistently looking after the palms rather than addressing each concern as an isolated event.</p><a data-conversion="homeowner-inquiry-initiation" href="./palm-records-monitoring-verification.html#homeowner-inquiry">Tell me about your palm</a></article></div>') +
        section("Field work", "See the evidence behind the service.", "Review local observations, sample reporting, and documented outcomes.", '<div class="field-links"><a href="./palm-proof-examples.html">View Field Work</a><a href="./palm-journal-new.html">Read the Palm Journal</a><a href="./palm-journal/documented-loss/">Visit Documented Loss</a></div>', "section-tint"),
    },
    "about.html": {
        "title": "About San Diego Palm Protection | Owner-Led Palm Services",
        "description": "Meet John Krause, the owner-led specialist providing palm stewardship for managed properties and important residential palms in San Diego County.",
        "eyebrow": "About San Diego Palm Protection",
        "h1": "I look at the palm, take the photographs, and write the report.",
        "lede": "SDPP began after South American palm weevil activity and palm loss reached my own Old Escondido property.",
        "image": "beautiful-old_escondido-cidp.jpg",
        "body": section("About John", "Local experience shapes how I approach the work.", "SDPP grew from firsthand experience with the threat facing the mature palms that help define Old Escondido and other San Diego communities.", '''<div class="about-john-profile">
<figure class="about-john-photo">
  <picture>
    <source type="image/webp" srcset="./images/about-john/john-krause-palm-640.webp 640w, ./images/about-john/john-krause-palm-960.webp 960w, ./images/about-john/john-krause-palm-1280.webp 1280w" sizes="(max-width: 700px) calc(100vw - 32px), 42vw">
    <img src="./images/about-john/john-krause-palm-960.jpg" width="960" height="1280" alt="John Krause standing beneath a mature Canary Island date palm at his Old Escondido property" loading="eager" decoding="async" fetchpriority="high">
  </picture>
</figure>
<div class="about-john-story">
  <div class="about-john-copy">
    <p>I started SDPP after confronting South American palm weevil activity and palm loss on my own Old Escondido property. That experience made the threat very real to me&mdash;and made me look more closely at how many mature palms across our neighborhoods could be lost without earlier attention.</p>
    <p>Wisconsin native with an Environmental Science B.S. from the University of Minnesota and time in the Naval Service.</p>
    <p>Today, based in Old Escondido, I provide owner-led palm assessments, monitoring, protection, and treatment services throughout San Diego County. I built SDPP to give palm owners a knowledgeable local point of contact&mdash;someone who will personally look at the tree, explain what is visible, maintain useful records, and help determine a responsible next step.</p>
  </div>
  <div class="about-john-marks">
    <img class="about-john-mark about-john-mark--umn" src="./images/about-john/education/university-of-minnesota-block-m.svg" alt="University of Minnesota Block M mark" width="124" height="68" loading="lazy" decoding="async">
    <img class="about-john-mark about-john-mark--iu" src="./images/about-john/education/indiana-university-trident.svg" alt="Indiana University Trident mark" width="56" height="68" loading="lazy" decoding="async">
  </div>
</div>
</div>''') +
        '''<section class="section section-tint"><div class="article-shell">
<h2>We Protect What Cannot Be Quickly Replaced</h2>
<p>Southern California’s mature palms define estates, resorts, communities, civic spaces, and historic neighborhoods. They represent decades of growth and cannot be replaced on demand.</p>
<p>The South American palm weevil does not wait for owners, contractors, or agencies to organize. SDPP exists to act before visible decline narrows the opportunity for preservation.</p>
</div></section>
<section class="section"><div class="article-shell">
<h2>Stewardship Means Continuity</h2>
<p>Palm care is often fragmented among landscapers, arborists, applicators, researchers, and public agencies. No one necessarily maintains continuous responsibility for the palm itself—its identity, condition, history, treatment record, and next action.</p>
<p>SDPP closes that gap with baselines, monitoring, preventive treatment, useful records, and coordinated follow-through.</p>
<p>We do not sell fear or exaggerate certainty. We distinguish observation from diagnosis, evidence from inference, and confidence from speculation.</p>
<p>We work alongside existing professionals while keeping responsibility for the palm from disappearing between contractors.</p>
<p>That is palm stewardship.</p>
</div></section>''' +
        section("Qualification and scope", "Qualified, insured, and operating within a defined service boundary.", "I hold California Qualified Applicator License No. 175295, Category B — Landscape Maintenance. The license supports appropriate treatment within a broader owner-led palm stewardship service.", '<p class="note">Treatment follows the pesticide label, applicable law, site conditions, and agreed scope. I do not promise diagnosis from photographs, treatment efficacy, palm recovery, or guaranteed outcomes.</p>') +
        section("Start a conversation", "Choose the inquiry path that fits.", "Homeowners can request an assessment. Managers, HOAs, institutions, and other property stakeholders can discuss a palm portfolio.", '<div class="button-row"><a class="button" data-conversion="homeowner-inquiry-initiation" href="./palm-records-monitoring-verification.html#homeowner-inquiry">Request a Palm Assessment</a><a class="button" data-conversion="organization-inquiry-initiation" href="./palm-records-monitoring-verification.html#organization-inquiry">Discuss a Property or Palm Portfolio</a></div>', "section-tint"),
    },
    "residential-palm-assessment.html": {
        "title": "Palm Health Assessment San Diego | Residential Palm Care",
        "description": "On-site palm health assessment for declining, damaged, or changing mature palms, with dated photographs, written findings, and practical next steps.",
        "eyebrow": "On-site residential service", "h1": "Palm Health Assessment for Mature Palms",
        "lede": "I come to the property, look at the whole palm from the ground, photograph what concerns you, and explain whether monitoring, treatment, confirmation, or urgent response fits what I find.",
        "image": "mature_healthy_cidp_poway_mansion.jpg",
        "body": section("What I deliver", "A dated starting point for your palm.", "I photograph the entire palm, its crown, trunk, base, and any concern I can safely see. Those photographs give us something real to compare later.", cards([
            ("The palm and its setting", "I note where it stands, what can be accessed safely, and what prompted the visit."),
            ("Dated photographs", "I take whole-palm and detail views that can be repeated during a future visit."),
            ("What I observed", "I separate what I saw from what you reported, what I suspect, and what would need confirmation."),
            ("Your written report", "You receive the photographs, findings, limits of the visit, and the next steps I recommend."),
        ]) + '<p class="section-proof-link"><a href="./palm-proof-examples.html">View field work and reporting</a></p>') + section("What it is not", "Useful because its limits are explicit.", "A visual assessment cannot promise tree safety, uncover hidden conditions, replace laboratory confirmation, or guarantee an outcome.", '<p class="note">Urgent structural or life-safety concerns may require an emergency contractor or other specialist.</p>', "section-tint") +
        section("If the palm needs watching", "The first visit becomes the comparison point.", "When I return, I try to repeat the same views. That makes it easier to see whether the crown, trunk, or surrounding conditions have changed.", process([("Before the visit", "Tell me what changed and send any older photographs you have."), ("At the property", "I observe and photograph the areas I can access safely."), ("Afterward", "You receive the dated report and a recommended time for another look, if one is useful.")]) + '<p class="section-proof-link"><a href="./about.html">Learn more about John Krause</a></p>')
    },
    "palm-records-monitoring-verification.html": {
        "title": "Palm Assessment, Monitoring & Management Services | SDPP",
        "description": "Palm assessment, condition baselines, recurring monitoring, treatment records, portfolio reporting, and decline response for San Diego properties.",
        "eyebrow": "Palm services in San Diego County", "h1": "Palm assessment, monitoring, and management services.",
        "lede": "I connect the site visit, photographs, treatment decisions, recurring care, and written record so owners and managers know what each important palm needs next.",
        "image": "journal-monitoring.jpg",
        "body": section("Assessment, Monitoring & Documentation", "You receive work you can actually use.", "The photographs and report are part of the service.", cards([
            ("Residential Mature Palm Assessment", "I visit, examine the palm from the ground, take photographs, and write down what I found."),
            ("Palm Condition Baseline", "A dated set of repeatable photographs before a concern becomes harder to reconstruct."),
            ("Recurring Palm Monitoring", "I return at an agreed interval and compare the palm with the earlier images."),
            ("Managed-property Palm Inventory & Reporting", "Each palm gets an ID, photographs, current notes, and a place in the property summary."),
            ("Written Palm Condition Report", "A readable account of the visit, including what I know, what I do not know, and what I recommend."),
            ("Contractor-Work Verification", "I can photograph completed work and organize the records the contractor provides. I cannot verify work hidden from view."),
        ]), "section-tint") +
        section("How it works", "Tell me what you are trying to decide.", "I will ask about the palm, the property, access, and recent history before we agree on the visit.", process([
            ("First conversation", "Tell me what you have noticed and share any older photographs or work history."),
            ("Property visit", "I look at what can be seen safely from the ground and take the needed photographs."),
            ("Written findings", "I send a dated account of the visit with priorities, uncertainties, and recommendations."),
            ("What comes next", "I may recommend monitoring, protection or treatment, contractor work, removal, or replacement."),
        ])) +
        section("Request", "Choose the direct inquiry path.", "Open the form that fits the property.", f'{compact_credentials("BUSINESS_CREDENTIALS_CONTACT")}{inquiry_paths()}<p class="section-proof-link"><a href="./palm-removal-coordination.html">Removal coordination</a> · <a href="./palm-sourcing-installation.html">Palm sourcing and installation</a> · <a href="./specimen-palms-cycads.html">Specimen palms and cycads</a> · <a href="./palm-journal/documented-loss/">Documented Loss</a></p>').replace('<section class="section ">', '<section class="section " id="request">', 1)
    },
    "quarterly-palm-care-san-diego.html": {
        "title": "Palm Stewardship & Mature Palm Preservation San Diego | SDPP",
        "description": "Recurring palm stewardship for mature-palm preservation, including health visits, fertilization, irrigation review, preventive treatment, and monitoring.",
        "eyebrow": "Recurring stewardship", "h1": "Palm stewardship and preservation, visit after visit.",
        "lede": "Return visits keep palm health, care, protection, treatment history, and changing priorities connected over time. The schedule follows the palms, the property, and the agreed scope.",
        "image": "journal-seasonal.jpg",
        "body": section("Recurring care", "Each visit advances the stewardship plan.", "I review current palm health and site conditions, carry out agreed care within scope, and keep the history useful for the next decision.", process([
            ("Observe", "Review palm health, site conditions, watering or irrigation concerns, and changes since the prior visit."),
            ("Care", "Address agreed fertilization, preventive protection, or treatment when appropriate for the palm and property."),
            ("Record", "Update comparable photographs, condition notes, treatment and work history, and portfolio priorities."),
            ("Plan", "Set the next visit, budget priority, contractor question, or response step."),
        ])) + section("Choosing the interval", "The timing follows the palms and the work.", "A quarterly schedule can be useful, but it is not automatically right for every property. I explain the proposed rhythm and what each return visit is meant to accomplish.", cards([
            ("Managed-property stewardship", "Maintain recurring hands-on care, a multi-palm history, work status, priorities, and planning continuity."),
            ("Estate and residential care", "Follow a significant palm after a baseline, treatment, contractor work, storm exposure, or a new concern."),
            ("Response", "Adjust monitoring, protection, treatment, coordination, removal, or replacement planning when the evidence supports it."),
        ]), "section-tint")
    },
    "managed-property-palm-services.html": {
        "title": "Palm Portfolio Stewardship for Managed Properties | SDPP",
        "description": "Owner-led palm portfolio stewardship, asset records, recurring care planning, licensed treatment, and coordinated response for managed properties in San Diego.",
        "eyebrow": "Commercial and managed properties", "h1": "Palm Portfolio Stewardship for Managed Properties",
        "lede": POSITIONING["canonical_position"] + " " + POSITIONING["stewardship_distinction"],
        "image": "Las Palmas_Appartments_Healthy-CIDP.jpg",
        "body": section("The stewardship role", "What SDPP takes responsibility for.", "The agreed scope keeps the palm inventory, care, records, and next actions connected.", cards([
            ("Stewardship & Palm Health", "Maintain palm identities, visible conditions, priorities, and the recurring schedule."),
            ("Protection & Treatment", "Provide preventive care and licensed treatment when appropriate and within scope."),
            ("Documentation & Portfolio Management", "Maintain condition, treatment, and supplied work history for planning."),
            ("Response, Removal & Renewal", "Coordinate focused handoffs with landscapers, arborists, removal contractors, and other specialists."),
        ])) + commercial_engagement_paths() +
        section("Defined deliverables", "What ongoing stewardship can include.", "Deliverables follow the agreed property scope.", cards([
            ("Palm asset register", "Stable IDs, locations, supportable species, and current status."),
            ("Baseline condition record", "Dated photographs, visible observations, known history, and priorities."),
            ("Recurring stewardship plan", "A schedule for observation, care, protection, treatment, and review."),
            ("Dated visit and treatment records", "SDPP service records, supplied contractor history, and completed actions."),
            ("Material-change alerts", "Significant visible change and the recommended next action."),
            ("Periodic portfolio summary", "Priorities, unresolved items, planned work, and budgeting considerations."),
        ]) + '''<div class="document-preview-shell commercial-overview-inline" aria-label="Commercial overview">
  <object class="document-preview" data="./SDPP-Commercial-Palm-Stewardship.pdf#view=FitH&amp;toolbar=1" type="application/pdf" aria-label="SDPP Commercial Palm Stewardship overview"><p>Your browser cannot display the PDF here. Use the links below.</p></object>
  <div class="document-actions"><a class="button" href="./SDPP-Commercial-Palm-Stewardship.pdf" target="_blank" rel="noopener noreferrer">View Commercial Overview <span class="sr-only">(PDF, opens in a new tab)</span></a><a class="text-link" href="./SDPP-Commercial-Palm-Stewardship.pdf" download>Download Commercial Overview</a></div>
</div>''') +
        section("Representative proof", "See the kind of palm-level record a property manager can use.", "This sanitized Old Escondido example demonstrates a repeatable multi-palm record without exposing private client information.", '<p><a class="button" href="./old-escondido-mature-palm-documentation-example.pdf" target="_blank" rel="noopener noreferrer">View the representative documentation example <span class="sr-only">(PDF, opens in a new tab)</span></a> <a href="./palm-proof-examples.html">View Field Work</a></p>', "section-tint") +
        section("Existing property teams", "SDPP does not need to replace the landscape team.", "I work alongside existing landscapers, maintain the palm record, perform agreed licensed work, and coordinate specialized action.", '<p class="note">Monitoring and treatment cannot guarantee survival or pest exclusion. Coordination does not imply supervision or verification of hidden work, workmanship, structural safety, code compliance, licensing, efficacy, or outcomes.</p>', "section-tint") +
        section("Next step", "Start with the property and its palms.", "A walkthrough establishes the scope, priorities, and records the property needs.", '<p><a class="button" data-conversion="organization-inquiry-initiation" href="./palm-records-monitoring-verification.html#organization-inquiry">Request a Property Walkthrough</a> <a href="./urban-forest-palm-documentation.html">Municipal and urban-forest support</a></p>')
    },
    "urban-forest-palm-documentation.html": {
        "title": UFMP_RESOURCE["metadata"]["title"],
        "description": UFMP_RESOURCE["metadata"]["description"],
        "eyebrow": "Municipal and managed-property support",
        "h1": "Palm Inventory, Condition Documentation & Urban Forest Support",
        "lede": "Specialized palm-focused field information and records for municipalities, public agencies, historic districts, managed properties, institutions, consultants, and contractors responsible for mature palms.",
        "image": "Old-Escondido_full-CIDP.jpg",
        "body": section("Who this is for", "Support for people responsible for public or shared landscapes.", "Projects are scoped for cities and public agencies, urban forestry teams, parks and public works departments, historic districts, HOAs, commercial portfolios, schools and campuses, landscape architects, arborists, consultants, and palm-maintenance contractors.", cards([
            ("Public and civic stakeholders", "Palm-focused records for defined public properties, corridors, districts, or implementation priorities."),
            ("Managed and institutional portfolios", "Repeatable information for boards, managers, campuses, commercial owners, and facilities teams."),
            ("Consultants and contractors", "A consistent palm record that can support planning, communication, and documented follow-through."),
        ])) +
        section("What SDPP documents", "Field information designed to remain useful.", "The agreed data structure can connect a palm’s identity, place, visible condition, work history, and next review.", cards([
            ("Identity and location", "Stable palm IDs, species records where supportable, location descriptions, and requested spreadsheet- or GIS-ready fields defined by contract."),
            ("Photographic baseline", "Dated overview, crown, trunk, site, and visible-condition photographs where access safely permits."),
            ("Condition observations", "Defined observation categories, priority or escalation flags, limitations, and recommended next actions."),
            ("Repeat records", "Monitoring comparisons, treatment history when supplied, work status, removals, documented loss, and replacement tracking."),
        ]), "section-tint") +
        section("Example deliverables", "Palm-level detail and portfolio-level summaries.", "Deliverables are selected for the project rather than implied as a universal package.", cards([
            ("Palm inventory", "Stable IDs, species and location fields, dated photographs, observation categories, and current status."),
            ("Priority and portfolio summary", "Grouped findings, escalation flags, maintenance priorities, unresolved items, and planned revisit points."),
            ("Contractor verification record", "Before-and-after photographs, supplied service information, visible completion, and discrepancies within scope."),
            ("Export-ready records", "Spreadsheet-ready tables and, when specifically requested and contractually defined, fields prepared for GIS use."),
        ])) +
        section("Field workflow", "From project definition to a maintained record.", "A concise workflow keeps data collection tied to the decisions it is intended to support.", process([
            ("Define", "Confirm geography, palm population, fields, access, stakeholders, and required outputs."),
            ("Inventory", "Assign stable IDs and record location, species fields, photographs, and visible conditions."),
            ("Prioritize", "Separate routine items, monitoring needs, escalation flags, and evidence gaps."),
            ("Report", "Deliver palm-level records, portfolio summaries, limitations, and recommended next actions."),
            ("Maintain", "Add repeat monitoring, work verification, removal, loss, or replacement records when commissioned."),
        ])) +
        section("UFMP and urban-forest implementation support", "Specialized palm information can support a broader program.", "SDPP can provide palm-focused inventory fields, condition documentation, monitoring records, priority information, and implementation follow-through that may support an Urban Forest Management Plan or consultant-led program.", '<p class="note">SDPP does not represent this service as preparation of a complete municipal Urban Forest Management Plan, a formal tree-risk assessment, laboratory diagnosis, structural engineering, or municipal-code determination.</p>', "section-tint") +
        section("Municipal context", "Accurate participation wording.", "San Diego Palm Protection submitted mature-palm documentation for consideration during the City of Escondido Urban Forest Management Plan process.", '<p class="note">This statement describes a submission for consideration. It does not state or imply City endorsement, partnership, selection, approval, or adoption.</p>') +
        approved_ufmp_resource()
    },
    "palm-removal-coordination.html": {
        "title": "Palm Decline, Removal & Replacement Coordination | SDPP",
        "description": "Document palm decline, coordinate urgent response and removal, preserve the loss record, and plan appropriate replacement.",
        "eyebrow": "Response pathway", "h1": "Decline, Removal & Replacement Coordination",
        "lede": "When a palm changes quickly or has to come down, I help the owner organize what happened, communicate with the right contractor, and plan what comes next.",
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
        "title": "Palm Field Work & Documentation | San Diego Palm Protection",
        "description": "See SDPP palm field work, broader-area documentation, dated observations, and public Palm Journal records.",
        "eyebrow": "Field work and reporting", "h1": "See what I photograph and what I put in writing.",
        "lede": "These public examples show the kind of palm views I take, how I describe what I saw, and how a field visit becomes a report the owner can use.",
        "image": "evidence.jpg",
        "body": '''<section class="section section-tint sample-assessment" id="mature-palm-documentation-example" aria-labelledby="mature-palm-documentation-heading">
<div class="sample-assessment-grid">
  <div>
    <p class="eyebrow">Broader-area documentation</p>
    <h2 id="mature-palm-documentation-heading">Mature Palm Documentation Example</h2>
    <p class="sample-assessment-lede">See a sanitized example of broader-area palm documentation prepared to support preservation, monitoring, loss records, and urban-forest implementation.</p>
    <p class="note">This limited Old Escondido field sample is not a complete inventory, municipal plan, formal tree-risk assessment, laboratory report, or City-endorsed document.</p>
    <div class="button-row"><a class="button" href="./old-escondido-urban-forest-documentation.pdf" target="_blank" rel="noopener noreferrer">View Civic Documentation Example <span class="sr-only">(PDF, opens in a new tab)</span></a><a class="sample-request-link" href="./urban-forest-palm-documentation.html">Explore urban forest documentation</a></div>
  </div>
  <aside class="sample-document-card" aria-label="Sanitized mature palm documentation example PDF">
    <span class="sample-document-type" aria-hidden="true">PDF</span><h3>Old Escondido mature palm documentation</h3><p>Eight-page public example with a repeatable field structure, monitoring value, decline and loss documentation, and explicit limitations.</p><a href="./urban-forest-palm-documentation.html#old-escondido-documentation-method">Review the documentation pathway</a> · <a href="./old-escondido-urban-forest-documentation.pdf" target="_blank" rel="noopener noreferrer">Open the PDF <span class="sr-only">(opens in a new tab)</span></a>
  </aside>
</div>
</section>''' +
        section("Continue from the field", "Examples, report scope, and privacy in one place.", "The Palm Journal and Documented Loss preserve dated local context. A client report can connect the purpose of the visit, baseline photographs, visible findings, limitations, recommendations, and follow-through without exposing private source records.", '<div class="field-links"><a href="./palm-journal-new.html">Read the Palm Journal</a><a href="./palm-journal/las-palmas-no-reply-then-the-saws.html">View the Las Palmas entry</a><a href="./palm-journal/documented-loss/">Visit Documented Loss</a></div><p class="note">Only separately approved, sanitized material appears publicly. Client identity, address, contact details, private notes, and unapproved photographs remain outside the website.</p><p><a class="button" data-conversion="homeowner-inquiry-initiation" href="./palm-records-monitoring-verification.html#homeowner-inquiry">Request a Palm Assessment</a></p>', "section-tint")
    },
    "palm-stewardship-plans.html": {
        "title": "Palm Tree Treatment & Preventive Protection San Diego | SDPP",
        "description": "Palm tree treatment and preventive protection for mature palms in San Diego and North County, based on an on-site assessment, label requirements, and site conditions.",
        "eyebrow": "Protection and treatment", "h1": "Palm treatment and preventive protection in San Diego.",
        "lede": "I assess the palm and site, explain the protection options, and provide pesticide treatment when it is appropriate for the species, condition, property, and agreed scope.",
        "image": "treatment.jpg",
        "body": section("Protection and treatment", "I start with the palm and the site.", "I review visible conditions, known pest pressure, treatment history, access, and the owner's goals before recommending a plan.", '<p class="note">Protection and treatment services are available when they are appropriate for the palm and property.</p>') +
        section("When protection may be considered", "The recommendation follows the palm and the evidence.", "Mature Canary Island date palms, locally significant palms, known pest pressure, visible change, or a prevention objective may warrant assessment. A symptom or photograph alone does not establish a diagnosis or automatically justify treatment.", cards([
            ("Assessment and observation", "Document visible condition, property context, history, access, and the decision the client needs to make."),
            ("Diagnosis and confirmation", "Separate observed or reported information from suspected causes; recommend laboratory or specialist confirmation when needed."),
            ("Treatment decision", "Use the site history, observed condition, label requirements, and property priorities to decide whether SDPP treatment is appropriate."),
        ]), "section-tint") +
        section("From assessment to follow-up", "Keep the work connected.", "A visible-condition record and treatment history help me choose and track the work.", process([("Assess", "Review the palm, site, history, and visible concern."), ("Plan", "Choose the protection or treatment approach that fits."), ("Treat", "Perform the agreed work when applicable."), ("Monitor", "Add comparable photographs at a useful interval.")])) +
        section("Records and follow-through", "The history remains understandable over time.", "The written record can identify the palm, visible condition, reported or supplied treatment history, limitations, and recommended monitoring or escalation.", '<p><a href="./quarterly-palm-care-san-diego.html">Explore recurring palm stewardship</a> · <a href="./palm-proof-examples.html">View sample work</a> · <a href="./palm-journal/monitoring-mature-cidp-after-palm-weevil-activity.html">See a local monitoring field record</a></p>') +
        section("Clear boundaries", "Educational information without unsupported promises.", "No pesticide treatment guarantees prevention, complete control, recovery, survival, or any other outcome, and a visual visit cannot reveal every hidden condition.", cards([
            ("Current scope", "I provide protection and treatment services when they are appropriate for the palm and site."),
            ("Coordinated work", "SDPP may coordinate pruning, removal, planting, or other contractor work but does not represent that work as directly performed when it falls outside the approved scope."),
            ("Professional referrals", "Formal tree-risk, structural, engineering, laboratory, municipal-code, or other specialist opinions are referred when they exceed the service scope."),
        ]), "section-tint")
    },
    "south-american-palm-weevil-treatment-san-diego.html": {
        "title": "South American Palm Weevil Treatment San Diego | SDPP",
        "description": "South American palm weevil treatment, preventive protection, monitoring, and documentation for Canary Island date palms in San Diego and North County.",
        "eyebrow": "Protection and treatment",
        "h1": "South American Palm Weevil Treatment in San Diego",
        "lede": "I provide South American palm weevil assessment, preventive protection, pesticide treatment, monitoring, and treatment records for Canary Island date palms when the palm and site are suitable.",
        "image": "treatment.jpg",
        "body": section("Documentation before decisions", "A visible-condition record supports better questions.", "The review considers palm species, visible condition, reported history, known pest pressure, access, timing, prior treatment information, and client objectives. Preventive treatment is available when appropriate, but photographs or a single symptom do not establish SAPW or another diagnosis.", cards([
            ("Document", "Establish dated photographs, observations, reported history, and limitations."),
            ("Prepare", "Separate monitoring, confirmation, preventive treatment, and urgent response paths."),
            ("Record", "Document SDPP treatment where applicable, supplied prior history, and the recommended follow-up or monitoring point."),
        ])) +
        section("Protection and treatment", "The palm and site determine the plan.", "I review the palm, its history, current pressure, access, and site conditions before recommending protection or treatment.", '<p><a href="./palm-stewardship-plans.html">Review general palm treatment and preventive protection</a> · <a href="./quarterly-palm-care-san-diego.html">Review recurring palm stewardship</a> · <a href="./sapw.html">Read the South American palm weevil field guide</a></p>', "section-tint")
    },
    "sapw.html": {
        "title": "South American Palm Weevil San Diego: Signs & Prevention",
        "description": "A San Diego guide to South American palm weevil warning signs, affected palms, prevention, treatment timing, local field evidence, and next steps.",
        "eyebrow": "Canary Island date palm risk", "h1": "South American Palm Weevil in San Diego: Signs, Prevention, and Response",
        "lede": "If a mature Canary Island date palm looks different, I will look at the whole palm, photograph the change, and explain whether I would monitor it, seek confirmation, or consider it urgent.",
        "image": "south-american-palm-weevil-cidp-poway.jpg",
        "body": section("What I watch for", "A change in the crown deserves a closer look.", "A drooping or thinning crown, unusual frond behavior, damage, odor, or debris may deserve attention. None of those signs alone proves South American palm weevil.", cards([("Look at the whole palm", "I review the crown, trunk, base, nearby ground, access, and the timeline the owner reports."), ("Photograph the change", "Dated views help show whether the palm is stable or continuing to decline."), ("Choose the response", "I explain whether monitoring, protection, treatment, decline response, or contractor coordination fits what I find.")])) +
        section("Prevention and treatment timing", "Earlier protection preserves more options.", "Canary Island date palms may merit preventive protection before obvious crown collapse, especially where local pressure, palm value, nearby losses, or property responsibility justify an assessment. Treatment timing, product selection, and application must follow the label and site conditions.", '<p><a href="./south-american-palm-weevil-treatment-san-diego.html">See South American palm weevil treatment services</a> · <a href="./palm-journal/when-sapw-became-local.html">Read the local field chronology</a></p>') +
        section("Safety and certainty", "Do not turn a checklist into a diagnosis.", "Hidden decay, structural stability, pest confirmation, and treatment outcome may require different evidence or qualified specialists.", '<p class="note">Keep people away from a visibly unstable or actively failing palm and contact the appropriate emergency or tree-risk professional when life safety may be involved.</p>', "section-tint")
    },
    "old-escondido-palm-preservation.html": {
        "title": "Mature Palm Preservation in Old Escondido | SDPP",
        "description": "John Krause documents and follows mature palms in Old Escondido, where he lives and has dealt with South American palm weevil activity firsthand.",
        "eyebrow": "Based in Old Escondido", "h1": "These palms are part of my neighborhood.",
        "lede": "I live in Old Escondido, photograph its mature palms, and have dealt with South American palm weevil activity on my own property.",
        "image": "beautiful-old_escondido-cidp.jpg",
        "body": section("Why I pay attention", "A mature palm can change faster than people expect.", "I have seen important neighborhood palms decline and disappear. I want owners to have dated photographs before memory becomes the only baseline.", three_pillars()) +
        section("Municipal context", "Accurate participation wording.", "San Diego Palm Protection submitted mature-palm documentation for consideration during the City of Escondido Urban Forest Management Plan process.", '<p class="note">This statement describes a submission for consideration. It does not state or imply City endorsement, partnership, selection, approval, or adoption.</p>', "section-tint")
    },
    "report-a-palm.html": {
        "title": "Report a Palm or Request Review | San Diego Palm Protection",
        "description": "Private palm observation and photo-review inquiry with explicit permissions and no automatic publication.",
        "eyebrow": "Private inquiry", "h1": "Report a Palm or Request Review",
        "lede": "Prepare a private email handoff. Nothing is published automatically, and this page does not upload or store photographs.",
        "image": "evidence1.jpg",
        "body": section("Private handoff", "Prepare the record before opening email.", "The report is not delivered until you send it from your configured email application.", f'''{compact_credentials("BUSINESS_CREDENTIALS_CONTACT")}
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
    "canary-island-date-palm-care-san-diego.html": ("Canary Island Date Palm Care & Treatment in San Diego", "Species pathway", "Canary Island date palm assessment, treatment, recurring care, nutrition and irrigation review, preservation planning, and decline response in San Diego.", "CIDP_big.jpg"),
    "cidp-risk-checklist.html": ("Canary Island Date Palm Risk Checklist", "Educational checklist", "A practical observation checklist to prepare for an assessment without substituting a diagnosis or safety evaluation.", "poway-what-does-sapw-look-like-cidp.jpg"),
    "palm-care-escondido.html": ("Palm Care & Treatment in Escondido", "Local service pathway", "Palm assessment, treatment, recurring care, preservation, and managed-property support from an owner-led specialist based in Old Escondido.", "Old-Escondido_full-CIDP.jpg"),
    "palm-care-poway.html": ("Palm Care & Treatment in Poway", "Local service pathway", "Palm assessment, treatment, recurring care, and preservation planning for residential, estate, and managed properties in Poway.", "Healthy-CIDP-Poway.jpg"),
    "palm-care-rancho-santa-fe.html": ("Palm Care & Treatment in Rancho Santa Fe", "Local service pathway", "Discreet palm assessment, treatment, recurring stewardship, and preservation planning for Rancho Santa Fe estates and managed properties.", "RSF1.jpg"),
    "palm-faq-san-diego.html": ("Palm Care, Treatment & Assessment FAQ", "Education & decision support", "Answers about palm assessments, treatment, monitoring, reporting, managed properties, visible decline, service limits, and next steps in San Diego.", "journal-overview.jpg"),
    "palm-sourcing-installation.html": ("Palm Sourcing, Installation & Replacement Planning", "Response, Removal & Replacement", "Replacement planning connects site constraints, appropriate selection, sourcing questions, installation responsibilities, baseline documentation, and establishment monitoring.", "Bismarck-Specimen-Escondido.jpg"),
    "specimen-palms-cycads.html": ("Specimen Palms & Cycads", "Replacement planning", "Explore significant palm and cycad landscape possibilities with realistic site, sourcing, installation, documentation, and establishment considerations.", "Bismarck.jpg"),
}


def generic_body(name: str) -> str:
    local_openings = {
        "palm-care-escondido.html": (
            "Working from Old Escondido",
            "I know how much mature palms shape this city.",
            "I photograph palms in older neighborhoods, apartment properties, and commercial landscapes where an established crown can be part of the view for decades.",
        ),
        "palm-care-poway.html": (
            "Palm work in Poway",
            "Large properties make comparison especially useful.",
            "Poway has mature statement palms on residential and estate properties where access, distance, and older landscaping can make a dated set of photographs worth keeping.",
        ),
        "palm-care-rancho-santa-fe.html": (
            "Palm work in Rancho Santa Fe",
            "A significant palm deserves an unhurried visit.",
            "On estate properties, I pay attention to the palm's place in the landscape, access around it, earlier care, and the question the owner or manager needs answered.",
        ),
        "canary-island-date-palm-care-san-diego.html": (
            "Canary Island date palms",
            "The crown tells part of the story.",
            "I photograph the whole palm and the crown carefully, because changes near the growing point can matter and older photographs are often the best comparison available.",
        ),
        "cidp-risk-checklist.html": (
            "Before the visit",
            "Write down what changed and when you first noticed it.",
            "Older photographs, dates, recent pruning or treatment history, fallen material, and a description of the change can make an on-site assessment more useful. A checklist is not a diagnosis.",
        ),
        "palm-faq-san-diego.html": (
            "Questions I hear",
            "What can you tell from the ground?",
            "I can describe what I can see, photograph the palm, compare earlier images, and explain what deserves another look. I cannot see hidden decay or certify structural safety from a routine visit.",
        ),
        "palm-sourcing-installation.html": (
            "After a palm is lost",
            "Replacement starts with the site, not the catalog.",
            "Before choosing another palm, I look at space, long-term scale, access, irrigation, installation responsibilities, and how the new palm will be photographed after planting.",
        ),
        "specimen-palms-cycads.html": (
            "Specimen plants",
            "A striking plant still has to fit the property.",
            "Size at maturity, access, sourcing, installation, irrigation, and follow-up all matter. I help organize those questions before a purchase or replacement decision.",
        ),
    }
    eyebrow, heading, intro = local_openings[name]
    return section(eyebrow, heading, intro, three_pillars()) + section("What to expect", "I start with your question and the palm in front of me.", "Tell me what you noticed, what has been done recently, and what you need to decide.", cards([
        ("At the property", "I examine what can be seen safely from the ground and take the photographs the question requires."),
        ("After the visit", "I explain what I observed, what remains uncertain, and what I recommend next."),
        ("If another professional is needed", "I keep the handoff focused on the facts and photographs already gathered."),
    ]), "section-tint")


def write_pages() -> None:
    pages = dict(PAGES)
    for filename, (h1, eyebrow, lede, image) in GENERIC.items():
        pages[filename] = {
            "title": f"{h1} | SDPP",
            "description": lede,
            "eyebrow": eyebrow, "h1": h1, "lede": lede, "image": image,
            "body": generic_body(filename),
        }
    for filename, data in pages.items():
        if filename == "urban-forest-palm-documentation.html":
            schema = {
                "@context": "https://schema.org", "@type": "Article",
                "headline": UFMP_RESOURCE["title"],
                "description": UFMP_RESOURCE["summary"],
                "url": f"{BASE_URL}/urban-forest-palm-documentation.html#old-escondido-documentation-method",
                "image": [
                    f"{BASE_URL}/images/old-escondido-urban-forest-documentation/{item['filename']}"
                    for item in UFMP_RESOURCE["media"]
                ],
                "author": {"@type": "Organization", "name": "San Diego Palm Protection", "url": BASE_URL},
                "about": UFMP_RESOURCE["metadata"]["about"],
                "isPartOf": {"@type": "WebPage", "url": f"{BASE_URL}/urban-forest-palm-documentation.html"},
            }
        else:
            schema = {
                "@context": "https://schema.org", "@type": "Service",
                "provider": {
                    "@type": "LocalBusiness",
                    "name": "San Diego Palm Protection",
                    "url": BASE_URL,
                    "telephone": "+1-262-492-3135",
                    "email": "sandiegopalmprotection@gmail.com",
                    "areaServed": ["San Diego County", "North County San Diego"],
                },
                "name": data["h1"], "serviceType": data["h1"],
                "areaServed": ["San Diego County", "North County San Diego"],
                "description": data["description"],
            }
        if filename == "about.html":
            schema = {
                "@context": "https://schema.org",
                "@type": "Person",
                "name": "John Krause",
                "jobTitle": "Owner",
                "worksFor": {
                    "@type": "Organization",
                    "name": "San Diego Palm Protection",
                    "url": BASE_URL,
                },
                "url": f"{BASE_URL}/about.html",
            }
        (ROOT / filename).write_text(page(filename=filename, extra_schema=schema, publish_extra_schema=filename == "about.html", **data), encoding="utf-8")
    (ROOT / "site-config" / "core_routes.json").write_text(json.dumps(sorted(pages), indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(pages)} canonical core pages.")


if __name__ == "__main__":
    write_pages()
