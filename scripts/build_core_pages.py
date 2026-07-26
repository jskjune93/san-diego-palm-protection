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
        "title": "Mature Palm Protection in North County San Diego | SDPP",
        "description": "Owner-led, qualified and insured mature palm assessment, monitoring, protection, treatment, and decline response in Escondido and North County San Diego.",
        "eyebrow": "Owner-led palm protection · Old Escondido",
        "h1": "Protect Your Mature Palms in North County San Diego",
        "lede": "On-site assessments, Canary Island date palm protection, SAPW-aware risk reduction, qualified treatment, monitoring, and decline response from a local Old Escondido specialist.",
        "image": "background.jpg",
        "body": section("Mature palm care", "Assessment first. Protection when warranted. Help when a palm declines.", "SDPP works directly with homeowners and property stakeholders, from the first look at a mature palm through monitoring, qualified treatment, or response.", three_pillars()) +
        section("Local and direct", "Owner-led from Old Escondido.", "You work directly with the local specialist who visits the property, photographs the palms, explains the visible concerns, and prepares the written findings.", '<div class="field-split"><div><h3>One point of contact</h3><p>Site observations, photographs, recommendations, and follow-up stay connected instead of being handed between a sales office and a field crew.</p><p><a href="./old-escondido-palm-preservation.html">About the Old Escondido service area</a></p></div><img src="./beautiful-old_escondido-cidp.jpg" alt="Mature Canary Island date palm in Old Escondido" loading="lazy"></div>') +
        section("Canary Island date palms", "Protection informed by what is happening on the property.", "Mature Canary Island date palms face serious pressures, including South American palm weevil. A site assessment helps establish the visible condition and whether protection, closer monitoring, referral, or urgent response is appropriate.", '<div class="field-split field-split--reverse"><img src="./south-american-palm-weevil-cidp-poway.jpg" alt="Canary Island date palm observed in North County San Diego" loading="lazy"><div><h3>Start before the decision becomes urgent</h3><p>SDPP provides SAPW-aware assessment and qualified treatment within the supported site, label, authorization, and service scope.</p><p><a href="./sapw.html">Learn about SAPW warning signs</a> · <a href="./palm-stewardship-plans.html">Explore protection and treatment</a></p></div></div>', "section-tint") +
        section("A useful record", "Photographs and written findings support better palm decisions.", "Documentation is part of the field service, not a substitute for it. A baseline and recurring views make visible change easier to understand and communicate.", process([
            ("Assess", "Look at the palm, property context, access, and immediate concern."),
            ("Document", "Create dated photographs and clear written observations."),
            ("Protect or monitor", "Carry out supported work or compare the palm over time."),
            ("Respond", "Coordinate the next responsible step if decline or loss occurs."),
        ]) + '<p class="section-proof-link"><a href="./palm-proof-examples.html#sample-assessment">View a sanitized sample palm assessment</a></p>') +
        section("Managed properties and public landscapes", "Palm records that support portfolio decisions.", "SDPP provides palm-focused inventories, condition documentation, monitoring, and implementation support for managed properties, institutions, consultants, and public stakeholders.", '<p><a href="./managed-property-palm-services.html">Explore managed-property palm services</a> · <a href="./urban-forest-palm-documentation.html">Explore urban forest palm documentation</a></p>', "section-tint") +
        section("Field work", "See how observations become practical next steps.", "The public Palm Journal and Field Work page show real local palm context, documented observations, and the structure of an example report without exposing private client information.", '<div class="field-links"><a href="./palm-records-monitoring-verification.html">View all palm services</a><a href="./palm-proof-examples.html">View Field Work</a><a href="./palm-journal-new.html">Read the Palm Journal</a><a href="./palm-journal/documented-loss/">Visit Documented Loss</a></div>'),
    },
    "residential-palm-assessment.html": {
        "title": "Residential Mature Palm Assessment | San Diego Palm Protection",
        "description": "A clear residential palm assessment with baseline photographs, visible-condition findings, limitations, and written next steps.",
        "eyebrow": "On-site residential service", "h1": "Residential Mature Palm Assessment",
        "lede": "Work directly with a local specialist to understand a mature palm's visible condition, photograph the concern, and get clear written next steps before treatment, monitoring, pruning, or a property decision.",
        "image": "mature_healthy_cidp_poway_mansion.jpg",
        "body": section("Core deliverable", "Palm Condition Baseline", "The baseline fixes a date, palm identity, viewing context, and set of comparable images so future change has a reference.", cards([
            ("Site and palm context", "Location, species when supportable, landscape role, access, and the question prompting the visit."),
            ("Dated photographic record", "Consistent overview, crown, trunk, ground, and concern-detail views when access safely permits."),
            ("Visible-condition findings", "Observed features are separated from reported information, possible concerns, and confirmed findings."),
            ("Written Palm Condition Report", "A concise record of findings, certainty, limitations, recommendations, and an appropriate monitoring interval."),
        ]) + '<p class="section-proof-link"><a href="./palm-proof-examples.html#sample-assessment">See a sanitized sample report</a></p>') + section("What it is not", "Useful because its limits are explicit.", "A visual assessment cannot promise tree safety, uncover hidden conditions, replace laboratory confirmation, or guarantee a treatment outcome. Referral is recommended where the question exceeds the documented scope.", '<p class="note">Urgent structural or life-safety concerns may require a qualified arborist, emergency contractor, property authority, or other specialist. Regulated work is offered only when current credentials, authorization, label, site, and scope support it.</p>', "section-tint") +
        section("Next step", "From one visit to a monitoring record.", "When change over time matters, the baseline becomes visit one of a recurring monitoring timeline.", process([("Scope", "Identify the decision and palms."), ("Visit", "Observe and photograph accessible conditions."), ("Report", "Receive a dated written record."), ("Revisit", "Compare at a useful interval.")]))
    },
    "palm-records-monitoring-verification.html": {
        "title": "Palm Assessment, Monitoring & Documentation Services | SDPP",
        "description": "Palm condition baselines, written reporting, recurring monitoring, managed-property inventories, contractor-work verification, protection, and decline response.",
        "eyebrow": "Palm assessment and ongoing care", "h1": "Practical help for the full life of a mature palm.",
        "lede": "Start with an on-site assessment, continue with monitoring or qualified protection when appropriate, and keep one clear point of contact if the palm declines.",
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
        section("How it works", "One record connects each decision.", "The scope can stop after a single assessment or continue through treatment, monitoring, contractor coordination, response, and replacement tracking.", process([
            ("Initial inquiry", "Share the palm or property information, concern, photographs, access, and desired outcome."),
            ("Field assessment", "Document visible condition, site context, history, photographs, risk factors, and limitations."),
            ("Written record", "Receive baseline documentation, findings, uncertainties, priorities, and recommendations."),
            ("Next action", "Choose monitoring, regulated treatment, contractor coordination, urgent response, removal planning, or replacement tracking."),
            ("Follow-up", "Add comparable photographs and document visible change, completed work, and unresolved items."),
        ])) +
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
        "lede": "A dedicated inventory, monitoring, and reporting pathway for HOAs, apartment communities, property managers, institutions, commercial properties, and public stakeholders—from a small group of significant palms to a defined portfolio.",
        "image": "Las Palmas_Appartments_Healthy-CIDP.jpg",
        "body": section("Who this serves", "A clear record for the people responsible for multiple palms.", "Property managers, HOA boards, apartment and commercial portfolios, schools, campuses, institutions, consultants, and public-property stakeholders use the service when palm decisions need to remain understandable across people and time.", cards([
            ("Defined portfolio", "Scope one significant group, a site, or a larger palm portfolio; the proposal defines included locations, access, fields, and deliverables."),
            ("Structured intake", "Confirm property contacts, existing records, known concerns, treatment or work history, access, and the decisions the record needs to support."),
            ("Stable palm identity", "Assign a durable palm ID and connect it to a described or mapped location, species field, photographs, and future visits."),
        ])) +
        section("Four connected services", "Choose a baseline, recurring work, or both.", "Each service produces a usable record and can connect to treatment or response planning without making treatment a prerequisite.", cards([
            ("Baseline inventory and documentation", "Initial palm IDs, locations, species records where supportable, dated photographs, visible conditions, and property priorities."),
            ("Recurring monitoring", "Comparable photographs and structured observations over time, with priority changes and escalation flags."),
            ("Contractor and work verification", "Before-and-after documentation, supplied service records, visible completion checks, and unresolved-condition tracking."),
            ("Response and loss records", "Urgent observations, contractor handoffs, removals, documented loss, and replacement history."),
        ]), "section-tint") +
        section("What the client receives", "Property-level clarity with palm-level detail.", "Deliverables follow the agreed scope and may be one-time or recurring.", cards([
            ("Palm register", "Stable IDs, location records, species fields, baseline photographs, observed conditions, and current status."),
            ("Priority summary", "A portfolio view of urgent, near-term, routine, and watch-list items, with responsible next actions."),
            ("Written reporting", "Findings, reported history, uncertainties, limitations, recommendations, and an appropriate review interval."),
            ("Work and outcome history", "Treatment information when supplied or performed within scope, visible contractor completion, removals, losses, and replacements."),
        ])) +
        section("Observation and escalation", "Visible conditions are not automatically a diagnosis.", "SDPP separates field observations from reported history, suspected causes, laboratory confirmation, structural opinions, and other specialist determinations. Priority findings are communicated through the agreed contact and reporting method.", '<p class="note">Treatment may follow assessment where current credentials, authorization, product labeling, site conditions, and scope support it. Pruning, removal, planting, formal tree-risk opinions, engineering conclusions, laboratory diagnosis, and code determinations remain outside SDPP’s direct scope unless explicitly supported by a separately qualified provider.</p>') +
        section("Verification boundary", "Contractor-work verification records evidence; it does not certify the unknowable.", "SDPP can document visible completion, dates, supplied records, and discrepancies within an agreed scope.", '<p class="note"><strong>Limitations:</strong> verification does not certify concealed work, workmanship, structural safety, legal or code compliance, pesticide efficacy, contractor licensing, or outcomes unless a separately qualified party and explicit scope support that conclusion.</p>', "section-tint") +
        section("Municipal and urban-forest support", "Palm-focused field records for broader programs.", "Specialized palm documentation can support portfolio management and urban-forest implementation without claiming to prepare a complete municipal plan.", '<p><a href="./urban-forest-palm-documentation.html">Explore Urban Forest Palm Documentation</a> · <a href="./palm-proof-examples.html">View sample work</a> · <a href="./old-escondido-mature-palm-documentation-example.pdf" target="_blank" rel="noopener noreferrer">View the sanitized mature palm documentation example <span class="sr-only">(PDF, opens in a new tab)</span></a></p>') +
        section("Municipal context", "Accurate participation wording.", "San Diego Palm Protection submitted mature-palm documentation for consideration during the City of Escondido Urban Forest Management Plan process.", '<p class="note">This statement describes a submission for consideration. It does not state or imply City endorsement, partnership, selection, approval, or adoption.</p>')
    },
    "urban-forest-palm-documentation.html": {
        "title": "Palm Inventory, Condition Documentation & Urban Forest Support | SDPP",
        "description": "Palm inventory, condition documentation, monitoring, contractor verification, and urban-forest implementation support for managed properties and public stakeholders in North County San Diego.",
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
        section("Sample work", "Review sanitized field documentation.", "The public examples show how SDPP separates visible observations, photographs, limitations, and follow-up at residential and broader-area scales. They are example deliverables, not testimonials, diagnoses, formal risk certifications, municipal plans, endorsements, or promises of outcome.", '<p><a href="./old-escondido-mature-palm-documentation-example.pdf" target="_blank" rel="noopener noreferrer">View the mature palm documentation example <span class="sr-only">(PDF, opens in a new tab)</span></a> · <a href="./palm-proof-examples.html#sample-assessment">View the sanitized residential assessment</a> · <a href="./managed-property-palm-services.html">Explore managed-property palm services</a></p><p class="note">The Old Escondido example is a sanitized field-documentation sample. It is not a municipal endorsement or a complete Urban Forest Management Plan deliverable.</p>')
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
        "title": "Sample Palm Assessment Report | San Diego Palm Protection",
        "description": "View a sanitized sample palm assessment showing SDPP's photographic baseline, visible-condition observations, written recommendations, limitations, and follow-up guidance.",
        "eyebrow": "Field work and reporting", "h1": "See the palms, observations, and written follow-through.",
        "lede": "Public field examples show how SDPP photographs mature palms, records visible conditions, follows change, and turns an on-site visit into useful next steps.",
        "image": "evidence.jpg",
        "body": '''<section class="section sample-assessment" id="sample-assessment" aria-labelledby="sample-assessment-heading">
<div class="sample-assessment-grid">
  <div>
    <p class="eyebrow">Sample assessment</p>
    <h2 id="sample-assessment-heading">See what a documented palm assessment looks like.</h2>
    <p class="sample-assessment-lede">This sanitized field report shows the structure of an SDPP assessment: the purpose and scope of the visit, visible-condition observations, a dated photographic baseline, clearly separated questions and limitations, practical recommendations, and a defined follow-up point.</p>
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
      <a class="button" href="./old-escondido-mature-palm-documentation-example.pdf" target="_blank" rel="noopener noreferrer">View Civic Documentation Example <span class="sr-only">(PDF, opens in a new tab)</span></a>
      <a class="sample-request-link" href="./urban-forest-palm-documentation.html">Explore urban forest documentation</a>
    </div>
  </div>
  <aside class="sample-document-card" aria-label="Sanitized mature palm documentation example PDF">
    <span class="sample-document-type" aria-hidden="true">PDF</span>
    <h3>Old Escondido mature palm documentation</h3>
    <p>Eight-page public example with a repeatable field structure, representative records, monitoring value, decline and loss documentation, implementation uses, and explicit limitations.</p>
    <a href="./old-escondido-mature-palm-documentation-example.pdf" target="_blank" rel="noopener noreferrer">Open the documentation PDF <span class="sr-only">(opens in a new tab)</span></a>
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
        "description": "Qualified palm protection and treatment planning for mature palms in North County San Diego, with clear scope, site review, and follow-up.",
        "eyebrow": "Protection and treatment", "h1": "Protect a Mature Palm Before the Decision Becomes Urgent",
        "lede": "SDPP assesses the palm and site, explains the supported options, and provides qualified treatment when the current authorization, label, property conditions, and agreed scope allow it.",
        "image": "treatment.jpg",
        "body": section("Treatment availability", "SDPP currently provides regulated treatment when the job supports it.", "An on-site assessment comes first. SDPP reviews the palm, site conditions, visible symptoms, known pest pressure, treatment history, access, and client objectives before recommending or performing treatment.", '<p class="note">Regulated work proceeds only when current credentials, authorization, product labeling, site conditions, and the agreed job-specific scope support it.</p>') +
        section("When protection may be considered", "The recommendation follows the palm and the evidence.", "Mature Canary Island date palms, locally significant palms, known pest pressure, visible change, or a prevention objective may warrant assessment. A symptom or photograph alone does not establish a diagnosis or automatically justify treatment.", cards([
            ("Assessment and observation", "Document visible condition, property context, history, access, and the decision the client needs to make."),
            ("Diagnosis and confirmation", "Separate observed or reported information from suspected causes; recommend laboratory or specialist confirmation when needed."),
            ("Protection and regulated treatment", "Define only the work supported by the label, site, authorization, timing, and documented scope."),
        ]), "section-tint") +
        section("Direct field service", "Protection begins with the palm in front of us.", "Treatment can be a one-time supported action or part of an ongoing monitoring plan when repeat observation would improve the decision record.", process([("Assess", "Review the palm, site, history, and immediate concern."), ("Plan", "Define the supported treatment scope and practical limitations."), ("Treat", "Perform authorized work in accordance with applicable requirements."), ("Follow up", "Record the service and identify an appropriate monitoring interval.")])) +
        section("Records and follow-through", "The service remains understandable after the visit.", "The written record can identify the assessed palm, visible condition, supported action, service date, limitations, supplied or performed treatment history, and recommended monitoring or escalation.", '<p><a href="./quarterly-palm-care-san-diego.html">Explore recurring monitoring</a> · <a href="./palm-proof-examples.html">View sample work</a></p>') +
        section("Clear boundaries", "Qualified service without promises the evidence cannot support.", "Treatment does not guarantee prevention, control, recovery, survival, eradication, or any other outcome, and a visual visit cannot reveal every hidden condition.", cards([
            ("Supported scope", "Work proceeds only when credentials, authorization, label, site, and scope support it."),
            ("Coordinated work", "SDPP may coordinate pruning, removal, planting, or other contractor work but does not represent that work as directly performed when it falls outside the approved scope."),
            ("Professional referrals", "Formal tree-risk, structural, engineering, laboratory, municipal-code, or other specialist opinions are referred when they exceed the service scope."),
        ]), "section-tint")
    },
    "south-american-palm-weevil-treatment-san-diego.html": {
        "title": "South American Palm Weevil Protection & Treatment | SDPP",
        "description": "Assessment-first SAPW protection, regulated treatment, monitoring, and written records for supported Canary Island date palm sites in North County San Diego.",
        "eyebrow": "Protection and treatment",
        "h1": "South American Palm Weevil Protection & Treatment",
        "lede": "SDPP assesses the palm and property before recommending regulated treatment, monitoring, referral, or urgent response. Treatment is available only where the evidence, label, authorization, site, and scope support it.",
        "image": "treatment.jpg",
        "body": section("Assessment before treatment", "A site visit determines whether treatment is supportable.", "The review considers palm species, visible condition, reported history, known pest pressure, access, timing, prior treatment information, and client objectives. Photographs or a single symptom do not establish SAPW or another diagnosis.", cards([
            ("Document", "Establish dated photographs, observations, reported history, and limitations."),
            ("Decide", "Separate treatment, monitoring, confirmation, specialist referral, and urgent response paths."),
            ("Record", "Document supported treatment work and the recommended follow-up or monitoring point."),
        ])) +
        section("Conservative treatment scope", "Label, authorization, and site conditions govern the work.", "SDPP does not publish blanket intervals, application rates, mixing instructions, or guaranteed outcomes. A plan is specific to the supported job and current requirements.", '<p><a href="./palm-stewardship-plans.html">Review the Protection & Treatment pathway</a> · <a href="./quarterly-palm-care-san-diego.html">Review recurring monitoring</a></p>', "section-tint")
    },
    "sapw.html": {
        "title": "South American Palm Weevil Assessment in San Diego | SDPP",
        "description": "Local SAPW-aware assessment, Canary Island date palm protection, monitoring, and response in North County San Diego.",
        "eyebrow": "Canary Island date palm risk", "h1": "South American Palm Weevil: Warning Signs and Next Steps",
        "lede": "If a mature Canary Island date palm looks different, an on-site assessment can document what is visible and determine whether protection, monitoring, referral, or urgent response is appropriate.",
        "image": "south-american-palm-weevil-cidp-poway.jpg",
        "body": section("Look closely, act responsibly", "Visible change deserves a site-specific review.", "Crown change, frond behavior, damage, odor, debris, or other unusual conditions may warrant attention, but a photograph or single symptom does not prove a cause.", cards([("On-site assessment", "Review the palm, crown appearance, trunk, ground context, access, and reported timeline."), ("SAPW-aware protection", "Discuss qualified treatment only where the evidence, timing, site, label, and scope support it."), ("Monitoring or response", "Establish comparison photographs or coordinate a more urgent next step when warranted.")])) +
        section("Safety and certainty", "Do not turn a checklist into a diagnosis.", "Hidden decay, structural stability, pest confirmation, and treatment outcome may require different evidence or qualified specialists.", '<p class="note">Keep people away from a visibly unstable or actively failing palm and contact the appropriate emergency or tree-risk professional when life safety may be involved.</p>', "section-tint")
    },
    "old-escondido-palm-preservation.html": {
        "title": "Old Escondido Mature Palm Protection | SDPP",
        "description": "Owner-led mature palm assessment, protection, monitoring, and decline response from Old Escondido.",
        "eyebrow": "Based in Old Escondido", "h1": "Local Protection for Old Escondido's Mature Palms",
        "lede": "SDPP is an owner-led local palm service based in Old Escondido, working directly with property owners and stakeholders to assess, protect, monitor, and respond to significant palms.",
        "image": "beautiful-old_escondido-cidp.jpg",
        "body": section("Local work", "Direct attention to the palm and the property.", "The same specialist handles the site visit, photographs, written findings, and follow-up so the property context is not lost between steps.", three_pillars()) +
        section("Municipal context", "Accurate participation wording.", "San Diego Palm Protection submitted mature-palm documentation for consideration during the City of Escondido Urban Forest Management Plan process.", '<p class="note">This statement describes a submission for consideration. It does not state or imply City endorsement, partnership, selection, approval, or adoption.</p>', "section-tint")
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
    return section("Mature palm service", "Start with the palm and the property.", "SDPP works directly with owners and property stakeholders to understand the concern, document what is visible, and choose a responsible next step.", three_pillars()) + section("What to expect", "A site-specific visit and clear follow-through.", "The work begins with the palm, property context, access, recent history, and the decision you need to make.", cards([
        ("On-site assessment", "Look at the visible condition and establish useful baseline photographs."),
        ("Clear written next steps", "Explain observations, possible concerns, recommendations, and limits in plain language."),
        ("Protection, monitoring, or response", "Carry out supported work, set a useful revisit interval, or coordinate the next responsible action."),
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
