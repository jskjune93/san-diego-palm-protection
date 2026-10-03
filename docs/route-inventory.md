# Route inventory and disposition

51 public HTML routes are generated and validated. Two superseded audience routes are preserved through permanent redirects into the canonical service and inquiry page.

| Route | Disposition | Commercial or educational purpose |
|---|---|---|
| `/about.html` | created | Owner identity, qualifications, field process, and trust |
| `/canary-island-date-palm-care-san-diego.html` | restructured | Species-specific discovery route |
| `/cidp-risk-checklist.html` | restructured | Educational observation checklist |
| `/` | restructured | Commercial orientation and three-pillar gateway |
| `/old-escondido-palm-preservation.html` | restructured | Community documentation and exact UFMP context |
| `/palm-care-escondido.html` | consolidated in place | Escondido local discovery route |
| `/palm-care-poway.html` | consolidated in place | Poway local discovery route |
| `/palm-care-rancho-santa-fe.html` | consolidated in place | Rancho Santa Fe local discovery route |
| `/palm-faq-san-diego.html` | restructured | Educational decision support |
| `/palm-journal-new.html` | restructured | Field evidence library and Journal gateway |
| `/palm-journal/cidp-assessment-local-palm-health-concerns.html` | preserved / regenerated | Palm Journal evidence: Palm Health and Stewardship |
| `/palm-journal/classic-old-escondido-canary-island-date-palm.html` | preserved / regenerated | Palm Journal evidence: Field Observation |
| `/palm-journal/documented-loss/` | restructured | Confirmed-loss collection with attribution boundaries |
| `/palm-journal/grand-ave-cidp.html` | preserved / regenerated | Palm Journal evidence: Field Observation |
| `/palm-journal/grand-ave-old-escondido.html` | preserved / regenerated | Palm Journal evidence: Palm Health and Stewardship |
| `/palm-journal/healthy-palm-growth.html` | preserved / regenerated | Palm Journal evidence: Palm Health and Stewardship |
| `/palm-journal/i-have-seen-this-pattern-before.html` | preserved / regenerated | Palm Journal evidence: Palm Protection |
| `/palm-journal/las-palmas-no-reply-then-the-saws.html` | preserved / regenerated | Palm Journal evidence: Documented Loss |
| `/palm-journal/local-is-the-point.html` | preserved / regenerated | Palm Journal evidence: Palm Stewardship |
| `/palm-journal/monitoring-mature-cidp-after-palm-weevil-activity.html` | preserved / regenerated | Palm Journal evidence: SAPW Documentation |
| `/palm-journal/old-escondido-adult-sapw-declining-cidp.html` | preserved / regenerated | Palm Journal evidence: SAPW Documentation |
| `/palm-journal/old-escondido-albert-h-beach-house-palms.html` | preserved / regenerated | Palm Journal evidence: Preservation and Historic Landscapes |
| `/palm-journal/old-escondido-cidp-collection.html` | preserved / regenerated | Palm Journal evidence: Preservation and Historic Landscapes |
| `/palm-journal/old-escondido-cidp-icons-and-change.html` | preserved / regenerated | Palm Journal evidence: Palm Health and Stewardship |
| `/palm-journal/old-escondido-historic-canary-island-date-palm.html` | preserved / regenerated | Palm Journal evidence: Preservation and Historic Landscapes |
| `/palm-journal/old-escondido-living-landmarks.html` | preserved / regenerated | Palm Journal evidence: Preservation and Historic Landscapes |
| `/palm-journal/old-escondido-mature-cidps-deserve-a-baseline.html` | preserved / regenerated | Palm Journal evidence: Civic Documentation |
| `/palm-journal/old-escondido-mexican-fan-palm-curve.html` | preserved / regenerated | Palm Journal evidence: Preservation and Historic Landscapes |
| `/palm-journal/old-escondido-palm-weevils.html` | preserved / regenerated | Palm Journal evidence: SAPW Documentation |
| `/palm-journal/palm-stewardship-solving-the-whole-problem.html` | preserved / regenerated | Palm Journal evidence: Palm Stewardship |
| `/palm-journal/poway-old-winery-cidp.html` | preserved / regenerated | Palm Journal evidence: Preservation and Historic Landscapes |
| `/palm-journal/rancho-santa-fe-palm-walk.html` | preserved / regenerated | Palm Journal evidence: Field Observation |
| `/palm-journal/september-treatment-day.html` | preserved / regenerated | Palm Journal evidence: Protection & Treatment |
| `/palm-journal/the-palm-is-only-part-of-the-site.html` | preserved / regenerated | Palm Journal evidence: Field Observation |
| `/palm-journal/the-palm-record-outlives-the-palm.html` | preserved / regenerated | Palm Journal evidence: Field Documentation |
| `/palm-journal/the-palms-that-complete-old-escondidos-historic-homes.html` | preserved / regenerated | Palm Journal evidence: Historic Homes and Landscapes |
| `/palm-journal/when-palms-were-california-gold/` | preserved / regenerated | Palm Journal evidence: Palm Preservation |
| `/palm-journal/when-sapw-became-local.html` | preserved / regenerated | Palm Journal evidence: Owner-Documented Field Record |
| `/palm-journal/who-owns-your-palm-treatment-company.html` | preserved / regenerated | Palm Journal evidence: Palm Stewardship |
| `/palm-proof-examples.html` | created | Approved sanitized proof presentation and privacy boundary |
| `/palm-records-monitoring-verification.html` | restructured | Canonical service overview and inquiry |
| `/palm-removal-coordination.html` | restructured | Decline, removal, documented loss, and replacement pathway |
| `/palm-sourcing-installation.html` | restructured | Replacement sourcing and installation planning |
| `/palm-stewardship-plans.html` | restructured | Protection and treatment planning |
| `/quarterly-palm-care-san-diego.html` | restructured | Annual mature-palm protection and recurring treatment pathway; URL preserved |
| `/report-a-palm.html` | restructured | Permissioned private observation handoff |
| `/sapw.html` | restructured | SAPW education, risk, and assessment gateway |
| `/south-american-palm-weevil-treatment-san-diego.html` | consolidated in place | Treatment-specific discovery route into canonical protection pathway |
| `/specimen-palms-cycads.html` | restructured | Specimen selection and replacement education |
| `/urban-forest-palm-documentation.html` | created | Municipal, public-agency, institutional, and urban-forest palm documentation support |

## Permanent redirects

| Legacy route | Canonical destination |
|---|---|
| `/managed-property-palm-services.html` | `/palm-records-monitoring-verification.html#organization-inquiry` |
| `/residential-palm-assessment.html` | `/palm-records-monitoring-verification.html#homeowner-inquiry` |

## Consolidation policy

Local and species pages retain search/discovery roles but point into the canonical service architecture. They do not define competing service names, navigation, credential wording, or design systems. Superseded audience pages redirect to the matching inquiry on the canonical service page.

SAPW visual exhibit: `/sapw.html` is the original SDPP photo and film page. The apex and www `southamericanpalmweevil.com` roots rewrite to it without changing the visitor-facing domain. Existing SDPP links and the SDPP canonical URL remain intact.

SAPW domain dispatch uses explicit Vercel routes before the filesystem phase. Ordinary rewrites are evaluated after static index.html and therefore do not override the existing root document. Existing redirect rules are retained as equivalent ordered routes.

| `/palm-journal/where-we-care-for-palms-october-2026.html` | created | Dated customer reach update, preventive-care education, and assessment inquiry |
