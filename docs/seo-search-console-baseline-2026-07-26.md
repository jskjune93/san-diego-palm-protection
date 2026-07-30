# Search Console baseline — July 26, 2026

## Property and verification

- Property: Domain property `sandiegopalmprotection.com`
- Account role observed: verified owner
- Verification: Google DNS TXT record at the Namecheap-managed apex
- Verification completed: July 26, 2026
- The verification record is permanent and must not be removed.

## Sitemap and indexing

- Submitted sitemap: `https://www.sandiegopalmprotection.com/sitemap.xml`
- Search Console status: Success
- Submitted: July 4, 2026
- Last read at review time: July 25, 2026
- Google-discovered pages at last read: 39
- Current production sitemap: 41 canonical URLs, all returning HTTP 200
- Search Console overview: 12 indexed pages and 8 excluded pages at the time of review.
- Valid enhancements: 6 breadcrumb items; 0 invalid.
- HTTPS report: 12 HTTPS pages, 0 non-HTTPS pages.

The two-page difference between the last-read sitemap count and current production is expected: the sitemap was read before the latest approved Palm Journal release. The existing successful sitemap was retained rather than deleted and resubmitted.

### Priority inspection

The homepage, Residential Palm Assessment, Managed-property Palm Services, SAPW, Urban Forest Palm Documentation, Field Work, and the shared inquiry page were reported as indexed during URL Inspection. The homepage was last crawled by Googlebot Smartphone on July 26, 2026; crawling and indexing were allowed, fetch succeeded, and Google's selected canonical matched the declared canonical.

Four URLs appeared in the older “Discovered — currently not indexed” report:

- `/palm-removal-coordination.html`
- `/palm-sourcing-installation.html`
- `/palm-stewardship-plans.html`
- `/specimen-palms-cycads.html`

That report was last updated July 9, before the current reconstruction. Search Console validation was started on July 26 so Google can reassess those materially updated pages. This is a crawl/indexing request, not a guarantee of indexing or ranking.

The newly approved `/palm-journal/when-sapw-became-local.html` article was unknown to Google at inspection time, as expected for a same-day release. An individual indexing request was made after confirming the live URL, canonical sitemap entry, and production validation. Documented Loss, the mature-CIDP monitoring article, Escondido, and Poway pages were already indexed.

## Search performance baseline

Search Console data was available from June 2 through July 24, 2026. The dataset is small and should not support broad conclusions.

| Window | Clicks | Impressions | CTR | Average position |
| --- | ---: | ---: | ---: | ---: |
| Last 7 days | 1 | 26 | 3.8% | 12.8 |
| Last 28 days | 10 | 171 | 5.8% | 10.3 |
| Available 3-month view | 20 | 246 | 8.1% | 10.4 |

For the 28-day view, desktop produced 6 clicks and 116 impressions; mobile produced 4 clicks and 55 impressions. The United States produced all 10 clicks and 157 of 171 impressions.

Leading 28-day pages included the homepage (4 clicks/44 impressions), Old Escondido preservation (4/25), the retained quarterly-care URL (1/25), and the Poway page (1/18). The legacy HTTP apex appeared with 49 impressions and no clicks; the Business Profile website URL was corrected to canonical HTTPS `www`, and the apex host redirect is being made permanent.

Top visible queries were sparse and mostly nonbranded, including local palm trimming, SAPW, palm planting, tree-health assessment, palm protection, and Canary Island date palm terms. No query had enough volume to justify a major content change.

## Google Business Profile

- Profile: verified service-area business
- Name: San Diego Palm Protection
- Primary category observed: Tree service
- Phone: `(262) 492-3135`
- Service areas: Poway, Escondido, and Rancho Santa Fe
- Physical storefront: none shown
- Website corrected from the HTTP apex to `https://www.sandiegopalmprotection.com/`
- Description corrected to the current owner-operated assessment, documentation, monitoring, protection-planning, and decline-response scope.
- The current description identifies John Krause as owner, California QAL No. 175295, Category B — Landscape Maintenance, SDPP's insured status, and the available palm services.

No category, address, or hours change was made. Those fields can create verification or suspension risk and were not shown to be factually wrong by this review.

## Technical findings and corrections

- All 41 sitemap URLs returned HTTP 200.
- Sitemap MIME type: `application/xml`.
- Sitemap URLs use the canonical HTTPS `www` host.
- The homepage declared canonical and Google-selected canonical matched.
- The apex HTTPS host used a temporary 307 redirect; a bounded Vercel host redirect corrects it to a permanent redirect while preserving paths.
- A durable validator now checks unique titles, descriptions, one H1, canonical/sitemap agreement, JSON-LD parsing, primary-page indexability, primary-page orphaning, and prohibited private or credential-confusion strings.
- Existing credential, proof, inquiry, conversion, privacy, and production validations remained green.

## 30-day monitoring checklist

1. Confirm the sitemap last-read date advances and discovered URL count reaches the current sitemap count.
2. Review the four-URL validation result without repeatedly requesting indexing.
3. Reinspect the homepage, Residential Assessment, Managed-property, Urban Forest, and newest substantial Palm Journal page.
4. Compare 7-day and 28-day clicks, impressions, CTR, and position without treating small changes as trends.
5. Check query and page reports for authentic service demand and content overlap.
6. Review Core Web Vitals when field data becomes available.
7. Confirm Google Business Profile edits are approved and the canonical website is displayed.
8. Check for new manual actions, security issues, sitemap errors, 404s, soft 404s, and canonical conflicts.
9. Publish only genuinely useful field evidence and request indexing only for material new or changed pages.
10. Keep SEO in monitoring mode unless Search Console identifies a specific defect.
