---
name: course-examples
description: Guides the design, implementation, and verification of practical example chapters (topics 10-12 · Noob, Pro, IGL) across the AI Factory course series.
---

# Skill · Practical Example Chapters (10-12)

Use this skill whenever working on practical chapters: topic 10 (Noob), topic 11 (Pro), or topic 12 (IGL).

## 1. Golden Ratio and Scope

- **Number of scenarios:** strictly 6-7 scenarios per chapter (total 18-21 scenarios across topics 10-12).
- **Word floor:** strictly at least 1100 words per chapter (typical target: 1350-1550 words).
- **Difficulty progression:**
  - **Topic 10 (Noob):** Foundational everyday tasks, essential CLI syntax, removing magic, basic workflows.
  - **Topic 11 (Pro):** Real-world team pipelines, multi-job coordination, caching, artifact sharing, production deployment.
  - **Topic 12 (IGL):** Enterprise platform architecture, governance, OIDC security, ephemeral autoscaling, policy enforcement.

## 2. Top-Down Planning (The 3-Tier Scenario Matrix)

- **Phase 1 · Matrix Framing:** Before writing implementation code, agree with the Conductor on the high-level 3-tier scenario matrix (6-7 battle-tested scenarios per tier: Noob, Pro, IGL; total 18-21 scenarios). Formulate only concise 1-sentence problem statements for each scenario to verify whole-course coverage and eliminate duplication.
- **Phase 2 · Autonomous Sequential Delivery:** Deliver practical chapters in strictly 3 independent shifts (one chapter per shift: Topic 10, then 11, then 12). Full triad markup, configurations, and deep rationale are drafted directly into the target page `ru/<N>.html` under approved step tasks.

## 3. Mandatory Triad Format

Every scenario MUST be structured using the 3-part triad:
1. **Problem statement:** `<p><strong>Задача:</strong> Concise description of the production challenge and desired outcome.</p>`
2. **Implementation:** `<pre><code>Complete, working configuration or script without placeholders</code></pre>`
3. **Deep rationale:** `<div class="prints"><strong>Почему так:</strong> In-depth explanation of internal mechanics, failure modes, performance implications, and architectural decisions.</div>`

## 4. Viewport and Mobile Safety (390px)

- **Strictly forbidden:** multi-column `<table>` elements. They cause horizontal layout overflow on mobile screens (390px viewport).
- **Preferred alternatives:** definition lists, bulleted lists, and `<pre><code>` blocks with proper CSS wrapping.

## 5. Machine Claims Contract

- Every practical chapter MUST declare at least 3 machine-checkable statements in `tools/claims.tsv`.
- Each claim must be backed by a deterministic CLI command that executes and exits with code 0 in `./tools/check-claims.sh`.
- Run `./tools/check-claims.sh` to ensure all claims evaluate to `[ ДА ]`.

## 6. Landing Page Integration (index.html)

- The site landing page (`ru/index.html`) introduces the 18-21 practical scenarios under `<h3>Практические сценарии и банки вопросов (главы 10-15)</h3>`.
- Ensure that the descriptions for chapters 10, 11, and 12 on `index.html` accurately summarize the battle-tested scenarios delivered in those chapters and reflect the progression from Noob (basic hygiene) to Pro (team workflows) and IGL (platform architecture).

## 7. Delivery Workflow

1. Write `lessons/step-N.md` with strictly 3 predicates before editing any product files.
2. Draft the scenarios in `ru/<N>.html` adhering to the triad and word floor.
3. Add at least 3 executable claims to `tools/claims.tsv`.
4. Run `python3 tools/build-nav.py` and `python3 tools/build-search.py`.
5. Verify with `./check.sh` (must be completely `ЗЕЛЁНОЕ`, 9/9, 0 mobile defects).
6. Commit with scope `feat(content):` and detailed 1-2 paragraph explanatory commit body.
7. Record delivery in `lessons/record-N.md`.
