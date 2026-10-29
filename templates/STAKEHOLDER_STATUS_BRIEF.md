# Stakeholder Status Brief — optional communication template

**Purpose:** Explain engineering, research, or operations progress to a
non-specialist decision-maker without discarding evidence or overstating completion.

**Scope:** Presentation style only. This template does not change Ticket
authority, test/acceptance gates, ownership, production permission, or
documentation contracts. Do not apply it to ordinary coding answers or
technical incident diagnosis unless a stakeholder summary is requested.

## Six-part storyline

1. **Problem:** What was not working, and why did it matter?
2. **Cause:** Why did it happen? Distinguish established causes from hypotheses.
3. **Action:** What did the team change or verify? Why that approach?
4. **Result:** What is different now? Cite a concrete, comparable outcome.
5. **Status:** What is complete, in progress, blocked, or not started?
6. **Next step and risk:** What remains, what could invalidate the conclusion,
   and what decision, if any, is required?

**One-sentence lead:** "We found [problem and impact], traced it to
[verified cause or current hypothesis], took [action], achieved [result],
and are now [status]; next we will [step or decision]."

This is a narrative order, not a requirement to create six headings or
repeat information. Combine sections when a shorter update is clearer.

## Reusable ChatGPT / Agent prompt

Copy and fill only the fields that matter:

```text
Act as the project owner giving a group-meeting update to a
non-technical leader. Explain the work in clear, plain language.

Topic: <project / task / issue IDs>
Audience: <manager / cross-functional team / executives>
Time budget: <30 seconds / 2 minutes / 5 minutes>
Decision needed: <none / a specific decision>

First inspect the current task, code, test evidence, and progress state
where access is available. Do not treat a closed ticket, a passing test,
or an old audit as proof of deployment or complete data correctness.

Organize the answer as:
1) the previous problem and its impact;
2) root cause, explicitly separating confirmed facts from inference;
3) actions taken and why;
4) verified results and their scope;
5) current completed / ongoing / blocked work;
6) next steps, remaining risks, and any decision needed.

Lead with the central takeaway. Explain *why it matters* before technical
implementation details. Replace jargon with everyday language or define it
in one short clause. Keep ticket numbers, paths, commands, and raw test
output in a small optional appendix.

Use at most 2-3 informative metrics in the spoken summary; provide
denominators or the tested scope where relevant. Do not invent numbers,
causes, dates, progress percentages, or delivery estimates. Say "not yet
verified" when evidence is missing. Distinguish code complete, local
tests passed, deployed, and production accepted.

Return:
A) a spoken update within the time budget;
B) current status in one sentence;
C) 2-3 likely management questions with concise answers, if useful.
```

## Output sizing

- **30 seconds:** One paragraph, 70–110 English words (or approximately
  150–230 Chinese characters), with the main result and next step.
- **2 minutes:** One compact spoken narrative, approximately 200–280 English
  words (or 350–550 Chinese characters); normally three problem/action/result
  groups plus status and risk.
- **5 minutes:** Expand the evidence and trade-offs, but put detail in an
  appendix rather than leading with implementation jargon.

These are editing targets, not automated gates.

## Evidence and wording guardrails

| Weak or misleading | Better |
| --- | --- |
| "All data is correct because 1,000 tests passed." | "1,000 local tests passed; full data-quality acceptance remains open." |
| "We fixed 8,000 data errors." (unknown files) | "8,000 files have unresolved provenance; they are not necessarily bad data." |
| "The root cause was legacy architecture." (not verified) | "The working hypothesis is inconsistent historical import conventions; the verified finding is [evidence]." |
| "The system is live." (only a PR merged) | "The code was merged; production deployment has not been verified." |

Use one familiar analogy only when it makes a difficult mechanism easier
to understand. Do not imply the analogy is literal evidence.

## Self-check before speaking

- Could someone unfamiliar with the repo repeat the problem in one sentence?
- Is the stated cause supported, or clearly qualified as a hypothesis?
- Are action and outcome different statements (work done vs effect proven)?
- Is every important "complete" tied to a scope and evidence?
- Is "not yet tested / not deployed / still blocked" visible?
- Is the next action specific enough to guide a decision?

If the reader asks for technical detail, offer a separate engineering
appendix with issue/PR links, evidence source, tests, and risks.
