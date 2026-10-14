import { useNavigate } from "react-router";

import { paths } from "../../app/paths";
import { Placeholder } from "../../app/Placeholder";
import { Button } from "../../design-system";
import { useT } from "../../i18n/useT";
import { completeStep, finishOnboarding, setUnder18 } from "./progress";
import { TOTAL_STEPS, UNDER_18_PATH, nextStep, stepNumber, stepPath } from "./steps";
import type { StepId } from "./steps";

/** One onboarding step (placeholder body). Its answer controls come with the real screens. */
export function OnboardingStepPage({ step }: { step: StepId }) {
  const t = useT();
  const navigate = useNavigate();
  const n = stepNumber(step);

  async function next() {
    const following = nextStep(step);
    if (step !== "welcome") await completeStep(step);
    if (following) {
      await navigate(stepPath(following));
    } else {
      await finishOnboarding();
      await navigate(paths.today);
    }
  }

  const progressLabel = t("onb.progress", { step: n, total: TOTAL_STEPS });
  return (
    <Placeholder>
      {step !== "welcome" && (
        <>
          <p className="dn-placeholder" aria-hidden="true">
            {progressLabel}
          </p>
          <progress
            className="dn-progress"
            max={TOTAL_STEPS}
            value={n}
            aria-label={progressLabel}
          />
        </>
      )}
      {step === "welcome" && <p className="dn-placeholder">{t("onb.welcome.subtitle")}</p>}
      <div className="dn-actions">
        {step === "age" ? (
          <>
            <Button
              variant="primary"
              onClick={() => {
                setUnder18(false);
                void next();
              }}
            >
              {t("onb.age.yes")}
            </Button>
            <Button
              variant="primary"
              onClick={() => {
                setUnder18(true);
                void navigate(UNDER_18_PATH);
              }}
            >
              {t("onb.age.no")}
            </Button>
          </>
        ) : (
          <Button variant="primary" onClick={() => void next()}>
            {t(
              step === "welcome"
                ? "onb.welcome.cta"
                : step === "cooking"
                  ? "onb.cook.cta"
                  : "onb.next",
            )}
          </Button>
        )}
      </div>
    </Placeholder>
  );
}
