const request = require("supertest");
const app = require("../app");

describe("GET /", () => {
  it("repond 200 et affiche le message DevOps", async () => {
    const res = await request(app).get("/");
    expect(res.status).toBe(200);
    expect(res.text).toMatch(/Bonjour DevOps/);
  });
});

describe("GET /health", () => {
  it("repond 200 avec le statut ok", async () => {
    const res = await request(app).get("/health");
    expect(res.status).toBe(200);
    expect(res.body.status).toBe("ok");
  });
});
