// IndexedDB wrapper (stub). Holds the offline copies from Dev Plan §3.1: the
// health-profile copy, the active plan and its recipes, the shopping list,
// and the outbox of meal-status and checkmark changes waiting to sync.
// Never auth tokens.
import { openDB } from "idb";
import type { DBSchema, IDBPDatabase } from "idb";

export const DB_NAME = "donut";
export const DB_VERSION = 1;

export interface OutboxEntry {
  id?: number;
  /** e.g. "meal-status", "shopping-check" */
  kind: string;
  payload: unknown;
  createdAt: number;
}

interface DonutDB extends DBSchema {
  /** Key-value records: "profile", "active-plan", "shopping-list" … */
  kv: { key: string; value: unknown };
  recipes: { key: string; value: { id: string } & Record<string, unknown> };
  outbox: { key: number; value: OutboxEntry };
}

let dbPromise: Promise<IDBPDatabase<DonutDB>> | null = null;

export function openDonutDB(): Promise<IDBPDatabase<DonutDB>> {
  dbPromise ??= openDB<DonutDB>(DB_NAME, DB_VERSION, {
    upgrade(db) {
      db.createObjectStore("kv");
      db.createObjectStore("recipes", { keyPath: "id" });
      db.createObjectStore("outbox", { keyPath: "id", autoIncrement: true });
    },
  });
  return dbPromise;
}

export async function kvGet<T>(key: string): Promise<T | undefined> {
  return (await (await openDonutDB()).get("kv", key)) as T | undefined;
}

export async function kvSet(key: string, value: unknown): Promise<void> {
  await (await openDonutDB()).put("kv", value, key);
}

export async function kvDelete(key: string): Promise<void> {
  await (await openDonutDB()).delete("kv", key);
}

export async function outboxAdd(entry: Omit<OutboxEntry, "id" | "createdAt">): Promise<number> {
  return (await openDonutDB()).add("outbox", { ...entry, createdAt: Date.now() });
}

export async function outboxAll(): Promise<OutboxEntry[]> {
  return (await openDonutDB()).getAll("outbox");
}

/** Close and forget the connection (tests, account deletion). */
export async function closeDonutDB(): Promise<void> {
  if (dbPromise) (await dbPromise).close();
  dbPromise = null;
}
