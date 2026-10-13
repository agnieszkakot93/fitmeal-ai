// The Donut design system, used straight from design/design-system/ (not
// copied): its React bundle, stylesheet and typings.
import "./react-global";
import "../../../design/design-system/components/bundle.js";
import "../../../design/design-system/components/bundle.css";

import type * as DS from "../../../design/design-system/components/index";

declare global {
  interface Window {
    Donut: typeof DS;
  }
}

export const {
  AppShell,
  Avatar,
  Button,
  Notice,
  OnboardingProgress,
  SegmentedControl,
  Select,
  TopBar,
} = window.Donut;

export type TabId = "today" | "plan" | "shopping";
