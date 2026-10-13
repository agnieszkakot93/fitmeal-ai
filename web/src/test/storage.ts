import { closeDonutDB } from "../storage/db";

/** Forget everything the app stored in this test: IndexedDB and web storage. */
export async function resetStorage(): Promise<void> {
  window.localStorage.clear();
  window.sessionStorage.clear();
  await closeDonutDB();
  await new Promise<void>((resolve) => {
    const req = indexedDB.deleteDatabase("donut");
    req.onsuccess =
      req.onerror =
      req.onblocked =
        () => {
          resolve();
        };
  });
}
