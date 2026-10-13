import { act, render, screen } from "@testing-library/react";
import { IntlMessageFormat } from "intl-messageformat";
import { afterEach, describe, expect, it } from "vitest";

import { LocaleProvider, useLocale } from "./LocaleProvider";
import { DEFAULT_LOCALE, LOCALES, MESSAGES, isLocale, loadLocale } from "./locale";
import { useT } from "./useT";

afterEach(() => {
  window.localStorage.clear();
  document.documentElement.lang = "";
});

describe("message files", () => {
  it("define the same keys in every locale", () => {
    const keys = Object.keys(MESSAGES.pl).sort();
    for (const locale of LOCALES) expect(Object.keys(MESSAGES[locale]).sort()).toEqual(keys);
  });

  it.each(LOCALES)("%s has only non-empty, valid ICU messages", (locale) => {
    for (const [id, message] of Object.entries(MESSAGES[locale])) {
      expect(message.trim(), id).not.toBe("");
      expect(() => new IntlMessageFormat(message, locale), id).not.toThrow();
    }
  });
});

describe("locale", () => {
  it("defaults to Polish", () => {
    expect(DEFAULT_LOCALE).toBe("pl");
    expect(loadLocale()).toBe("pl");
  });

  it("restores a saved choice and ignores unknown values", () => {
    window.localStorage.setItem("donut.locale", "en");
    expect(loadLocale()).toBe("en");
    window.localStorage.setItem("donut.locale", "de");
    expect(loadLocale()).toBe("pl");
    expect(isLocale("de")).toBe(false);
  });
});

function Probe() {
  const t = useT();
  const { setLocale } = useLocale();
  return (
    <>
      <h1>{t("today.title")}</h1>
      <p>{t("app.documentTitle", { page: t("plan.title") })}</p>
      <button
        type="button"
        onClick={() => {
          setLocale("en");
        }}
      >
        en
      </button>
    </>
  );
}

describe("<LocaleProvider>", () => {
  it("renders Polish and sets <html lang> by default", () => {
    render(
      <LocaleProvider>
        <Probe />
      </LocaleProvider>,
    );
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Dzisiaj");
    expect(screen.getByText("Plan · Donut")).toBeInTheDocument();
    expect(document.documentElement.lang).toBe("pl");
  });

  it("switches to English, updates <html lang> and remembers the choice", () => {
    render(
      <LocaleProvider>
        <Probe />
      </LocaleProvider>,
    );
    act(() => {
      screen.getByRole("button", { name: "en" }).click();
    });
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Today");
    expect(document.documentElement.lang).toBe("en");
    expect(window.localStorage.getItem("donut.locale")).toBe("en");
  });
});
