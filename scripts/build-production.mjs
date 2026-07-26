import { cp, mkdir, readFile, readdir, rm, stat, writeFile } from "node:fs/promises";
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
    .filter(name => name.endsWith(".html"))
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
  if (routes.length !== 40) throw new Error(`Expected 40 HTML routes, found ${routes.length}`);

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

  const manifest = {
    schema_version: 1,
    generated_from: "allowlisted public routes and referenced assets",
    html_routes: routes.length,
    files: [...copied].map(item => item.split(path.sep).join("/")).sort(),
  };
  await writeFile(path.join(output, "production-manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
  console.log(`Production output ready: ${routes.length} routes, ${copied.size + 1} files.`);
}

await main();
