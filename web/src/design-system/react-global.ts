// The design-system bundle is a classic script that reads `window.React`
// and publishes its components on `window.Donut`. Expose React first; this
// module must be imported before the bundle.
import * as React from "react";

declare global {
  interface Window {
    React: typeof React;
  }
}

window.React = React;
