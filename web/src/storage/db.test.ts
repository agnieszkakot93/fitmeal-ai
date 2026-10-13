import { afterEach, describe, expect, it } from "vitest";

import { closeDonutDB, kvDelete, kvGet, kvSet, outboxAdd, outboxAll } from "./db";

afterEach(async () => {
  await closeDonutDB();
  await new Promise<void>((resolve) => {
    const req = indexedDB.deleteDatabase("donut");
    req.onsuccess = req.onerror = () => {
      resolve();
    };
  });
});

describe("IndexedDB wrapper", () => {
  it("stores and deletes key-value records", async () => {
    await kvSet("active-plan", { id: "p1" });
    expect(await kvGet("active-plan")).toEqual({ id: "p1" });
    await kvDelete("active-plan");
    expect(await kvGet("active-plan")).toBeUndefined();
  });

  it("queues outbox entries in order", async () => {
    await outboxAdd({ kind: "meal-status", payload: { slot: 1 } });
    await outboxAdd({ kind: "shopping-check", payload: { item: 2 } });
    const entries = await outboxAll();
    expect(entries.map((e) => e.kind)).toEqual(["meal-status", "shopping-check"]);
    expect(entries[0]!.id).toBeLessThan(entries[1]!.id!);
  });
});
