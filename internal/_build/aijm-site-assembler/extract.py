#!/usr/bin/env python3
import re, os, json

SRC_DIR = os.path.expanduser("~/mnt/Work/Research/RSCH01 - AIML LLM Journalism and Medicine/OUTPUTS/build")

FILES = [
    ("01-introduction.html", 1),
    ("02-how-the-field-got-here.html", 2),
    ("03-how-these-systems-work.html", 3),
    ("04-predictive.html", 4),
    ("05-generative.html", 5),
    ("06-agentic.html", 6),
    ("07-conclusion.html", 7),
    ("08-technical-references.html", 8),
    ("09-appendix.html", 9),
]

sections = {}
for fname, num in FILES:
    path = os.path.join(SRC_DIR, fname)
    with open(path, encoding="utf-8") as f:
        html = f.read()
    m = re.search(r'<main id="main" class="doc">\n(.*?)\n</main>', html, re.S)
    assert m, f"main content not found in {fname}"
    body = m.group(1)
    # first <h1>...</h1> is the section's own title
    hm = re.search(r'<h1>(.*?)</h1>\n', body, re.S)
    assert hm, f"h1 not found in {fname}"
    title = hm.group(1)
    body_no_h1 = body[hm.end():]
    sections[num] = {"file": fname, "title": title, "body": body_no_h1}
    print(num, fname, "->", title, "(%d chars)" % len(body_no_h1))

with open(os.path.expanduser("~/scratch/3page/sections.json"), "w", encoding="utf-8") as f:
    json.dump(sections, f)
print("OK")
