const { chromium } = require("playwright");
const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const output = path.join(root, "docs", "audit-screenshots");
const base = process.env.SDPP_AUDIT_BASE_URL || "http://127.0.0.1:8123";
const executablePath = process.env.SDPP_CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const viewports = [
  [360, 800],
  [390, 844],
  [768, 1024],
  [1366, 768],
  [1920, 1080],
];

function walk(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) return walk(target);
    return entry.name.endsWith(".html") ? [target] : [];
  });
}

const routes = [
  ...fs.readdirSync(root).filter(name => name.endsWith(".html")).map(name => path.join(root, name)),
  ...walk(path.join(root, "palm-journal")),
].sort();

function screenshotName(route, width, height) {
  const relative = path.relative(root, route).replaceAll("\\", "_").replaceAll("/", "_");
  const normalized = relative === "index.html" ? "index" : relative.replace(/\/index\.html$/, "index");
  return `${width}x${height}__${normalized}.png`;
}

(async () => {
  const browser = await chromium.launch({ executablePath, headless: true });
  fs.mkdirSync(output, { recursive: true });
  for (const [width, height] of viewports) {
    const page = await browser.newPage({ viewport: { width, height } });
    for (const route of routes) {
      const relative = path.relative(root, route).replaceAll("\\", "/");
      await page.goto(`${base}/${relative}`, { waitUntil: "networkidle" });
      await page.screenshot({
        path: path.join(output, screenshotName(route, width, height)),
        fullPage: false,
      });
    }
    await page.close();
  }
  await browser.close();
  console.log(`Rendered ${routes.length * viewports.length} current audit screenshots.`);
})().catch(error => {
  console.error(error);
  process.exit(1);
});
