import { Placeholder } from "../../app/Placeholder";
import { useT } from "../../i18n/useT";

/** 01 Welcome and the 14 steps (docs/design/screens/onboarding.md). */
export function OnboardingPage() {
  const t = useT();
  return (
    <Placeholder>
      <p className="dn-placeholder">{t("onb.welcome.subtitle")}</p>
    </Placeholder>
  );
}
