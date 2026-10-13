import type { ReactNode } from "react";

import { useT } from "../i18n/useT";

/** Stand-in body for screens that aren't built yet (docs/design/screens/). */
export function Placeholder({ children }: { children?: ReactNode }) {
  const t = useT();
  return (
    <>
      {children}
      <p className="dn-placeholder">{t("shell.placeholder")}</p>
    </>
  );
}
