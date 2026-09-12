#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extract_md.py -- markdown-source counterpart to extract.py.

Per HANDOFF_AIJM-to-BURSBUILD_v1.4.md S3: AIJM now hands off raw markdown, not
build_paper.py's built HTML. Rather than re-derive the directive handling
(frontmatter strip, provenance cutoff, ANALYST-comment strip, diagram/panel
extraction including the new `practitioner` kind, definition-blockquote
styling), this script IMPORTS build_paper.py as a library and calls its own
convert() on each raw .md file directly -- convert() already does exactly
this pipeline and is the authoritative, already-proven implementation.

This means SECTIONS (the file list/order/labels) is never duplicated here --
it's read live off build_paper.SECTIONS, so a future file-list change in
build_paper.py is picked up automatically, per the build guide's own
"reuse, don't reinvent" principle and its warning against re-deriving cutoff
logic independently.

Output: sections.json, same shape produced by extract.py --
  {int section_number: {"file": <md filename>, "title": <str>, "body": <html>}}
so assemble.py needs zero changes to consume it.

Usage: python3 extract_md.py
"""
import io, os, re, sys, json

AIJM_DIR = os.path.expanduser(
    "~/mnt/Work/Research/RSCH01 - AIML LLM Journalism and Medicine/OUTPUTS"
)
OUT_JSON = os.path.expanduser("~/scratch/3page/sections.json")

sys.path.insert(0, AIJM_DIR)
# build_paper.py resolves its own HERE from __file__, and load_glossary_terms()
# reads the Appendix file by a path relative to that -- safe to import from
# anywhere since it uses os.path.dirname(os.path.abspath(__file__)), not cwd.
import build_paper as B


def strip_practitioner_eyebrow(html):
    """Task 3 (BURSBUILD-S27): strip the redundant eyebrow label specifically
    inside practitioner panels. build_paper.py's panel template (line 89)
    renders the same '<div class="panel__label">KIND</div>' eyebrow for all
    three panel kinds; Hugh wants it removed only for panel--practitioner,
    since the colored <h3> name heading + indent treatment already carries
    that signal. Scoped by the panel--practitioner wrapper so panel--view
    and panel--assistant eyebrows are untouched. Done here (BURSBUILD layer,
    post-processing build_paper.py's output) rather than editing
    build_paper.py itself, per the two-owner/two-layer principle: AIJM owns
    content/markdown, BURSBUILD owns presentation."""
    pattern = re.compile(
        r'(<aside class="panel panel--practitioner">\n)'
        r'<div class="panel__label">Practitioner</div>\n'
    )
    return pattern.sub(r"\1", html)


def convert_title_split(html):
    """Pull the leading <h1>...</h1> out as the section title, matching
    extract.py's existing contract against build_paper.py's built HTML
    (body_no_h1). B.convert() renders a leading '# Title' line to <h1>."""
    m = re.search(r"<h1>(.*?)</h1>\s*\n?", html, flags=re.S)
    if not m:
        return None, html
    title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return title, html[m.end():]


def main():
    sections = {}
    for i, (slug, fn, label) in enumerate(B.SECTIONS, 1):
        path = os.path.join(AIJM_DIR, fn)
        raw = io.open(path, encoding="utf-8").read()
        html = B.convert(raw)
        html = strip_practitioner_eyebrow(html)
        title, body = convert_title_split(html)
        if title is None:
            print("  WARNING: no <h1> found in %s, falling back to build_paper.py's SECTIONS label" % fn)
            title = label
        sections[i] = {"file": fn, "title": title, "body": body}
        print("%d %-28s -> %-40s (%d chars)" % (i, fn, title, len(body)))

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with io.open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(sections, f)
    print("OK ->", OUT_JSON)


if __name__ == "__main__":
    main()
