from __future__ import annotations

from html import escape
from pathlib import Path
import json

from site_components import ROOT, BASE_URL, page, three_pillars, credentials, INQUIRY

UFMP_RESOURCE = json.loads((ROOT / "site-config" / "ufmp_resource.json").read_text(encoding="utf-8"))


def section(eyebrow: str, heading: str, intro: str, content: str, classes: str = "") -> str:
    return f'<section class="section {classes}"><div class="section-intro"><p class="eyebrow">{escape(eyebrow)}</p><h2>{escape(heading)}</h2><p>{escape(intro)}</p></div>{content}</section>'


def cards(items: list[tuple[str, str]], cls: str = "service-grid") -> str:
    count_class = f" {cls}--{len(items)}" if cls == "service-grid" else ""
    return f'<div class="{cls}{count_class}">' + "".join(f'<article class="service-card"><h3>{escape(h)}</h3><p>{escape(p)}</p></article>' for h, p in items) + "</div>"


def process(items: list[tuple[str, str]]) -> str:
    return '<div class="process">' + "".join(f'<div><h3>{escape(h)}</h3><p>{escape(p)}</p></div>' for h, p in items) + "</div>"


def inquiry_paths() -> str:
    explanation = escape(INQUIRY["public_explanation"])
    return f'''<div class="inquiry-paths">
<article class="inquiry-panel" id="homeowner-inquiry">
  <p class="eyebrow">For homeowners</p><h3>Request a Palm Assessment</h3>
  <p>Use this path for a residential assessment, condition baseline, recurring monitoring, sourcing, or decline-response question.</p>
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
</article>
<article class="inquiry-panel" id="organization-inquiry">
  <p class="eyebrow">For commercial and managed properties</p><h3>Request a Property Walkthrough</h3>
  <p>Use this path for an HOA, apartment community, senior-living community, hotel, club, school, church, campus, commercial property, institution, or public palm portfolio.</p>
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
</article>
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
    <a href="./palm-proof-examples.html#sample-assessment">Sanitized sample assessment</a>
  </div>
</section>'''


