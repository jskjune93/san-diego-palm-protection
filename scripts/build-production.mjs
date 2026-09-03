import { cp, mkdir, readFile, readdir, rm, stat, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "dist");
const forbiddenRoots = new Set([
  ".git", ".openai", "docs", "journal-data", "proof-data", "scripts",
  "site-config", "dist",
]);
const copied = new Set();

function insideRoot(candidate) {
  const relative = path.relative(root, candidate);
  return relative !== "" && !relative.startsWith("..") && !path.isAbsolute(relative);
}

function assertPublicSource(source) {
  const relative = path.relative(root, source);
  const first = relative.split(path.sep)[0];
  if (!insideRoot(source) || forbiddenRoots.has(first)) {
    throw new Error(`Refusing non-public source: ${relative}`);
  }
}

async function copyPublic(source) {
  const absolute = path.resolve(source);
  assertPublicSource(absolute);
  const relative = path.relative(root, absolute);
  if (copied.has(relative)) return;
  copied.add(relative);
  const destination = path.join(output, relative);
  await mkdir(path.dirname(destination), { recursive: true });
  await cp(absolute, destination);
}

async function htmlRoutes() {
  const rootHtml = (await readdir(root))
    .filter(name => name.endsWith(".html") && !new Set([
      "managed-property-palm-services.html",
      "residential-palm-assessment.html",
    ]).has(name))
    .map(name => path.join(root, name));
  const journalRoot = path.join(root, "palm-journal");
  const journal = [];
  async function walk(directory) {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const target = path.join(directory, entry.name);
      if (entry.isDirectory()) await walk(target);
      else if (entry.name.endsWith(".html")) journal.push(target);
    }
  }
  await walk(journalRoot);
  return [...rootHtml, ...journal].sort();
}

function localReferences(text) {
  const values = [];
  for (const match of text.matchAll(/(?:src|href|poster)=["']([^"'#]+)["']/gi)) values.push(match[1]);
  for (const match of text.matchAll(/srcset=["']([^"']+)["']/gi)) {
    for (const candidate of match[1].split(",")) {
      const value = candidate.trim().split(/\s+/)[0];
      if (value) values.push(value);
    }
  }
  for (const match of text.matchAll(/url\(["']?([^"')]+)["']?\)/gi)) values.push(match[1]);
  return values.filter(value =>
    !/^(?:https?:|mailto:|tel:|sms:|data:|javascript:)/i.test(value) &&
    !value.endsWith(".html") && !value.endsWith("/")
  );
}

