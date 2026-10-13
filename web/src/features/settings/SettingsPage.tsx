import { Select } from "../../design-system";
import { useLocale } from "../../i18n/LocaleProvider";
import { LOCALES, isLocale } from "../../i18n/locale";
import { useT } from "../../i18n/useT";

/** Settings; for now only the app language. */
export function SettingsPage() {
  const t = useT();
  const { locale, setLocale } = useLocale();
  return (
    <Select
      id="settings-language"
      label={t("settings.language.label")}
      hint={t("settings.language.hint")}
      lang={locale}
      value={locale}
      options={LOCALES.map((value) => ({ value, label: t(`settings.language.${value}`) }))}
      onChange={(value) => {
        if (isLocale(value)) setLocale(value);
      }}
    />
  );
}
