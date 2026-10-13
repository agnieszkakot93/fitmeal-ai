// Donut design system — React 18, window.Donut. Types are documentation.
import * as React from 'react';
type Tone = 'neutral' | 'basil' | 'paprika' | 'warning' | 'danger' | 'premium' | 'solid';
type Macro = 'protein' | 'carbs' | 'fat';
export interface DeltaItem { value: number; unit: 'kcal' | 'g' | 'PLN'; letter?: 'P' | 'C' | 'F'; tone?: 'good' | 'bad' | 'neutral' }
export declare const Icon: React.FC<{ name: string; size?: number; weight?: number; label?: string; className?: string }> & { names: string[] };
export declare const Button: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' | 'quiet' | 'danger' | 'premium' | 'accent' | 'glass' | 'glass-prominent'; size?: 'lg' | 'md' | 'sm'; icon?: string; trailingIcon?: string; block?: boolean }>;
export declare const IconButton: React.FC<{ icon: string; label: string; variant?: 'glass' | 'glass-prominent' | 'sunken' | 'raised'; size?: number; onClick?: () => void; disabled?: boolean; 'aria-describedby'?: string; 'aria-disabled'?: boolean | 'true' | 'false'; 'aria-haspopup'?: 'menu' | 'dialog' | boolean; 'aria-expanded'?: boolean }>;
export declare const Chip: React.FC<{ selected?: boolean; onChange?: (v: boolean) => void; icon?: string; disabled?: boolean; children: React.ReactNode }>;
export declare const SegmentedControl: React.FC<{ options: (string | { value: string; label: string })[]; value?: string; onChange?: (v: string) => void; label?: string }>;
export declare const SelectCard: React.FC<{ title: string; description?: string; icon?: string; meta?: string; selected?: boolean; multiple?: boolean; onChange?: (v: boolean) => void }>;
export declare const Toggle: React.FC<{ label: string; description?: string; checked?: boolean; onChange?: (v: boolean) => void; disabled?: boolean }>;
export declare const Checkbox: React.FC<{ label: string; checked?: boolean; onChange?: (v: boolean) => void }>;
export declare const NumberField: React.FC<{ label?: string; value?: string; unit?: string; hint?: string; error?: string; large?: boolean; placeholder?: string }>;
export declare const ExclusionRow: React.FC<{ name: string; examples?: string; severity?: 'allergy' | 'intolerance' | 'dislike' | 'prefer-not' | null; relaxed?: boolean; onChange?: (v: string | null) => void }>;
export declare const DistributionEditor: React.FC<{ kcal: number; meals: { name: string; pct: number }[] }>;
export declare const MacroRing: React.FC<{ value: number; target: number; macros?: Partial<Record<Macro, { share: number }>>; size?: number; stroke?: number; label?: string }>;
export declare const MacroBar: React.FC<{ macro: Macro; value: number; target: number; mode?: 'min' | 'exact'; compact?: boolean }>;
export declare const MacroLine: React.FC<{ kcal?: number; protein?: number; carbs?: number; fat?: number; size?: 'lg' }>;
export declare const Delta: React.FC<{ items: DeltaItem[] }>;
export declare const Badge: React.FC<{ tone?: Tone; icon?: string; children: React.ReactNode }>;
export declare const Notice: React.FC<{ tone?: 'danger' | 'warning' | 'info' | 'offline'; title?: string; body?: string; items?: React.ReactNode[]; actions?: ({ label: string; icon?: string } | string)[]; icon?: string }>;
export declare const MealCard: React.FC<{ slot: string; time?: string; title: string; kcal: number; protein: number; carbs?: number; fat?: number; badges?: { label: string; tone?: Tone; icon?: string }[]; status?: 'planned' | 'cooked' | 'eaten' | 'skipped'; prep?: { portion: string; cook: string; eatBy: string }; swappable?: boolean; actions?: boolean; onToggleEaten?: false }>;
export declare const DayStrip: React.FC<{ days: { name: string; num: number; state?: 'planned' | 'done' | 'prep' }[]; selected?: number }>;
export declare const RebalanceProposal: React.FC<{ title?: string; body?: string; adjustments?: { meal: string; portion: string; kcal: string; accepted?: boolean }[]; locked?: { meal: string; reason: string }[]; before?: { kcal: number; protein: number }; after?: { kcal: number; protein: number }; cta?: string; unreachable?: boolean }>;
export declare const IngredientRow: React.FC<{ name: string; amount: string; was?: string; role?: string; excluded?: string; checkable?: boolean; checked?: boolean; swappable?: boolean }>;
export declare const SwapOption: React.FC<{ title: string; amount?: string; delta?: DeltaItem[]; best?: boolean; note?: string; selected?: boolean }>;
export declare const ChangeItem: React.FC<{ what: string; effect: string; icon?: string; rejected?: boolean; decidable?: boolean }>;
export declare const CompareCard: React.FC<{ original: { kcal: number; protein: number }; yours: { kcal: number; protein: number }; target?: string; found?: boolean; foundLabel?: string; originalLabel?: string; yoursLabel?: string; missed?: string; sourceKcal?: number }>;
export declare const ConfidencePrompt: React.FC<{ raw: string; question: string; options: string[]; selected?: string; note?: string }>;
export declare const ShoppingItem: React.FC<{ name: string; qty: string; packages?: string; checked?: boolean; extra?: string; /** Phase 2 */ pantry?: string; /** Phase 2 */ price?: string }>;
export declare const StatTile: React.FC<{ value: string; unit?: string; label: string; note?: string }>;
export declare const PlanCard: React.FC<{ tier?: 'free' | 'standard' | 'premium'; name: string; flag?: string; promise?: string; price: string; period?: string; subprice?: string; features?: string[]; selected?: boolean; soon?: boolean }>;
export declare const LockedPreview: React.FC<{ kicker: string; stats: { label: string; from: string; to: string }[]; note?: string; cta: string; tier?: 'standard' | 'premium' }>;
export declare const SectionHeader: React.FC<{ title: string; meta?: string; action?: string }>;
export declare const NavBar: React.FC<{ title: string; large?: boolean; subtitle?: string; back?: string; trailing?: React.ReactNode; avatar?: React.ReactNode; overlay?: boolean }>;
export declare const Avatar: React.FC<{ initials?: string; size?: number; badge?: boolean | string; label?: string }>;
export declare const OnboardingProgress: React.FC<{ step: number; total?: number }>;
export declare const TabBar: React.FC<{ active?: 'today' | 'plan' | 'shopping'; accessory?: React.ReactNode; minimized?: boolean; lang?: 'en' | 'pl'; links?: boolean; hrefs?: Partial<Record<'today' | 'plan' | 'shopping', string>>; onNavigate?: (id: 'today' | 'plan' | 'shopping', e: React.MouseEvent) => void; onAdd?: () => void }>;
export declare const BottomAccessory: React.FC<{ icon?: string; tone?: 'basil' | 'paprika'; title: string; subtitle?: string; action?: string; progress?: number }>;
export declare const RecipeHero: React.FC<{ macros?: { protein: number; carbs: number; fat: number }; height?: number; tone?: 'paprika' | 'basil' | 'premium'; className?: string; children?: React.ReactNode }>;
export declare const PhoneFrame: React.FC<{ caption?: string; theme?: 'light' | 'dark'; children?: React.ReactNode }>;