PAGES: dict[str, dict] = {
    "index.html": {
        "title": "Mature Palm Protection in North County San Diego | SDPP",
        "description": "Commercial palm care and managed-property palm protection, assessments, recurring treatment, monitoring, and documentation in San Diego.",
        "eyebrow": "Palm assessment and documentation · Old Escondido",
        "h1": "Protect Your Mature Palms in North County San Diego",
        "lede": "Specialized palm protection for estates, multifamily communities, senior-living campuses, hospitality properties, HOAs, commercial grounds, and homeowners with valuable mature palms.",
        "image": "background.jpg",
        "body": section("Commercial & managed properties", "Build one clear operating record for the property.", "I inventory, photograph, monitor, and treat mature palms across managed properties. Each palm can receive a stable ID, visible-condition baseline, treatment history, and defined next action.", '<div class="button-row"><a class="button" data-conversion="organization-inquiry-initiation" href="./palm-records-monitoring-verification.html#organization-inquiry">Request a Property Walkthrough</a><a class="button button-secondary" href="./managed-property-palm-services.html">View Commercial &amp; Managed Services</a></div>', "section-tint") +
        section("How I help", "Assessment, protection, and follow-through.", "The work can begin with one palm or a full portfolio and continue through preventive treatment, recurring monitoring, written reporting, decline response, and replacement planning.", three_pillars()) +
        section("Who I work with", "Palm protection for valuable properties.", "The work is shaped by the palms, the property, and the decisions that need to be made.", '<div class="audience-grid audience-grid--2"><article class="audience-card"><h3>Commercial &amp; Managed Properties</h3><p>Recurring palm protection, documentation, planning, and coordination for properties with multiple or high-value palms.</p><a data-conversion="organization-inquiry-initiation" href="./palm-records-monitoring-verification.html#organization-inquiry">Discuss a multi-palm property</a></article><article class="audience-card"><h3>Residential &amp; Estate Properties</h3><p>Owner-performed assessment, treatment, and recurring care for homeowners and estate owners protecting important mature palms.</p><a data-conversion="homeowner-inquiry-initiation" href="./palm-records-monitoring-verification.html#homeowner-inquiry">Tell me about your palm</a></article></div>') +
        section("Local and direct", "You work with me from the first call.", "The owner handles the property visit, photographs, written findings, and follow-up questions.", '<div class="field-split"><div><h3>No sales-to-field handoff</h3><p>The person you speak with is the person who looks at your palms. That matters when small details and property history need to carry through to the report.</p><p><a class="button" href="./about.html">About John and SDPP</a></p></div><img src="./beautiful-old_escondido-cidp.jpg" alt="Mature Canary Island date palm in Old Escondido" loading="lazy"></div>') +
        section("Canary Island date palms", "I take South American palm weevil seriously.", "I have dealt with South American palm weevil activity on my own Old Escondido property. That firsthand experience is one reason I pay close attention to crown change and to photographs that show when a change began.", '<div class="field-split field-split--reverse"><img src="./south-american-palm-weevil-cidp-poway.jpg" alt="Canary Island date palm observed in North County San Diego" loading="lazy"><div><h3>Do not wait for a guess to become an emergency</h3><p>A photograph cannot diagnose a pest, but it can show whether the crown is changing and help me assess the next step.</p><p><a href="./sapw.html">Learn what I watch for</a> · <a href="./palm-stewardship-plans.html">Read about protection planning</a></p></div></div>', "section-tint") +
        section("What you receive", "Photographs you can use later.", "I photograph the entire palm, its crown, trunk, base, and any concern I can safely see. Those images give us something real to compare during a future visit.", process([
            ("At the property", "I look at the palm, access, recent history, and the reason you called."),
            ("In the report", "I organize the photographs and explain what I observed, what remains uncertain, and what deserves attention."),
            ("After the visit", "You can use the report to monitor the palm or speak with a contractor or another qualified professional."),
        ]) + '<p class="section-proof-link"><a data-conversion="residential-sample-pdf-view" href="./san-diego-palm-protection-sample-assessment.pdf" target="_blank" rel="noopener noreferrer">View a sanitized sample palm assessment <span class="sr-only">(PDF, opens in a new tab)</span></a></p>') +
        section("Scope and pricing", "I price the visit after I understand the job.", "Palm count, access, travel, urgency, and the report you need all affect the price.", '<p class="note">I will confirm the work and price with you before the visit.</p>') +
        section("Commercial proof", "See the kind of palm-level record a property manager can use.", "The sanitized Old Escondido example shows how multiple palms, dated photographs, visible observations, priorities, and limits can be organized without exposing private client information.", '<p><a class="button" href="./old-escondido-mature-palm-documentation-example.pdf" target="_blank" rel="noopener noreferrer">View the representative palm documentation example <span class="sr-only">(PDF, opens in a new tab)</span></a> <a href="./palm-proof-examples.html">See more Field Work</a></p>', "section-tint") +
        section("Field work", "See the kind of work I publish.", "The Field Work page and Palm Journal show local palms, dated observations, and sample reporting without exposing private client information.", '<div class="field-links"><a href="./palm-records-monitoring-verification.html">View services</a><a href="./palm-proof-examples.html">View Field Work</a><a href="./palm-journal-new.html">Read the Palm Journal</a><a href="./palm-journal/documented-loss/">Visit Documented Loss</a></div>'),
    },
    "about.html": {
        "title": "About San Diego Palm Protection | Owner-Led Palm Services",
        "description": "Meet John Krause, the Old Escondido owner who personally visits, photographs, and reports on mature palms for San Diego Palm Protection.",
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
<div class="about-john-copy">
  <p>I started SDPP after confronting South American palm weevil activity and palm loss on my own Old Escondido property. That experience made the threat very real to me&mdash;and made me look more closely at how many mature palms across our neighborhoods could be lost without earlier attention.</p>
  <p>I have my B.S. from the University of Minnesota in environmental science and am also a Navy veteran. That background shapes how I approach this work: observe carefully, document what is happening, communicate clearly, and take responsibility for the work performed.</p>
  <p>Today, I provide owner-led palm assessments, monitoring, protection, and treatment services throughout San Diego County. I built SDPP to give palm owners a knowledgeable local point of contact&mdash;someone who will personally look at the tree, explain what is visible, maintain useful records, and help determine a responsible next step.</p>
</div>
</div>''') +
        section("Work directly with the owner", "I stay with the work.", "I answer the inquiry, visit the property, photograph the palms, write the findings, and discuss the next step with you.", '<div class="field-split"><div><h3>Why that matters</h3><p>I do not have to translate another person&#x27;s field notes or guess what happened during the visit. I was there.</p></div><img src="./journal-monitoring.jpg" alt="Palm condition documentation during an SDPP field visit" loading="lazy"></div>', "section-tint") +
        section("Qualification and scope", "Qualified, insured, and operating within a defined service boundary.", "I hold California Qualified Applicator License No. 175295, Category B — Landscape Maintenance. SDPP is insured and provides assessment, monitoring, documentation, protection and pesticide treatment services as applicable.", '<p class="note">Treatment follows the pesticide label, applicable law, site conditions, and agreed scope. I do not promise diagnosis from photographs, treatment efficacy, palm recovery, or guaranteed outcomes.</p>') +
        section("Local focus", "Old Escondido is home.", "I am based in Old Escondido and focus on mature palms, especially Canary Island date palms, across North County and selected nearby San Diego communities.", '<p><a href="./old-escondido-palm-preservation.html">See my Old Escondido work</a></p>', "section-tint") +
        section("Firsthand experience", "South American palm weevil reached my own property.", "I have personally dealt with SAPW activity on my Canary Island date palms in Old Escondido. I do not turn every symptom into a diagnosis, but I do believe owners should photograph changes early and take them seriously.", cards([
            ("Observation is not diagnosis", "I report what I can see and keep suspected causes separate from confirmed facts."),
            ("The photographs belong in the service", "They are the baseline for a later comparison, not decoration."),
            ("A return visit answers a different question", "Sometimes the most useful finding is whether the palm looks stable or has continued to change."),
        ])) +
        section("Start a conversation", "Choose the inquiry path that fits.", "Homeowners can request an assessment. Managers, HOAs, institutions, and other property stakeholders can discuss a palm portfolio.", '<div class="button-row"><a class="button" data-conversion="homeowner-inquiry-initiation" href="./palm-records-monitoring-verification.html#homeowner-inquiry">Request a Palm Assessment</a><a class="button" data-conversion="organization-inquiry-initiation" href="./palm-records-monitoring-verification.html#organization-inquiry">Discuss a Property or Palm Portfolio</a></div>', "section-tint"),
    },
    "residential-palm-assessment.html": {
        "title": "Residential Mature Palm Assessment | San Diego Palm Protection",
        "description": "John Krause visits your property, examines the palm from the ground, takes dated photographs, and gives you a written assessment.",
        "eyebrow": "On-site residential service", "h1": "Residential Mature Palm Assessment",
        "lede": "I come to the property, look at the whole palm from the ground, photograph what concerns you, and give you a written account of what I found.",
        "image": "mature_healthy_cidp_poway_mansion.jpg",
        "body": section("What I deliver", "A dated starting point for your palm.", "I photograph the entire palm, its crown, trunk, base, and any concern I can safely see. Those photographs give us something real to compare later.", cards([
            ("The palm and its setting", "I note where it stands, what can be accessed safely, and what prompted the visit."),
            ("Dated photographs", "I take whole-palm and detail views that can be repeated during a future visit."),
            ("What I observed", "I separate what I saw from what you reported, what I suspect, and what would need confirmation."),
            ("Your written report", "You receive the photographs, findings, limits of the visit, and the next steps I recommend."),
        ]) + '<p class="section-proof-link"><a href="./palm-proof-examples.html#sample-assessment">See a sanitized sample report</a></p>') + section("What it is not", "Useful because its limits are explicit.", "A visual assessment cannot promise tree safety, uncover hidden conditions, replace laboratory confirmation, or guarantee an outcome.", '<p class="note">Urgent structural or life-safety concerns may require an emergency contractor or other specialist.</p>', "section-tint") +
        section("If the palm needs watching", "The first visit becomes the comparison point.", "When I return, I try to repeat the same views. That makes it easier to see whether the crown, trunk, or surrounding conditions have changed.", process([("Before the visit", "Tell me what changed and send any older photographs you have."), ("At the property", "I observe and photograph the areas I can access safely."), ("Afterward", "You receive the dated report and a recommended time for another look, if one is useful.")]) + '<p class="section-proof-link"><a href="./about.html">Learn more about John Krause</a></p>')
    },
    "palm-records-monitoring-verification.html": {
        "title": "Palm Assessment, Monitoring & Documentation Services | SDPP",
        "description": "Palm condition baselines, written reporting, recurring monitoring, managed-property inventories, contractor-work verification, protection, and decline response.",
        "eyebrow": "Palm assessment and ongoing care", "h1": "Start with a careful look at the palm.",
        "lede": "I can assess one palm, return to compare it over time, organize a larger property, or help when a palm begins to fail.",
        "image": "journal-monitoring.jpg",
        "body": section("Services", "Three ways I can help.", "The work begins with what you need to know now. It can end with one report or continue through return visits, contractor work, decline, and replacement.", three_pillars()) +
        section("Assessment, Monitoring & Documentation", "You receive work you can actually use.", "The photographs and report are part of the service.", cards([
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
        section("Commercial & managed pathway", "Start with a property walkthrough.", "For an HOA, apartment community, senior-living property, hotel, club, school, church, campus, commercial site, historic property, or large estate, I can scope a paid palm inventory, preventive treatment, recurring monitoring, reporting, and stewardship plan.", '<p><a class="button" data-conversion="organization-inquiry-initiation" href="#organization-inquiry">Request a Property Walkthrough</a> <a href="./managed-property-palm-services.html">View commercial and managed services</a></p>', "section-tint") +
        section("Request", "Tell me about the palm or property.", "Use the homeowner form for one palm or a small group. Use the organization form for an HOA, apartment property, institution, or commercial site.", f'{credentials("BUSINESS_CREDENTIALS_CONTACT")}{inquiry_paths()}') +
        section("Related decisions", "When the question changes.", "These pages cover decline, contractor coordination, sourcing, and confirmed loss.", '<p><a href="./palm-removal-coordination.html">Decline, removal, and replacement</a> · <a href="./palm-sourcing-installation.html">Sourcing and installation</a> · <a href="./specimen-palms-cycads.html">Specimen palms and cycads</a> · <a href="./palm-journal/documented-loss/">Documented Loss</a></p>')
    },
    "quarterly-palm-care-san-diego.html": {
        "title": "Recurring Palm Monitoring | San Diego Palm Protection",
        "description": "John Krause returns to photograph the same palm views, compare changes, and update the written findings.",
        "eyebrow": "Monitoring pathway", "h1": "Recurring Palm Monitoring",
        "lede": "A return visit is useful when we can compare the same palm from the same views. The interval depends on the concern, the season, and what the owner needs to decide.",
        "image": "journal-seasonal.jpg",
        "body": section("What I compare", "I go back to the earlier photographs.", "I try to repeat the whole-palm, crown, trunk, and base views so changes are easier to see.", process([
            ("First visit", "Create the dated photographs and written starting point."),
            ("Return visit", "Repeat the useful views and note anything new."),
            ("Comparison", "Show what looks stable, what has changed, and what the photographs cannot answer."),
            ("Update", "Revise the priorities and recommend whether another visit or referral makes sense."),
        ])) + section("Choosing the interval", "The timing follows the question.", "A three-month schedule can be useful, but it is not automatically right for every palm. I explain when I would look again and why.", cards([
            ("Residential monitoring", "Follow a significant palm after a baseline, contractor work, storm exposure, or a new concern."),
            ("Managed-property monitoring", "Maintain an auditable multi-palm timeline with priority changes and work-status notes."),
            ("Escalation", "Recommend closer review, specialist referral, treatment consideration, or response when documented change supports it."),
        ]), "section-tint")
    },
    "managed-property-palm-services.html": {
        "title": "Commercial & Managed-Property Palm Care San Diego | SDPP",
        "description": "Commercial palm care, HOA palm care, multi-palm assessments, recurring palm treatment, monitoring, and documentation for managed properties in San Diego.",
        "eyebrow": "Commercial & managed-property palm stewardship", "h1": "Know every palm. Track every decision.",
        "lede": "Specialized palm protection for HOAs, multifamily and senior-living communities, hospitality properties, clubs, campuses, commercial grounds, historic properties, and large estates.",
        "image": "Las Palmas_Appartments_Healthy-CIDP.jpg",
        "body": section("Start with the property", "A practical path from walkthrough to annual planning.", "The first conversation is usually 15–20 minutes. A complete inventory or report is paid work, scoped after I understand the property.", process([
            ("1. Property walkthrough", "Confirm palm count, species, access, known concerns, landscape responsibilities, and management objectives."),
            ("2. Paid palm portfolio baseline", "Assign IDs, establish locations, create repeatable photographs, document visible condition, and identify priorities."),
            ("3. Protection and treatment plan", "Identify palms for monitoring, preventive treatment, or escalation based on actual conditions and lawful label-compliant scope."),
            ("4. Recurring stewardship", "Schedule monitoring, appropriate treatment, comparable photographs, treatment history, and management reporting."),
            ("5. Response coordination", "Organize contractor questions, removal documentation, access, loss records, sourcing, and replacement planning when required."),
            ("6. Annual planning", "Prepare a concise portfolio summary for operational priorities and budgeting."),
        ]) + '<p><a class="button" data-conversion="organization-inquiry-initiation" href="./palm-records-monitoring-verification.html#organization-inquiry">Request a Property Walkthrough</a></p>') +
        section("Properties served", "Built for valuable palms in shared and substantial landscapes.", "A property does not need hundreds of palms to benefit. The common thread is responsibility for multiple palms, high-value specimens, or a landscape where continuity and records matter.", cards([
            ("Communities and campuses", "HOAs, multifamily communities, senior-living properties, churches, schools, nonprofit campuses, and historic properties."),
            ("Hospitality and clubs", "Hotels, hospitality grounds, country clubs, private clubs, and properties where mature palms shape the arrival experience."),
            ("Commercial properties and estates", "Commercial grounds, large estates, and properties with multiple Canary Island date palms or other valuable mature palms."),
        ])) +
        section("Commercial service levels", "Choose the depth the property actually needs.", "These are flexible service levels, not rigid packages. Scope follows palm count, species, condition, access, treatment requirements, and property priorities.", cards([
            ("Palm Portfolio Baseline", "Numbered inventory, species and location where supportable, dated photographs, visible-condition observations, priority classification, and recommended next actions."),
            ("Protection and Monitoring", "Baseline maintenance, recurring observations, preventive treatment when appropriate, treatment and work history, change-over-time documentation, and escalation triggers."),
            ("Palm Stewardship", "Protection and monitoring, management reporting, contractor interface, decline-response coordination, removal and replacement records, and annual planning."),
        ]), "section-tint") +
        section("What the client receives", "Palm-by-palm detail and a property summary.", "Multi-palm properties receive a customized proposal after the property discussion or walkthrough. The exact deliverables are agreed before work begins.", cards([
            ("Palm register", "Stable IDs, locations, species where supportable, baseline photographs, visible observations, and current status."),
            ("Priority summary", "What needs attention now, what can wait, and who owns the next step."),
            ("Written reporting", "Observed conditions, reported history, uncertainties, recommendations, and scheduled review points."),
            ("Treatment and work history", "Label-compliant SDPP treatment records where applicable, supplied contractor records, removals, losses, and replacements."),
        ])) +
        section("Owner-level accountability", "One point of contact from walkthrough through follow-up.", "John handles the field review, documentation, proposal, and client communication. A certificate of insurance and W-9 are available for vendor setup.", '<p class="note">SDPP remains a specialized palm company, not a general tree-service or full-service landscape contractor.</p>', "section-tint") +
        section("Representative proof", "See the kind of palm-level record a property manager can use.", "This sanitized Old Escondido example demonstrates a repeatable multi-palm record. It is representative documentation, not a claim of commercial client work or a complete municipal inventory.", '<p><a class="button" href="./old-escondido-mature-palm-documentation-example.pdf" target="_blank" rel="noopener noreferrer">View the representative documentation example <span class="sr-only">(PDF, opens in a new tab)</span></a> <a href="./palm-proof-examples.html">View Field Work</a></p>', "section-tint") +
        section("Observation and response", "Visible conditions guide the next step.", "I separate what I observe from reported history and suspected causes, then explain the response that fits the palm and property.", '<p class="note">I provide protection and treatment services and coordinate removal or contractor work as applicable.</p>') +
        section("Contractor work", "I can photograph what was completed and organize the paperwork.", "I can compare before-and-after views, note dates, and keep the records a contractor provides.", '<p class="note">I cannot verify work hidden from view or certify workmanship, structural safety, code compliance, pesticide efficacy, contractor licensing, or outcomes.</p>', "section-tint") +
        section("Municipal and urban-forest support", "Palm-focused field records for broader programs.", "Specialized palm documentation can support portfolio management and urban-forest implementation without claiming to prepare a complete municipal plan.", '<p><a href="./urban-forest-palm-documentation.html#old-escondido-documentation-method">Review the approved Old Escondido civic documentation resource</a> · <a href="./palm-proof-examples.html">View sample work</a> · <a href="./old-escondido-urban-forest-documentation.pdf" target="_blank" rel="noopener noreferrer">Download the civic documentation packet <span class="sr-only">(PDF, opens in a new tab)</span></a></p>') +
        section("Municipal context", "Accurate participation wording.", "San Diego Palm Protection submitted mature-palm documentation for consideration during the City of Escondido Urban Forest Management Plan process.", '<p class="note">This statement describes a submission for consideration. It does not state or imply City endorsement, partnership, selection, approval, or adoption.</p><p><a class="button" data-conversion="organization-inquiry-initiation" href="./palm-records-monitoring-verification.html#organization-inquiry">Request a Property Walkthrough</a></p>')
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
        "title": "Sample Palm Assessment Report | San Diego Palm Protection",
        "description": "See a sanitized SDPP field assessment with dated palm photographs, written observations, limitations, and follow-up recommendations.",
        "eyebrow": "Field work and reporting", "h1": "See what I photograph and what I put in writing.",
        "lede": "These public examples show the kind of palm views I take, how I describe what I saw, and how a field visit becomes a report the owner can use.",
        "image": "evidence.jpg",
        "body": '''<section class="section sample-assessment" id="sample-assessment" aria-labelledby="sample-assessment-heading">
<div class="sample-assessment-grid">
  <div>
    <p class="eyebrow">Sample assessment</p>
    <h2 id="sample-assessment-heading">See what a documented palm assessment looks like.</h2>
     <p class="sample-assessment-lede">This sanitized report shows an actual SDPP field assessment. It includes the reason for the visit, dated photographs, what I observed, what I could not confirm, and what I recommended next.</p>
    <p class="note">Client-identifying information has been removed. Every assessment is property-specific, and findings are limited by access, visible evidence, site conditions, and the documented scope.</p>
    <div class="button-row">
      <a class="button" href="./san-diego-palm-protection-sample-assessment.pdf" target="_blank" rel="noopener noreferrer">View sample assessment <span class="sr-only">(PDF, opens in a new tab)</span></a>
      <a class="sample-request-link" href="./residential-palm-assessment.html#request">Request an assessment</a>
    </div>
  </div>
  <aside class="sample-document-card" aria-label="Sanitized sample palm assessment PDF">
    <span class="sample-document-type" aria-hidden="true">PDF</span>
    <h3>Sanitized sample palm assessment</h3>
    <p>Five-page field report with photographs, observations, limitations, recommendations, and follow-up guidance.</p>
    <a href="./san-diego-palm-protection-sample-assessment.pdf" target="_blank" rel="noopener noreferrer">Open the sample PDF <span class="sr-only">(opens in a new tab)</span></a>
  </aside>
</div>
<div class="sample-includes">
  <h3>What the report includes</h3>
  <ul>
    <li>Dated site and palm baseline</li>
    <li>Visible-condition observations</li>
    <li>Photo record and captions</li>
    <li>Known, unknown, and follow-up items</li>
    <li>Practical recommendations</li>
    <li>Monitoring or response interval</li>
  </ul>
</div>
</section>''' +
        '''<section class="section section-tint sample-assessment" id="mature-palm-documentation-example" aria-labelledby="mature-palm-documentation-heading">
<div class="sample-assessment-grid">
  <div>
    <p class="eyebrow">Broader-area documentation</p>
    <h2 id="mature-palm-documentation-heading">Mature Palm Documentation Example</h2>
    <p class="sample-assessment-lede">See a sanitized example of broader-area palm documentation prepared to support preservation, monitoring, loss records, and urban-forest implementation.</p>
    <p class="note">This example uses a limited Old Escondido field sample. It is not a complete inventory, municipal plan, formal tree-risk assessment, laboratory report, or City-endorsed document.</p>
    <div class="button-row">
      <a class="button" href="./old-escondido-urban-forest-documentation.pdf" target="_blank" rel="noopener noreferrer">View Civic Documentation Example <span class="sr-only">(PDF, opens in a new tab)</span></a>
      <a class="sample-request-link" href="./urban-forest-palm-documentation.html">Explore urban forest documentation</a>
    </div>
  </div>
  <aside class="sample-document-card" aria-label="Sanitized mature palm documentation example PDF">
    <span class="sample-document-type" aria-hidden="true">PDF</span>
    <h3>Old Escondido mature palm documentation</h3>
    <p>Eight-page public example with a repeatable field structure, representative records, monitoring value, decline and loss documentation, implementation uses, and explicit limitations.</p>
    <a href="./urban-forest-palm-documentation.html#old-escondido-documentation-method">Review the Urban Forest Documentation pathway</a> · <a href="./old-escondido-urban-forest-documentation.pdf" target="_blank" rel="noopener noreferrer">Open the documentation PDF <span class="sr-only">(opens in a new tab)</span></a>
  </aside>
</div>
</section>''' +
        section("From the field", "Local observations, presented with their limits.", "The Palm Journal preserves dated local context and distinguishes what was observed from what was reported or inferred.", '<div class="field-work-grid"><article><img src="./journal-monitoring.jpg" alt="Palm monitoring field photograph" loading="lazy"><h3>Palm Journal</h3><p>Field notes and educational entries connect local palm conditions with practical observation.</p><a href="./palm-journal-new.html">Read the Palm Journal</a></article><article><img src="./images/las-palmas/01-property-context-laspalmas-escondido-cidp.jpg" alt="Canary Island date palms at Las Palmas in Escondido" loading="lazy"><h3>Las Palmas documented observations</h3><p>A public chronology shows how property context, visible change, communication, and outcome can be documented without overstating cause.</p><a href="./palm-journal/las-palmas-no-reply-then-the-saws.html">View the Las Palmas entry</a></article><article><img src="./evidence.jpg" alt="Palm condition documentation example" loading="lazy"><h3>Documented Loss</h3><p>A respectful public record of significant palms that have been confirmed lost.</p><a href="./palm-journal/documented-loss/">Visit Documented Loss</a></article></div><p class="section-proof-link"><a href="./managed-property-palm-services.html">Managed-property inventory and reporting</a> · <a href="./urban-forest-palm-documentation.html">Urban forest palm documentation</a></p>') +
        section("Example deliverable", "What a written palm condition report can contain.", "The exact scope follows the property and question, but a useful report makes the visit understandable after the specialist leaves.", cards([
            ("Assessment purpose", "The palm, property context, concern, available access, and decision prompting the visit."),
            ("Photographic baseline", "Dated overview and detail views that can support later comparison."),
            ("Visible findings", "Observed conditions separated from reported history, interpretation, and unknowns."),
            ("Recommended next steps", "Practical priorities, monitoring intervals, treatment considerations, response, or referral."),
            ("Limitations", "What could not be seen, tested, verified, or concluded within the agreed visit."),
            ("Follow-through", "A structure for monitoring, contractor communication, or a later outcome record."),
        ], "proof-grid"), "section-tint") +
        section("Privacy boundary", "Only approved public material belongs here.", "The examples above are separately approved sanitized public artifacts. Private client reports and source records are not copied into website source, and any future examples must pass the same public-use and privacy checks.", '<p class="note">No unapproved proof bundle can render publicly. The website accepts only an allowlisted, versioned public derivative; private identity, address, contact, access details, and unapproved photographs remain outside this repository.</p>')
    },
    "palm-stewardship-plans.html": {
        "title": "Palm Protection & Treatment | San Diego Palm Protection",
        "description": "Palm assessment, protection, preventive treatment when appropriate, and recurring monitoring for mature palms in North County San Diego.",
        "eyebrow": "Protection and treatment", "h1": "Protect a Mature Palm Before the Decision Becomes Urgent",
        "lede": "I assess visible palm and site conditions, explain protection options, and provide treatment services when they fit the palm and property.",
        "image": "treatment.jpg",
        "body": section("Protection and treatment", "I start with the palm and the site.", "I review visible conditions, known pest pressure, treatment history, access, and the owner's goals before recommending a plan.", '<p class="note">Protection and treatment services are available when they are appropriate for the palm and property.</p>') +
        section("When protection may be considered", "The recommendation follows the palm and the evidence.", "Mature Canary Island date palms, locally significant palms, known pest pressure, visible change, or a prevention objective may warrant assessment. A symptom or photograph alone does not establish a diagnosis or automatically justify treatment.", cards([
            ("Assessment and observation", "Document visible condition, property context, history, access, and the decision the client needs to make."),
            ("Diagnosis and confirmation", "Separate observed or reported information from suspected causes; recommend laboratory or specialist confirmation when needed."),
            ("Treatment decision", "Use the site history, observed condition, label requirements, and property priorities to decide whether SDPP treatment is appropriate."),
        ]), "section-tint") +
        section("From assessment to follow-up", "Keep the work connected.", "A visible-condition record and treatment history help me choose and track the work.", process([("Assess", "Review the palm, site, history, and visible concern."), ("Plan", "Choose the protection or treatment approach that fits."), ("Treat", "Perform the agreed work when applicable."), ("Monitor", "Add comparable photographs at a useful interval.")])) +
        section("Records and follow-through", "The history remains understandable over time.", "The written record can identify the palm, visible condition, reported or supplied treatment history, limitations, and recommended monitoring or escalation.", '<p><a href="./quarterly-palm-care-san-diego.html">Explore recurring monitoring</a> · <a href="./palm-proof-examples.html">View sample work</a></p>') +
        section("Clear boundaries", "Educational information without unsupported promises.", "No pesticide treatment guarantees prevention, control, recovery, survival, eradication, or any other outcome, and a visual visit cannot reveal every hidden condition.", cards([
            ("Current scope", "I provide protection and treatment services when they are appropriate for the palm and site."),
            ("Coordinated work", "SDPP may coordinate pruning, removal, planting, or other contractor work but does not represent that work as directly performed when it falls outside the approved scope."),
            ("Professional referrals", "Formal tree-risk, structural, engineering, laboratory, municipal-code, or other specialist opinions are referred when they exceed the service scope."),
        ]), "section-tint")
    },
    "south-american-palm-weevil-treatment-san-diego.html": {
        "title": "South American Palm Weevil Protection & Treatment | SDPP",
        "description": "SAPW-aware assessment, visible-condition documentation, preventive treatment when appropriate, and monitoring for Canary Island date palms in North County San Diego.",
        "eyebrow": "Protection and treatment",
        "h1": "South American Palm Weevil Protection & Treatment",
        "lede": "I assess visible palm and property conditions, compare what is changing, and provide protection and treatment services for South American palm weevil concerns when applicable.",
        "image": "treatment.jpg",
        "body": section("Documentation before decisions", "A visible-condition record supports better questions.", "The review considers palm species, visible condition, reported history, known pest pressure, access, timing, prior treatment information, and client objectives. Photographs or a single symptom do not establish SAPW or another diagnosis.", cards([
            ("Document", "Establish dated photographs, observations, reported history, and limitations."),
            ("Prepare", "Separate monitoring, confirmation, preventive treatment, and urgent response paths."),
            ("Record", "Document SDPP treatment where applicable, supplied prior history, and the recommended follow-up or monitoring point."),
        ])) +
        section("Protection and treatment", "The palm and site determine the plan.", "I review the palm, its history, current pressure, access, and site conditions before recommending protection or treatment.", '<p><a href="./palm-stewardship-plans.html">Review Protection & Treatment</a> · <a href="./quarterly-palm-care-san-diego.html">Review recurring monitoring</a></p>', "section-tint")
    },
    "sapw.html": {
        "title": "South American Palm Weevil Assessment in San Diego | SDPP",
        "description": "Local SAPW-aware assessment, Canary Island date palm protection, monitoring, and response in North County San Diego.",
        "eyebrow": "Canary Island date palm risk", "h1": "South American Palm Weevil: Warning Signs and Next Steps",
        "lede": "If a mature Canary Island date palm looks different, I will look at the whole palm, photograph the change, and explain whether I would monitor it, seek confirmation, or consider it urgent.",
        "image": "south-american-palm-weevil-cidp-poway.jpg",
        "body": section("What I watch for", "A change in the crown deserves a closer look.", "A drooping or thinning crown, unusual frond behavior, damage, odor, or debris may deserve attention. None of those signs alone proves South American palm weevil.", cards([("Look at the whole palm", "I review the crown, trunk, base, nearby ground, access, and the timeline the owner reports."), ("Photograph the change", "Dated views help show whether the palm is stable or continuing to decline."), ("Choose the response", "I explain whether monitoring, protection, treatment, decline response, or contractor coordination fits what I find.")])) +
        section("Safety and certainty", "Do not turn a checklist into a diagnosis.", "Hidden decay, structural stability, pest confirmation, and treatment outcome may require different evidence or qualified specialists.", '<p class="note">Keep people away from a visibly unstable or actively failing palm and contact the appropriate emergency or tree-risk professional when life safety may be involved.</p>', "section-tint")
    },
    "old-escondido-palm-preservation.html": {
        "title": "Old Escondido Mature Palm Protection | SDPP",
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
    "canary-island-date-palm-care-san-diego.html": ("Canary Island Date Palm Assessment & Care", "Species pathway", "Assessment, baseline documentation, monitoring, protection planning, and response for significant Canary Island date palms.", "CIDP_big.jpg"),
    "cidp-risk-checklist.html": ("Canary Island Date Palm Risk Checklist", "Educational checklist", "A practical observation checklist to prepare for an assessment without substituting a diagnosis or safety evaluation.", "poway-what-does-sapw-look-like-cidp.jpg"),
    "palm-care-escondido.html": ("Palm Assessment & Monitoring in Escondido", "Local service pathway", "Residential and managed-property palm assessment, baselines, monitoring, protection planning, and decline response in Escondido.", "Old-Escondido_full-CIDP.jpg"),
    "palm-care-poway.html": ("Palm Assessment & Monitoring in Poway", "Local service pathway", "Residential and managed-property palm assessment, baselines, monitoring, protection planning, and decline response in Poway.", "Healthy-CIDP-Poway.jpg"),
    "palm-care-rancho-santa-fe.html": ("Palm Assessment & Monitoring in Rancho Santa Fe", "Local service pathway", "Discreet residential and estate palm assessment, condition baselines, monitoring, protection planning, and decline response.", "RSF1.jpg"),
    "palm-faq-san-diego.html": ("Palm Assessment & Monitoring FAQ", "Education & decision support", "Clear answers about assessments, monitoring, treatment boundaries, reporting, managed properties, decline, and proof privacy.", "journal-overview.jpg"),
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
            "title": f"{h1} | San Diego Palm Protection",
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
                "provider": {"@type": "LocalBusiness", "name": "San Diego Palm Protection", "url": BASE_URL},
                "name": data["h1"], "areaServed": "North County San Diego",
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
