import { Link } from "react-router";

import { useT } from "../../i18n/useT";
import { stepPath } from "./steps";

/** 02b: no way forward, only Back to 02 in case of a mis-tap. */
export function Under18Page() {
  const t = useT();
  return (
    <>
      <p className="dn-placeholder">{t("onb.age.stop.body")}</p>
      <p>
        <Link className="fm-link" to={stepPath("age")}>
          {t("onb.age.stop.back")}
        </Link>
      </p>
    </>
  );
}
