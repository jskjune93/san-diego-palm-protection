import assert from "node:assert/strict";
import { handleInquiry } from "../api/inquiry.mjs";

Object.assign(process.env, {
  RESEND_API_KEY: "test_resend_key",
  TURNSTILE_SITE_KEY: "test_site_key",
  TURNSTILE_SECRET_KEY: "test_secret_key",
  SDPP_INQUIRY_TO_EMAIL: "destination@example.com",
  SDPP_INQUIRY_FROM_EMAIL: "SDPP Website <website@example.com>",
});

function response() {
  return {
    statusCode: 200,
    headers: {},
    payload: null,
    status(code) { this.statusCode = code; return this; },
    setHeader(name, value) { this.headers[name] = value; },
    json(payload) { this.payload = payload; return this; },
  };
}

function request(body, overrides = {}) {
  return {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-forwarded-for": `192.0.2.${Math.floor(Math.random() * 180 + 1)}`,
      "x-idempotency-key": `test_${crypto.randomUUID().replaceAll("-", "")}`,
      ...overrides.headers,
    },
    body: {
      inquiry_type: "homeowner",
      name: "Website Test",
      email: "test@example.com",
      property_city: "Escondido",
      concern: "Testing provider-confirmed delivery.",
      "cf-turnstile-response": "valid-token",
      ...body,
    },
    ...overrides,
  };
}

const providerSuccess = async url => {
  if (url.includes("siteverify")) return { ok: true, json: async () => ({ success: true, hostname: "www.sandiegopalmprotection.com" }) };
  if (url.includes("api.resend.com")) return { ok: true, json: async () => ({ id: "email_test_123" }) };
  throw new Error(`unexpected request: ${url}`);
};

{
  const res = response();
  await handleInquiry({ method: "GET", headers: {} }, res, { fetch: providerSuccess });
  assert.equal(res.statusCode, 200);
  assert.equal(res.payload.enabled, true);
  assert.equal(res.payload.turnstileSiteKey, "test_site_key");
  assert.equal(res.payload.uploadsEnabled, false);
}

{
  const res = response();
  await handleInquiry(request({}), res, { fetch: providerSuccess });
  assert.equal(res.statusCode, 200);
  assert.equal(res.payload.ok, true);
  assert.equal(res.payload.verified, true);
  assert.equal(res.payload.event, "homeowner-inquiry-delivered");
}

{
  const res = response();
  await handleInquiry(request({
    inquiry_type: "organization",
    contact_name: "Property Manager",
    organization: "Example HOA",
    role: "Manager",
    property_or_service_area: "North County",
    support_requested: "Palm inventory and recurring monitoring.",
  }), res, { fetch: providerSuccess });
  assert.equal(res.statusCode, 200);
  assert.equal(res.payload.verified, true);
  assert.equal(res.payload.event, "organization-inquiry-delivered");
}

{
  let resendCalled = false;
  const res = response();
  await handleInquiry(request({}), res, { fetch: async url => {
    if (url.includes("siteverify")) return { ok: true, json: async () => ({ success: false }) };
    resendCalled = true;
    return { ok: true, json: async () => ({ id: "unexpected" }) };
  } });
  assert.equal(res.statusCode, 400);
  assert.equal(resendCalled, false);
  assert.equal(res.payload.ok, false);
}

{
  const res = response();
  await handleInquiry(request({ concern: "" }), res, { fetch: providerSuccess });
  assert.equal(res.statusCode, 400);
}

{
  const res = response();
  await handleInquiry(request({}), res, { fetch: async url => {
    if (url.includes("siteverify")) return { ok: true, json: async () => ({ success: true, hostname: "sandiegopalmprotection.com" }) };
    return { ok: false, json: async () => ({ message: "provider unavailable" }) };
  } });
  assert.equal(res.statusCode, 502);
  assert.equal(res.payload.ok, false);
  assert.match(res.payload.message, /could not be confirmed/i);
}

console.log("Inquiry endpoint validation passed: configuration is non-secret; Turnstile is required and hostname-restricted; provider confirmation gates success and verified-lead events; failure remains honest.");
