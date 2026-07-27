const ALLOWED_HOSTNAMES = new Set([
  "sandiegopalmprotection.com",
  "www.sandiegopalmprotection.com",
]);
const WINDOW_MS = 10 * 60 * 1000;
const MAX_REQUESTS = 5;
const MAX_BODY_BYTES = 24_000;
const recentRequests = new Map();

const fieldSets = {
  homeowner: {
    label: "Homeowner palm inquiry",
    event: "homeowner-inquiry-delivered",
    required: ["name", "email", "property_city", "concern"],
    fields: [
      ["Name", "name"],
      ["Email", "email"],
      ["Phone", "phone"],
      ["Property city", "property_city"],
      ["Palm type", "palm_type"],
      ["Number of palms", "number_of_palms"],
      ["Concern or decision", "concern"],
      ["Preferred contact", "preferred_contact"],
      ["Timing or urgency", "timing"],
    ],
  },
  organization: {
    label: "Organization palm inquiry",
    event: "organization-inquiry-delivered",
    required: ["contact_name", "email", "organization", "role", "property_or_service_area", "support_requested"],
    fields: [
      ["Contact name", "contact_name"],
      ["Work email", "email"],
      ["Phone", "phone"],
      ["Organization", "organization"],
      ["Role", "role"],
      ["Property or service area", "property_or_service_area"],
      ["Approximate palm count", "approximate_palm_count"],
      ["Preferred contact", "preferred_contact"],
      ["Support requested", "support_requested"],
      ["Timing or procurement context", "timing"],
    ],
  },
};

const text = (value, max = 3000) => String(value ?? "").trim().slice(0, max);
const html = value => text(value).replace(/[&<>"']/g, character => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
})[character]);
const validEmail = value => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) && value.length <= 254;

function json(response, status, payload) {
  response.status(status);
  response.setHeader("Content-Type", "application/json; charset=utf-8");
  response.setHeader("Cache-Control", "no-store");
  return response.json(payload);
}

async function bodyFrom(request) {
  if (request.body && typeof request.body === "object") return request.body;
  const raw = typeof request.body === "string" ? request.body : "";
  if (Buffer.byteLength(raw) > MAX_BODY_BYTES) throw new Error("body_too_large");
  if ((request.headers["content-type"] || "").includes("application/json")) return JSON.parse(raw || "{}");
  return Object.fromEntries(new URLSearchParams(raw));
}

function requestIp(request) {
  return text(request.headers["x-forwarded-for"] || request.socket?.remoteAddress || "unknown", 128).split(",")[0].trim();
}

function rateLimited(key, now = Date.now()) {
  const active = (recentRequests.get(key) || []).filter(time => now - time < WINDOW_MS);
  active.push(now);
  recentRequests.set(key, active);
  return active.length > MAX_REQUESTS;
}

function configurationReady() {
  return [
    "RESEND_API_KEY",
    "TURNSTILE_SITE_KEY",
    "TURNSTILE_SECRET_KEY",
    "SDPP_INQUIRY_TO_EMAIL",
    "SDPP_INQUIRY_FROM_EMAIL",
  ].every(name => text(process.env[name]));
}

async function verifyTurnstile(token, ip, fetcher) {
  const payload = new URLSearchParams({
    secret: process.env.TURNSTILE_SECRET_KEY,
    response: token,
    remoteip: ip,
  });
  const result = await fetcher("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    body: payload,
  });
  if (!result.ok) return false;
  const verification = await result.json();
  return verification.success === true && ALLOWED_HOSTNAMES.has(verification.hostname);
}

function emailPayload(kind, data) {
  const definition = fieldSets[kind];
  const rows = definition.fields
    .map(([label, name]) => `<tr><th align="left" style="padding:6px 12px 6px 0;vertical-align:top">${html(label)}</th><td style="padding:6px 0">${html(data[name]) || "—"}</td></tr>`)
    .join("");
  return {
    from: process.env.SDPP_INQUIRY_FROM_EMAIL,
    to: [process.env.SDPP_INQUIRY_TO_EMAIL],
    reply_to: data.email,
    subject: `${definition.label} — ${text(data.name || data.contact_name, 100)}`,
    html: `<h1>${html(definition.label)}</h1><table>${rows}</table><p>Delivered from the verified SDPP website inquiry form.</p>`,
    text: `${definition.label}\n\n${definition.fields.map(([label, name]) => `${label}: ${text(data[name]) || "—"}`).join("\n")}`,
  };
}

async function deliver(payload, fetcher) {
  const result = await fetcher("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
      "Idempotency-Key": payload.idempotencyKey,
    },
    body: JSON.stringify(payload.email),
  });
  if (!result.ok) return false;
  const response = await result.json();
  return Boolean(response.id);
}

export async function handleInquiry(request, response, dependencies = {}) {
  const fetcher = dependencies.fetch || fetch;
  if (request.method === "GET") {
    return json(response, 200, {
      enabled: configurationReady(),
      turnstileSiteKey: configurationReady() ? process.env.TURNSTILE_SITE_KEY : null,
      uploadsEnabled: false,
    });
  }
  if (request.method !== "POST") {
    response.setHeader("Allow", "GET, POST");
    return json(response, 405, { ok: false, message: "Method not allowed." });
  }
  if (!configurationReady()) {
    return json(response, 503, { ok: false, message: "Direct delivery is temporarily unavailable. Please use the email link instead." });
  }

  let body;
  try {
    body = await bodyFrom(request);
  } catch {
    return json(response, 400, { ok: false, message: "The inquiry could not be read. Please review the form and try again." });
  }
  if (text(body.website)) return json(response, 400, { ok: false, message: "The inquiry could not be accepted." });

  const kind = text(body.inquiry_type, 30);
  const definition = fieldSets[kind];
  if (!definition) return json(response, 400, { ok: false, message: "Choose a valid inquiry type." });
  const data = Object.fromEntries(definition.fields.map(([, name]) => [name, text(body[name])]));
  if (definition.required.some(name => !data[name]) || !validEmail(data.email)) {
    return json(response, 400, { ok: false, message: "Complete the required fields and enter a valid email address." });
  }

  const ip = requestIp(request);
  if (rateLimited(ip)) {
    return json(response, 429, { ok: false, message: "Too many recent attempts. Please wait a few minutes or use the email link." });
  }
  if (!await verifyTurnstile(text(body["cf-turnstile-response"], 4096), ip, fetcher)) {
    return json(response, 400, { ok: false, message: "The security check was not completed. Please try again." });
  }

  const idempotencyKey = text(request.headers["x-idempotency-key"], 128);
  if (!/^[a-zA-Z0-9_-]{16,128}$/.test(idempotencyKey)) {
    return json(response, 400, { ok: false, message: "Please refresh the page and try again." });
  }
  try {
    const delivered = await deliver({ idempotencyKey, email: emailPayload(kind, data) }, fetcher);
    if (!delivered) throw new Error("delivery_failed");
  } catch {
    return json(response, 502, { ok: false, message: "Delivery could not be confirmed. Please use the email link or call or text SDPP." });
  }
  return json(response, 200, {
    ok: true,
    verified: true,
    event: definition.event,
    message: "Your inquiry was delivered to SDPP. A copy was not emailed automatically; keep this page for confirmation.",
  });
}

export default async function handler(request, response) {
  return handleInquiry(request, response);
}
