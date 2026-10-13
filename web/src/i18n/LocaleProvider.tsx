import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { IntlProvider } from "react-intl";

import { DEFAULT_LOCALE, MESSAGES, loadLocale, saveLocale } from "./locale";
import type { Locale } from "./locale";

interface LocaleContextValue {
  locale: Locale;
  setLocale: (locale: Locale) => void;
}

const LocaleContext = createContext<LocaleContextValue | null>(null);

export function LocaleProvider({
  children,
  initialLocale,
}: {
  children: ReactNode;
  initialLocale?: Locale;
}) {
  const [locale, setLocaleState] = useState<Locale>(() => initialLocale ?? loadLocale());

  const setLocale = useCallback((next: Locale) => {
    setLocaleState(next);
    saveLocale(next);
  }, []);

  // WCAG 3.1.1: the page language follows the UI language.
  useEffect(() => {
    document.documentElement.lang = locale;
  }, [locale]);

  const value = useMemo(() => ({ locale, setLocale }), [locale, setLocale]);

  return (
    <LocaleContext.Provider value={value}>
      <IntlProvider locale={locale} defaultLocale={DEFAULT_LOCALE} messages={MESSAGES[locale]}>
        {children}
      </IntlProvider>
    </LocaleContext.Provider>
  );
}

export function useLocale(): LocaleContextValue {
  const value = useContext(LocaleContext);
  if (!value) throw new Error("useLocale must be used inside <LocaleProvider>");
  return value;
}