// ---------- Web (responsive PWA) ----------
type Lang = 'en' | 'pl';
type TabId = 'today' | 'plan' | 'shopping';
type TabHrefs = Partial<Record<TabId, string>>;
// TabBar (above) also accepts, for web: { lang?: Lang; links?: boolean; hrefs?: TabHrefs; onNavigate?: (id: TabId, e: React.MouseEvent) => void; onAdd?: () => void }
export declare const AppShell: React.FC<{
  active?: TabId; lang?: Lang; hrefs?: TabHrefs; onNavigate?: (id: TabId, e: React.MouseEvent) => void; onAdd?: () => void;
  /** Profile entry: an Avatar. Shown in SideNav at md/lg; put another in TopBar for phone. */ avatar?: React.ReactNode;
  /** OfflineBanner, rendered first in the top zone. */ banner?: React.ReactNode;
  /** TopBar (holds the page h1). */ header?: React.ReactNode;
  notices?: React.ReactNode;
  /** Right rail at lg (sticky); stacks after the top zone below lg. */ aside?: React.ReactNode; asideLabel?: string;
  /** Phone only: BottomAccessory above the TabBar. */ accessory?: React.ReactNode;
  /** Toast elements; the live region is always mounted. */ toasts?: React.ReactNode;
  /** false hides SideNav and TabBar (onboarding). */ nav?: boolean;
  /** Onboarding column, max 560 px. */ narrow?: boolean;
  /** The shell is its own scroller (showcases, embedded frames). */ contained?: boolean;
  mainId?: string; style?: React.CSSProperties; children?: React.ReactNode;
}>;
export declare const SideNav: React.FC<{ active?: TabId; lang?: Lang; hrefs?: TabHrefs; onNavigate?: (id: TabId, e: React.MouseEvent) => void; onAdd?: () => void; avatar?: React.ReactNode; /** auto (default) follows AppShell: rail at md, full at lg */ variant?: 'auto' | 'rail' | 'full' }>;
export declare const TopBar: React.FC<{ title: string; subtitle?: string; large?: boolean; back?: { label: string; href?: string; onClick?: (e: React.MouseEvent) => void }; actions?: React.ReactNode; avatar?: React.ReactNode; sticky?: boolean; level?: 1 | 2; titleId?: string; lang?: Lang }>;
interface DialogProps {
  open?: boolean; onClose?: (reason: 'escape' | 'backdrop' | 'close') => void; title: string; description?: string;
  actions?: React.ReactNode; children?: React.ReactNode; closeButton?: boolean; closeOnBackdrop?: boolean; lang?: Lang;
  /** Showcase only: renders the panel inline, not modal. */ preview?: boolean;
}
export declare const Dialog: React.FC<DialogProps>;
export declare const Sheet: React.FC<DialogProps & { /** auto: bottom sheet below 600 px, Dialog at >= 600 px */ presentation?: 'auto' | 'sheet' | 'modal' }>;
export declare const ToastRegion: React.FC<{ children?: React.ReactNode }>;
export declare const Toast: React.FC<{ message: React.ReactNode; action?: { label: string; onClick?: () => void }; icon?: string; /** ms, default 10000; 0 = stays */ duration?: number; onDismiss?: (reason: 'timeout' | 'action' | 'close' | 'escape') => void; lang?: Lang }>;
interface FieldProps { label: string; hint?: string; error?: string; optional?: boolean; id?: string; disabled?: boolean; required?: boolean; name?: string; lang?: Lang }
export declare const TextField: React.FC<FieldProps & { value?: string; defaultValue?: string; onChange?: (v: string, e: React.ChangeEvent) => void; type?: 'text' | 'email' | 'search' | 'url' | 'tel' | 'password'; autoComplete?: string; placeholder?: string; multiline?: boolean; rows?: number; maxLength?: number; inputMode?: string }>;
export declare const Select: React.FC<FieldProps & { options: (string | { value: string; label: string; disabled?: boolean })[]; value?: string; defaultValue?: string; onChange?: (v: string, e: React.ChangeEvent) => void; placeholder?: string; autoComplete?: string }>;
export interface WeekMeal { title: string; kcal: number; protein: number; status?: 'planned' | 'cooked' | 'eaten' | 'skipped'; href?: string; badges?: { label: string; tone?: Tone; icon?: string }[]; /** same id across cards cooked in one batch */ batch?: string; /** future day: Eat is aria-disabled with this hint */ eatHint?: string; /** offline: status change waiting to sync */ queued?: boolean }
export declare const WeekTable: React.FC<{
  days: { id: string; name: string; date: string; label?: string; today?: boolean; cook?: boolean; totals?: { kcal: number; protein: number } }[];
  slots: { id: string; label: string }[];
  meals: Record<string, Record<string, WeekMeal>>;
  caption?: string; showCaption?: boolean; headingLevel?: 2 | 3; lang?: Lang;
  /** auto: table at >= 1024 px viewport, list below */ layout?: 'auto' | 'table' | 'list';
  onEat?: (dayId: string, slotId: string) => void; onOpen?: (dayId: string, slotId: string) => void;
}>;
export declare const OfflineBanner: React.FC<{ state?: 'none' | 'offline' | 'syncing' | 'synced' | 'stuck'; pending?: number; onRetry?: () => void; sticky?: boolean; lang?: Lang }>;
export declare const InstallPrompt: React.FC<{ platform?: 'prompt' | 'ios' | 'none'; onInstall?: () => void; onDismiss?: () => void; lang?: Lang }>;
export declare const ProfileFileCard: React.FC<{ mode?: 'both' | 'download' | 'load'; title?: string; lastDownloaded?: string; persistRefused?: boolean; error?: boolean | string; onDownload?: () => void; onLoad?: (file: File) => void; lang?: Lang }>;
export declare const Tooltip: React.FC<{ label: string; children: React.ReactElement; placement?: 'bottom' | 'top' | 'end'; /** true: adds aria-describedby (extra info); false (default): visual repeat of the trigger's aria-label */ describe?: boolean; delay?: number; /** showcase / tests */ open?: boolean }>;
