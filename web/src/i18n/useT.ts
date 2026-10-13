import { useCallback } from "react";
import { useIntl } from "react-intl";
import type { PrimitiveType } from "react-intl";

import type { MessageId } from "./locale";

/** Typed message lookup: only ids that exist in the message files compile. */
export function useT() {
  const intl = useIntl();
  return useCallback(
    (id: MessageId, values?: Record<string, PrimitiveType>) => intl.formatMessage({ id }, values),
    [intl],
  );
}
