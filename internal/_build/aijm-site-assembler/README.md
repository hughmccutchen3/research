# AIJM site assembler — extract → assemble

Promoted from device scratch (`~/scratch/3page/`) into the repo on 2026-09-11, at the point
BURSBUILD-S26 confirmed this pattern's second real use (the next AIJM paper). Governing doc:
`BurseraConsulting/BURSBUILD-AIJM-SITE-BUILD-GUIDE_v1.2_2026-09-11.md` on the Work tree — read
that first; this README does not restate it.

## What's here

- `extract.py` — reads AIJM's built HTML files (`<main>` body + first `<h1>`), writes `sections.json`.
  **HTML-only.** The next paper hands off raw markdown, not HTML — this script does not yet read
  markdown. See the build guide's "Next build" section for what `extract_md.py` needs to handle
  (frontmatter, provenance cutoff, ANALYST-comment strip, diagram directives, panel extraction
  incl. the new `practitioner` kind, definition-blockquote styling) and exactly which
  `build_paper.py` functions to port rather than re-derive.
- `assemble.py` — reads `sections.json` + `aijm_css.txt`, builds the site's part pages. Needs no
  changes to consume a new paper, IF `sections.json` comes out the same shape — but `PARTS` and
  `SHORT_LABEL` at the top of the file are hand-written per paper (currently hard-coded to the
  Bloomberg paper's own 9 sections / 3-parts-of-3 grouping) and must be rewritten for each new
  paper's actual section count and titles. Do not assume 3-parts-of-3 for a future paper without
  asking — see the build guide.
- `aijm_css.txt` — AIJM's shared stylesheet, extracted verbatim from `build_paper.py`'s `CSS`
  variable. Untouched by the site build; `assemble.py`'s own `SITE_CSS` is the site-adaptation layer.

## Not yet here

`extract_md.py` (markdown-reading extractor) does not exist yet — it's the next paper's Task 1/3,
per the AIJM→BURSBUILD handoff v1.3 and the S25→S26 handoff. Once written, it belongs beside
these two scripts in this same directory.
