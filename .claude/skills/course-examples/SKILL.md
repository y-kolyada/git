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

## 2. Mandatory Triad Format

Every scenario MUST be structured using the 3-part triad:
1. **Problem statement:** `<p><strong>Задача:</strong> Concise description of the production challenge and desired outcome.</p>`
2. **Implementation:** `<pre><code>Complete, working configuration or script without placeholders</code></pre>`
3. **Deep rationale:** `<div class="prints"><strong>Почему так:</strong> In-depth explanation of internal mechanics, failure modes, performance implications, and architectural decisions.</div>`

## 3. Viewport and Mobile Safety (390px)

- **Strictly forbidden:** multi-column `<table>` elements. They cause horizontal layout overflow on mobile screens (390px viewport).
- **Preferred alternatives:** definition lists, bulleted lists, and `<pre><code>` blocks with proper CSS wrapping.

## 4. Machine Claims Contract

- Every practical chapter MUST declare at least 3 machine-checkable statements in `tools/claims.tsv`.
- Each claim must be backed by a deterministic CLI command that executes and exits with code 0 in `./tools/check-claims.sh`.
- Run `./tools/check-claims.sh` to ensure all claims evaluate to `[ ДА ]`.

## 5. Delivery Workflow

1. Write `lessons/step-N.md` with strictly 3 predicates before editing any product files.
2. Draft the scenarios in `ru/<N>.html` adhering to the triad and word floor.
3. Add at least 3 executable claims to `tools/claims.tsv`.
4. Run `python3 tools/build-nav.py` and `python3 tools/build-search.py`.
5. Verify with `./check.sh` (must be completely `ЗЕЛЁНОЕ`, 9/9, 0 mobile defects).
6. Commit with scope `feat(content):` and detailed 1-2 paragraph explanatory commit body.
7. Record delivery in `lessons/record-N.md`.
