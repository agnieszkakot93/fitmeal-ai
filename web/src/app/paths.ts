export const paths = {
  onboarding: "/onboarding",
  today: "/today",
  plan: "/plan",
  shopping: "/shopping",
  settings: "/settings",
  import: "/import",
  recipe: (recipeId: string) => `/recipes/${encodeURIComponent(recipeId)}`,
} as const;
