---
name: review-pr
description: Review a Donut pull request (number, branch, or the current diff) and give an APPROVE / REQUEST CHANGES / COMMENT verdict, running the code-reviewer agent and, for sensitive areas, the security-engineer. Use when asked to "review this PR", "approve this MR", "code review before merge". Pass --post to publish the review on GitHub.
---

# Review a pull request

Arguments: `$ARGUMENTS` — a PR number, a branch name, or nothing (current branch vs `develop`). `--post` publishes the review on GitHub.

1. **Resolve the target.** For a PR number, read it with the GitHub tools (`pull_request_read`: details, diff, files, existing reviews, check runs) and check out its head branch locally. For a branch, check it out. Note the base branch (default `develop`).
2. **Pick reviewers by changed paths:**
   - Always: `code-reviewer`.
   - Also `security-engineer` when the diff touches auth, tokens, payments/StoreKit, user or health data, URL/PDF import, LLM prompts, secrets, `infra/` or `.github/workflows/`.
   Run them in parallel, giving each the PR number, base, head and description.
3. **Merge the results** into one report in the `code-reviewer` output format: deduplicate findings, keep the higher severity, and take the stricter verdict (any blocker or major → REQUEST CHANGES).
4. **CI.** Read the PR's check runs. A red required check means REQUEST CHANGES, whatever the code looks like.
5. **Report** the verdict in chat. With `--post`, publish one GitHub review: pending review → inline comments on exact lines → submit with the matching event. If GitHub rejects `APPROVE` (the PR author is this account), submit `COMMENT` with "Verdict: APPROVE" in the body and tell the user a human needs to click approve. End every post with the Claude Code footer.

Never merge, never push to the PR branch, and never approve with a failing check or an unread file.