async function main() {
  await rm(output, { recursive: true, force: true });
  await mkdir(output, { recursive: true });
  const routes = await htmlRoutes();
  if (routes.length !== 45) throw new Error(`Expected 45 HTML routes after consolidation, found ${routes.length}`);

  const referenceQueue = [];
  for (const route of routes) {
    await copyPublic(route);
    const text = await readFile(route, "utf8");
    referenceQueue.push(...localReferences(text).map(value => ({ base: path.dirname(route), value })));
  }
  for (const name of ["robots.txt", "sitemap.xml"]) await copyPublic(path.join(root, name));

  const seenReferences = new Set();
  while (referenceQueue.length) {
    const { base, value } = referenceQueue.shift();
    const clean = decodeURIComponent(value.split("?")[0]);
    const target = clean.startsWith("/")
      ? path.join(root, clean.replace(/^\/+/, ""))
      : path.resolve(base, clean);
    const key = path.normalize(target);
    if (seenReferences.has(key)) continue;
    seenReferences.add(key);
    assertPublicSource(target);
    const targetStat = await stat(target).catch(() => null);
    if (!targetStat?.isFile()) throw new Error(`Missing referenced public asset: ${path.relative(root, target)}`);
    await copyPublic(target);
    if (/\.(?:css|js)$/i.test(target)) {
      const text = await readFile(target, "utf8");
      referenceQueue.push(...localReferences(text).map(next => ({ base: path.dirname(target), value: next })));
    }
  }

  const forbiddenOperationalPatterns = [
    /not currently offering pesticide/i,
    /pesticide applications? (?:are|is) not currently/i,
    /pesticide applications? (?:are|is) not offered/i,
    /appropriately licensed treatment provider/i,
    /appropriately licensed-provider referral/i,
    /regulated work must be discussed with/i,
    /documentation, monitoring, reporting, sourcing, and coordination are available now/i,
    /pre[- ]license/i,
    /referral[- ]only treatment/i,
    /production prelicense status/i,
    /(?:sdpp|san diego palm protection) (?:cannot|can not|does not|doesn't) (?:provide )?(?:pesticide )?treat(?:ment)?/i,
    /treatment must be (?:provided|performed) by (?:a )?third[- ]party/i,
    /licensed applicator referral/i,
    /awaiting (?:its |our )?(?:license|licence|insurance)/i,
    /does not establish business[- ]level pesticide authorization/i,
    /current service scope.{0,100}(?:exclude|without|does not include|unavailable).{0,40}treatment/i,
    /(?:only|solely) (?:provides?|offers?) (?:documentation|monitoring|reporting|sourcing|coordination)/i,
    /aguilar plant care/i,
    /\b(?:industry-leading|tree doctor|complete tree care|all plant health|sapw-free|eradication)\b/i,
    /\bSDPP (?:is|employs) (?:an? )?(?:ISA )?(?:certified )?arborist\b/i,
    /\bSDPP (?:is|employs) (?:an? )?(?:licensed )?PCA\b/i,
    /\b(?:SDPP|we|our treatment|this treatment) guarantees? (?:prevention|protection|survival|recovery|results?|outcomes?)\b/i,
  ];
  for (const route of routes) {
    const relative = path.relative(root, route);
    const deployable = await readFile(path.join(output, relative), "utf8");
    for (const pattern of forbiddenOperationalPatterns) {
      if (pattern.test(deployable)) throw new Error(`Operational-status regression in ${relative}: ${pattern}`);
    }
  }
  const requiredByPage = {
    "index.html": ["California Qualified Applicator License No. 175295", "Category B — Landscape Maintenance", "Insured", "South American Palm Weevil Protection for San Diego’s Mature Palms", "licensed preventive treatment", "mature Canary Island date palms", "Request a Palm Assessment", "View Field Work", "Treatment at San Diego Botanic Garden.", "Called to address an active South American palm weevil infestation", "Chilean wine palms, Canary Island date palms, and Sylvester palms", "does not imply that every treated palm was infested", "Real photographs. Real local records."],
    "palm-records-monitoring-verification.html": ["SAPW prevention and licensed palm treatment", "South American palm weevil prevention and treatment", "Assessments &amp; baselines", "Continuing care", "Decline, recovery &amp; transplant assessment", "Sourcing, re-homing &amp; coordination", "id=\"homeowner-inquiry\"", "id=\"organization-inquiry\"", "For commercial and managed properties", "Request a Baseline", "known_palm_species", "existing_contractor", "desired_service", "preferred_contact"],
    "palm-stewardship-plans.html": ["Protection and treatment services are available"],
    "quarterly-palm-care-san-diego.html": ["Palm stewardship and preservation, visit after visit.", "fertilization", "preventive protection", "treatment", "Managed-property stewardship"],
    "palm-sourcing-installation.html": ["Sourcing guidance", "Re-homing and transplant review", "Planting coordination", "Establishment baseline", "does not claim to own nursery inventory, trucks, cranes, or relocation crews", "transplant-health assessment"],
  };
  const authoritativeLicenseStatement = "California Pest Control Business License No. 47756 · California Qualified Applicator License No. 175295 · Category B — Landscape Maintenance · Insured";
  for (const route of routes) {
    const relative = path.relative(root, route);
    const deployable = await readFile(path.join(output, relative), "utf8");
    if (!deployable.includes(authoritativeLicenseStatement)) {
      throw new Error(`Authoritative licensing statement missing in ${relative}`);
    }
    if (!deployable.includes('name="business-credentials"') || !deployable.includes('"description": "California Pest Control Business License No. 47756 · California Qualified Applicator License No. 175295 · Category B — Landscape Maintenance · Insured')) {
      throw new Error(`Licensing metadata or structured data missing in ${relative}`);
    }
  }
  for (const [relative, phrases] of Object.entries(requiredByPage)) {
    const deployable = await readFile(path.join(output, relative), "utf8");
    for (const phrase of phrases) {
      if (!deployable.includes(phrase)) throw new Error(`Operational-status requirement missing in ${relative}: ${phrase}`);
    }
  }
  const homepage = await readFile(path.join(output, "index.html"), "utf8");
  if (/background\.jpg/i.test(homepage)) {
    throw new Error("Denied Coastline Palms image must not appear in the production homepage.");
  }
  const homepageHero = homepage.match(/<section class="page-hero"[\s\S]*?<\/section>/)?.[0] || "";
  if (homepageHero.indexOf("Request a Palm Assessment") < 0 || homepageHero.indexOf("View Field Work") < 0) {
    throw new Error("Homepage hero must provide one assessment CTA and one field-evidence CTA.");
  }

  const files = [...copied].map(item => item.split(path.sep).join("/")).sort();
  const sha256_by_file = {};
  for (const relative of files) {
    const bytes = await readFile(path.join(output, relative));
    sha256_by_file[relative] = createHash("sha256").update(bytes).digest("hex");
  }
  const releaseApprovals = JSON.parse(await readFile(path.join(root, "docs", "release-data", "when-sapw-became-local-approval.json"), "utf8"));
  const sapwApproval = releaseApprovals.release_items?.["palm-journal/when-sapw-became-local.html"];
  if (!sapwApproval || sapwApproval.approval_fingerprint !== "2204939026f694390763cebe4c2250c9964bd92f6597296fef66b874074fcbba") {
    throw new Error("Approved SAPW article fingerprint is missing or stale.");
  }
  const journalEntries = JSON.parse(await readFile(path.join(root, "journal-data", "journal_entries.json"), "utf8"));
  const sapwEntry = journalEntries.find(item => item.slug === "when-sapw-became-local");
  if (!sapwEntry || sapwEntry.date !== sapwApproval.publication_date) {
    throw new Error("SAPW article date does not match the controlled release date.");
  }
  const manifest = {
    schema_version: 1,
    generated_from: "allowlisted public routes and referenced assets",
    html_routes: routes.length,
    files,
    sha256_by_file,
    approved_release_items: {
      "palm-journal/when-sapw-became-local.html": sapwApproval,
    },
  };
  await writeFile(path.join(output, "production-manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
  console.log(`Production output ready: ${routes.length} routes, ${copied.size + 1} files.`);
}

await main();
