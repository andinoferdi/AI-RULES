// Record the observable behavior of one users.js as JSON.
// Usage: node probe_users.js <path-to-users.js>
"use strict";
const path = require("path");

const mod = require(path.resolve(process.argv[2]));

const people = [
  { firstName: "Ada", lastName: "Lovelace", nickname: "ada", isAdmin: true, active: true, email: " Ada@Example.com " },
  { firstName: "Bo", lastName: "Chen", nickname: "", isModerator: true, active: 1, email: "bo@example.com" },
  { firstName: "Cy", lastName: "Diaz", isBanned: true, isModerator: true, active: "yes", email: null },
  { firstName: "Di", lastName: "Eze", nickname: null, active: true, email: "" },
  { firstName: "Ed", lastName: "Fox", nickname: 0, active: false, email: "ed@example.com" },
  { firstName: "Flo", lastName: "Gu", isAdmin: false, isModerator: 0, isBanned: "no", active: true },
  { firstName: "Gus", lastName: undefined, nickname: "g", active: true, email: undefined },
  { firstName: "Hal", lastName: "Ito", active: true, email: "  HAL@example.com" },
];

function capture(fn) {
  try {
    const value = fn();
    return { value: value === undefined ? "<undefined>" : value };
  } catch (error) {
    return { error: String(error && error.message) };
  }
}

async function loadUserOutcome(service) {
  let returned;
  try {
    returned = mod.loadUser(service, 7);
  } catch (error) {
    return { kind: "sync-throw", error: error.message };
  }
  if (!returned || typeof returned.then !== "function") {
    return { kind: "plain-value", value: returned };
  }
  try {
    return { kind: "promise-resolved", value: await returned };
  } catch (error) {
    return { kind: "promise-rejected", error: error.message };
  }
}

(async () => {
  const services = {
    throwsSynchronously: { findById(id) { throw new Error("bad id " + id); } },
    returnsPlainValue: { findById(id) { return { id }; } },
    returnsPromise: { findById(id) { return Promise.resolve({ id }); } },
    rejects: { findById(id) { return Promise.reject(new Error("not found " + id)); } },
  };
  const record = { async_boundary: {} };
  for (const [name, service] of Object.entries(services)) {
    record.async_boundary[name] = await loadUserOutcome(service);
  }
  record.display_name = people.map((user) => capture(() => mod.displayName(user)));
  record.role_badge = people.map((user) => capture(() => mod.roleBadge(user)));
  record.active_emails = [capture(() => mod.activeEmails(people)), capture(() => mod.activeEmails([]))];
  record.summarize = [capture(() => mod.summarize(people)), capture(() => mod.summarize([]))];
  console.log(JSON.stringify(record));
})();
