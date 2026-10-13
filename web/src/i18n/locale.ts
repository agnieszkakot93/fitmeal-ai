import en from "./messages/en.json";
import pl from "./messages/pl.json";

export const LOCALES = ["pl", "en"] as const;
export type Locale = (typeof LOCALES)[number];
/** Polish first: the app opens in Polish unless the user picked English. */
export const DEFAULT_LOCALE: Locale = "pl";

export type MessageId = keyof typeof pl;
export const MESSAGES: Record<Locale, Record<MessageId, string>> = { pl, en };

// Only the language choice is kept in localStorage; never tokens or health data.
const STORAGE_KEY = "donut.locale";

export function isLocale(value: unknown): value is Locale {
  return typeof value === "string" && (LOCALES as readonly string[]).includes(value);
}

export function loadLocale(): Locale {
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    return isLocale(stored) ? stored : DEFAULT_LOCALE;
  } catch {
    return DEFAULT_LOCALE;
  }
}

export function saveLocale(locale: Locale): void {
  try {
    window.localStorage.setItem(STORAGE_KEY, locale);
  } catch {
    // Storage can be blocked (private mode); the choice then lasts for this visit.
  }
}
