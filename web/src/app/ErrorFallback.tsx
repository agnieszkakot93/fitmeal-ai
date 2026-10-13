import { useEffect } from "react";
import { useRouteError } from "react-router";

import { Button } from "../design-system";
import { useT } from "../i18n/useT";
import { reportError } from "../monitoring/sentry";

/** Shown instead of a page that threw. The error goes to Sentry, scrubbed. */
export function ErrorFallback() {
  const t = useT();
  return (
    <main id="main" tabIndex={-1} className="dn-error">
      <h1>{t("error.title")}</h1>
      <p className="dn-placeholder">{t("error.body")}</p>
      <Button
        variant="primary"
        onClick={() => {
          window.location.reload();
        }}
      >
        {t("error.reload")}
      </Button>
    </main>
  );
}

/** errorElement for the router: React Router catches render errors before any outer boundary. */
export function RouteError() {
  const error = useRouteError();
  useEffect(() => {
    reportError(error);
  }, [error]);
  return <ErrorFallback />;
}
