import { Link } from "react-router";

import { paths } from "../../app/paths";
import { useT } from "../../i18n/useT";

export function NotFoundPage() {
  const t = useT();
  return (
    <>
      <p className="dn-placeholder">{t("notFound.body")}</p>
      <p>
        <Link className="fm-link" to={paths.today}>
          {t("notFound.home")}
        </Link>
      </p>
    </>
  );
}
