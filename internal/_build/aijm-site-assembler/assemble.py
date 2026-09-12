#!/usr/bin/env python3
import json, re, os, hashlib

SCRATCH = os.path.expanduser("~/scratch/3page")
with open(os.path.join(SCRATCH, "sections.json"), encoding="utf-8") as f:
    sections = {int(k): v for k, v in json.load(f).items()}

SHORT_LABEL = {
    1: "Introduction", 2: "How the field got here", 3: "How these systems work",
    4: "Predictive", 5: "Generative", 6: "Agentic",
    7: "Conclusion", 8: "Technical references", 9: "Appendix",
}

PARTS = [
    {"n": 1, "file": "part-1.html", "title": "Foundations", "secs": [1, 2, 3],
     "tagline": "What AI is, how the field got here, and how these systems actually work"},
    {"n": 2, "file": "part-2.html", "title": "Predictive, Generative, Agentic", "secs": [4, 5, 6],
     "tagline": "The three modes, case by case, from the published record"},
    {"n": 3, "file": "part-3.html", "title": "Conclusion & Reference", "secs": [7, 8, 9],
     "tagline": "What the record adds up to, the technical vocabulary, and the open questions"},
]

PROVENANCE_BLOCK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "provenance_block_generated.html")
with open(PROVENANCE_BLOCK_PATH, encoding="utf-8") as f:
    PROVENANCE_BLOCK_HTML = f.read()

with open(os.path.join(SCRATCH, "aijm_css.txt"), encoding="utf-8") as f:
    AIJM_CSS = f.read()

SITE_CSS = """
/* --- BURSBUILD-S25 v3.0: site-adaptation chrome over the AIJM multi-page build --- */
.site-header{
  font-family:'DM Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:#FFFFFF; border-bottom:1px solid #E2E8F0;
  display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between;
  gap:12px 20px; padding:12px 24px;
}
.site-header .wordmark{ font-weight:700; font-size:1.125rem; letter-spacing:-.01em; color:#0F172A; text-decoration:none; white-space:nowrap; }
.site-header .wordmark span{ color:#8B6914; }
.site-header .site-nav{ display:flex; flex-wrap:wrap; gap:16px; font-size:14px; list-style:none; margin:0; padding:0; }
.site-header .site-nav a{ display:inline-block; min-height:44px; line-height:44px; color:#475569; text-decoration:none; border-bottom:2px solid transparent; transition:color .15s,border-color .15s; }
.site-header .site-nav a:hover{ color:#8B6914; border-bottom-color:#C9A33D; }
@media (min-width:720px){ .site-header{ padding:12px 48px; } }

/* v3.0: series-cap folded INTO the sticky topbar (was a second, separate dark band
   above the sticky one -- Hugh's call: collapse the two black bands into one combined
   band that stays visible with the current part's section nav while scrolling). */
.topbar__series{ display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:0 10px; }
.series-cap-label{ text-transform:uppercase; letter-spacing:2px; color:#94A3B8; }
.series-cap-sep{ color:#475569; user-select:none; }
.series-cap-item{ color:#CBD5E1; text-decoration:none; }
.series-cap-item:hover{ color:#F1F5F9; }
.series-cap-item--active{ color:#F1F5F9; font-weight:700; }
@media (max-width:640px){ .topbar__series{ justify-content:flex-start; font-size:10px; } }

.draft-marker{
  background:var(--gold-pale); border-bottom:2px solid var(--gold); color:var(--ink);
  font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:1px; text-transform:uppercase;
  text-align:center; padding:9px 16px;
}
.draft-marker a{ color:var(--ink); text-decoration:underline; }

.site-coverband{ background:var(--blue); color:#fff; text-align:center; }
.site-coverband__img{ width:100%; max-height:340px; object-fit:cover; object-position:top; display:block; }
.site-coverband__img--p1{ object-position:top; }
.site-coverband__img--p2{ object-position:center 65%; }
.site-coverband__img--p3{ object-position:bottom; }
.site-coverband__body{ padding:32px 24px 40px; max-width:var(--col-w); margin:0 auto; }
.site-coverband h1{ font-family:'DM Sans','Gill Sans',Trebuchet,sans-serif; font-size:clamp(26px,4.2vw,40px); font-weight:700; line-height:1.15; margin-bottom:10px; }
.site-coverband__partnum{ font-family:'JetBrains Mono',monospace; font-size:12px; letter-spacing:3px; text-transform:uppercase; color:var(--gold); margin-bottom:10px; }
.site-coverband__tagline{ font-size:15.5px; color:rgba(168,200,216,.9); font-style:italic; margin-bottom:8px; }
.site-coverband__meta{ font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--caliche); letter-spacing:1px; margin-top:14px; }

/* v3.0: strong visual break between the 3 sections concatenated within one part --
   Hugh's call: this is more content per page than the site has handled before, and the
   old plain <hr/> join between sections did not read as a real break while scrolling. */
.section-divider{
  width:100vw; margin-left:calc(50% - 50vw); margin-right:calc(50% - 50vw);
  background:var(--ink); color:#fff; margin-top:64px; margin-bottom:0;
  padding:22px 24px; display:flex; flex-wrap:wrap; align-items:baseline; justify-content:center;
  gap:4px 16px; font-family:'JetBrains Mono',monospace; border-top:2px solid var(--gold); border-bottom:2px solid var(--gold);
}
.section-divider__num{ text-transform:uppercase; letter-spacing:3px; font-size:11px; color:var(--gold-pale); opacity:.9; white-space:nowrap; }
.section-divider__title{ font-family:'DM Sans','Gill Sans',Trebuchet,sans-serif; font-weight:700; font-size:19px; color:#fff; }
.section-heading{ font-family:'DM Sans','Gill Sans',Trebuchet,sans-serif; font-size:15px; font-weight:600;
  text-transform:uppercase; letter-spacing:1px; color:var(--caliche); margin:20px 0 18px; }
.section-heading--first{ font-size:21px; text-transform:none; letter-spacing:normal; color:var(--blue); margin:0 0 20px; font-weight:600; }
@media print{
  .section-divider{ background:none; color:var(--ink); width:auto; margin-left:0; margin-right:0; }
  .section-divider__num{ color:var(--caliche); }
  .section-divider__title{ color:var(--ink); }
}

/* v3.0: quick "back to top" control -- more content per page than before makes this worth having */
.back-to-top{
  position:fixed; right:20px; bottom:24px; z-index:60; width:44px; height:44px; border-radius:50%;
  background:var(--ink); color:#fff; border:2px solid var(--gold); text-decoration:none;
  display:flex; align-items:center; justify-content:center; font-size:19px; line-height:1;
  box-shadow:0 6px 18px -6px rgba(0,0,0,.45); opacity:0; pointer-events:none; transform:translateY(8px);
  transition:opacity .2s ease, transform .2s ease;
}
.back-to-top.is-visible{ opacity:1; pointer-events:auto; transform:translateY(0); }
.back-to-top:hover{ background:#1c2531; }
@media print{ .back-to-top{ display:none; } }

.provenance{ background:#f0efec; border-top:3px solid var(--caliche); padding:40px 24px; max-width:var(--col-w); margin:48px auto 0; }
.provenance h2{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:4px; text-transform:uppercase; color:var(--caliche); margin-bottom:20px; }
.prov-row{ display:grid; grid-template-columns:160px 1fr; gap:12px; padding:10px 0; border-bottom:1px solid var(--gray-rule); font-size:13px; }
.prov-row:last-child{ border-bottom:none; }
.prov-label{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:1px; text-transform:uppercase; color:var(--caliche); padding-top:2px; }
.prov-value{ color:#444; line-height:1.6; }
@media (max-width:640px){ .prov-row{ grid-template-columns:1fr; } }
/* BURSBUILD-S27: compatibility for provenance_render.py's generated dl/dt/dd markup
   (the block is generated from the record, not hand-typeset -- keep its markup as-is
   and adapt the CSS, rather than rewriting generator output to match old div markup). */
.prov-grid{ margin:0; }
.prov-grid .prov-row dt{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:1px;
  text-transform:uppercase; color:var(--caliche); margin:0; padding-top:2px; }
.prov-grid .prov-row dd{ margin:0; color:#444; line-height:1.6; }
.prov-closing{ font-size:13px; color:var(--caliche); margin-top:16px; }

@media print{
  .site-header,.draft-marker{ display:none; }
  /* BURSBUILD-S27 print-blocker fix: without forcing color-adjust, browsers strip
     background colors by default in print, leaving thead th and .site-coverband's
     white text on a transparent (effectively white) background -- unreadable. */
  html,body{ -webkit-print-color-adjust:exact; print-color-adjust:exact; color-adjust:exact; }
  thead th{ background:var(--blue) !important; color:#fff !important; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .site-coverband{ background:var(--blue) !important; color:#fff !important; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .site-coverband__img{ display:none; }
}
"""

def demote_h1(body, sec_num):
    # kept for compatibility; superseded by build_section_block below
    return '<h2 id="s%d">%s</h2>\n' % (sec_num, sections[sec_num]["title"]) + body

def build_section_block(sec_num, order_in_part, part_size):
    title = sections[sec_num]["title"]
    body = sections[sec_num]["body"]
    if order_in_part == 1:
        heading = '<h2 id="s%d" class="section-heading section-heading--first">%s</h2>\n' % (sec_num, title)
        return heading + body
    divider = ('<div class="section-divider" id="s%d">\n'
               '<span class="section-divider__num">Section %d of %d</span>\n'
               '<span class="section-divider__title">%s</span>\n'
               '</div>\n') % (sec_num, order_in_part, part_size, title)
    heading = '<h2 class="section-heading">%s</h2>\n' % title
    return divider + heading + body

def build_series_links(current_n):
    parts_markup = []
    for p in PARTS:
        if p["n"] == current_n:
            parts_markup.append('<span class="series-cap-item series-cap-item--active">%d &mdash; %s</span>' % (p["n"], p["title"]))
        else:
            parts_markup.append('<a class="series-cap-item" href="%s">%d &mdash; %s</a>' % (p["file"], p["n"], p["title"]))
    return ('<span class="series-cap-label">How Bloomberg Used AI</span>'
            '<span class="series-cap-sep">&middot;</span>'
            + '<span class="series-cap-sep">&middot;</span>'.join(parts_markup))

def build_stickyhead(part):
    # v1.2: every chip is a real anchor with data-sec, including the first (scroll-spy
    # needs a consistent, addressable target set -- see SCROLLSPY_JS). The first chip
    # starts visually current for the pre-scroll/no-JS state; JS takes over from there.
    chips = []
    for i, sn in enumerate(part["secs"]):
        label = SHORT_LABEL[sn]
        current = ' chip--current' if i == 0 else ''
        aria = ' aria-current="page"' if i == 0 else ''
        chips.append('<a class="chip%s" href="#s%d" data-sec="s%d"%s><b>%02d</b>%s</a>' % (current, sn, sn, aria, sn, label))
    chips_html = "\n  ".join(chips)
    return '''<div class="stickyhead">
<div class="topbar">
<a class="topbar__brand" href="/">Bursera <span>Consulting</span></a>
<div class="topbar__series">%s</div>
<span class="topbar__draft">Public draft &middot; not yet deployed</span>
</div>
<nav class="series" aria-label="Sections in this part">
  <div class="series__label">Part %d &mdash; %s</div>
  <div class="series__chips">
  %s
  </div>
</nav>
</div>''' % (build_series_links(part["n"]), part["n"], part["title"], chips_html)

def build_pagefoot(current_n):
    prev_p = next((p for p in PARTS if p["n"] == current_n - 1), None)
    next_p = next((p for p in PARTS if p["n"] == current_n + 1), None)
    prev_html = ('<a class="pager pager--prev" href="%s">&#8592; Part %d: %s</a>' % (prev_p["file"], prev_p["n"], prev_p["title"])) if prev_p else '<a class="pager pager--prev" href="/internal/public-drafts/">&#8592; All public drafts</a>'
    next_html = ('<a class="pager pager--next" href="%s">Part %d: %s &#8594;</a>' % (next_p["file"], next_p["n"], next_p["title"])) if next_p else '<span></span>'
    return '<footer class="pagefoot">%s\n%s</footer>' % (prev_html, next_html)

LIGHTBOX_JS = '''<script>
(function(){
  function ready(fn){document.readyState!='loading'?fn():document.addEventListener('DOMContentLoaded',fn);}
  ready(function(){
    var figures = document.querySelectorAll('.figure');
    if(!figures.length) return;
    var lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.innerHTML = '<span class="lightbox__close" aria-label="Close">&#215;</span><div class="lightbox__inner"></div>';
    document.body.appendChild(lb);
    var inner = lb.querySelector('.lightbox__inner');
    function openLb(media){
      inner.innerHTML = '';
      var clone = media.cloneNode(true);
      clone.removeAttribute('loading');
      if(clone.tagName && clone.tagName.toLowerCase() === 'svg'){
        clone.removeAttribute('width');
        clone.removeAttribute('height');
      }
      inner.appendChild(clone);
      lb.classList.add('is-open');
    }
    function closeLb(){ lb.classList.remove('is-open'); inner.innerHTML = ''; }
    figures.forEach(function(f){
      var media = f.querySelector('img,svg');
      if(!media) return;
      var hint = document.createElement('span');
      hint.className = 'figure__expand';
      hint.textContent = 'Expand \\u2921';
      f.appendChild(hint);
      f.addEventListener('click', function(e){
        if(e.target.closest('a')) return;
        openLb(media);
      });
    });
    lb.addEventListener('click', closeLb);
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeLb(); });
  });
})();
</script>'''

BACKTOTOP_HTML = '<a href="#main" class="back-to-top" id="backToTop" aria-label="Back to top">&#8593;</a>'

BACKTOTOP_JS = '''<script>
(function(){
  function ready(fn){document.readyState!='loading'?fn():document.addEventListener('DOMContentLoaded',fn);}
  ready(function(){
    var btn = document.getElementById('backToTop');
    if(!btn) return;
    function onScroll(){
      if(window.scrollY > 480){ btn.classList.add('is-visible'); }
      else{ btn.classList.remove('is-visible'); }
    }
    window.addEventListener('scroll', onScroll, {passive:true});
    onScroll();
    btn.addEventListener('click', function(e){
      e.preventDefault();
      window.scrollTo({top:0, behavior:'smooth'});
    });
  });
})();
</script>'''

SCROLLSPY_JS = '''<script>
(function(){
  function ready(fn){document.readyState!='loading'?fn():document.addEventListener('DOMContentLoaded',fn);}
  ready(function(){
    var chips = Array.prototype.slice.call(document.querySelectorAll('.series__chips .chip'));
    if(!chips.length || !('IntersectionObserver' in window)) return;
    var targets = chips.map(function(c){
      var id = c.getAttribute('data-sec');
      return {chip:c, id:id, el: id ? document.getElementById(id) : null};
    }).filter(function(t){ return t.el; });
    if(!targets.length) return;
    function setCurrent(id){
      chips.forEach(function(c){
        if(c.getAttribute('data-sec') === id){ c.classList.add('chip--current'); c.setAttribute('aria-current','page'); }
        else { c.classList.remove('chip--current'); c.removeAttribute('aria-current'); }
      });
    }
    var io = new IntersectionObserver(function(entries){
      var visible = entries.filter(function(e){ return e.isIntersecting; });
      if(visible.length){
        visible.sort(function(a,b){ return a.boundingClientRect.top - b.boundingClientRect.top; });
        setCurrent(visible[0].target.id);
      }
    }, {rootMargin: '-25% 0px -65% 0px', threshold: 0});
    targets.forEach(function(t){ io.observe(t.el); });
    window.addEventListener('scroll', function(){
      if((window.innerHeight + window.scrollY) >= document.body.scrollHeight - 4){
        setCurrent(targets[targets.length - 1].id);
      }
    }, {passive:true});
  });
})();
</script>'''

def provenance_block():
    return '''<div class="provenance" id="provenance">
<h2>Provenance</h2>
<div class="prov-row"><span class="prov-label">Owner</span><span class="prov-value">Hugh McCutchen</span></div>
<div class="prov-row"><span class="prov-label">Contributors</span><span class="prov-value">Claude Sonnet 5 (site adaptation, BURSBUILD-S25) &middot; Claude Opus 5 (AIJM authorship) &middot; Hugh McCutchen (editor, ruling)</span></div>
<div class="prov-row"><span class="prov-label">How it began</span><span class="prov-value">Built directly from AIJM's own nine-file multi-page source (01-introduction.html through 09-appendix.html), grouped into three parts. Cover art from AIJM-PAPER-HEADER-IMAGE.</span></div>
<div class="prov-row"><span class="prov-label">Type of writing</span><span class="prov-value">Inquiry Record &mdash; straight reportage carrying Bursera's own marked view (the "Voice of Bursera" panels within the body).</span></div>
<div class="prov-row"><span class="prov-label">Process</span><span class="prov-value">Execution</span></div>
<div class="prov-row"><span class="prov-label">Tools</span><span class="prov-value">output-formatting &middot; bursera-site-deploy &middot; provenance &middot; bursera-webmaster</span></div>
<div class="prov-row"><span class="prov-label">Why this version</span><span class="prov-value">v2.0: Hugh's direction &mdash; split the single one-page draft into three separately releasable parts (Data Lifecycle series model), each with its own sticky in-page reading nav (AIJM's own stickyhead/chip pattern) and a series-cap linking all three parts. Reverted the v1.1 key-term link/glossary-panel treatment: AIJM-S18's own provenance record shows Hugh already reviewed and killed that exact glossary-linking feature (the cross-file hrefs broke in the one-page build) in favor of terms defined in place at first mention &mdash; carrying that reintroduced forward would have overridden a ruling already made. v3.0: Hugh's review of the live 3-page build &mdash; folded the series-cap band into the sticky topbar (one combined band stays visible on scroll instead of two separate dark bands), added a strong full-bleed divider band between the sections concatenated within each part, and added a back-to-top control (this is more content per page than the site had previously carried). v3.1 (BURSBUILD-S27): three refinements from Hugh's review of the v3.0 preview &mdash; the header cover image now crops from the top (object-position:top) rather than centering, which was cutting into the headline text; the redundant eyebrow label on practitioner panels was removed, since the colored name heading already carries that signal; and the vocab-term linking question was re-raised and explicitly reaffirmed as skipped for now &mdash; the v1.1 ruling above stands, no code change.</span></div>
<div class="prov-row"><span class="prov-label">Notes</span><span class="prov-value">The closing "Bursera's Take" panel for the Conclusion section has not been written yet. Published anyway, visibly marked as a draft &mdash; incomplete is honest here, concealing it would not be.</span></div>
<div class="prov-row"><span class="prov-label">Sources</span><span class="prov-value">Inherited from AIJM's own research; not separately tracked at this site-adaptation layer.</span></div>
<div class="prov-row"><span class="prov-label">Depth &amp; confidence</span><span class="prov-value">Deep &middot; unchanged</span></div>
<div class="prov-row"><span class="prov-label">Level of work</span><span class="prov-value">Substantial</span></div>
<div class="prov-row"><span class="prov-label">Record</span><span class="prov-value">Full history and audit trail available on request.</span></div>
</div>'''

def build_part(part):
    n = part["n"]
    part_size = len(part["secs"])
    body_parts = []
    for i, sn in enumerate(part["secs"]):
        body_parts.append(build_section_block(sn, i + 1, part_size))
    main_html = "\n".join(body_parts)
    if n == 3:
        # Document-level provenance: one consolidated, generated block at the end of
        # the full paper (Part 3), never repeated per-page -- per the standing lock and
        # Hugh's direction at BURSBUILD-S27.
        main_html += "\n" + PROVENANCE_BLOCK_HTML

    head = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s &mdash; How Bloomberg Used AI, Part %d of 3 &mdash; Bursera Consulting</title>
<meta name="description" content="Part %d of 3: %s. A decade of Bloomberg's predictive, generative and agentic AI systems, traced case by case from the published record. Public draft.">
<meta name="robots" content="noindex">
<link rel="canonical" href="https://burseraconsulting.com/internal/public-drafts/how-bloomberg-used-ai/%s">
<link rel="icon" href="https://burseraconsulting.com/favicon.svg" type="image/svg+xml">
<link rel="icon" href="https://burseraconsulting.com/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="https://burseraconsulting.com/apple-touch-icon.png">
<meta property="og:type" content="article">
<meta property="og:title" content="%s &mdash; How Bloomberg Used AI, Part %d of 3">
<meta property="og:description" content="Part %d of 3: %s. A decade of Bloomberg's predictive, generative and agentic AI systems, traced from the published record.">
<meta property="og:url" content="https://burseraconsulting.com/internal/public-drafts/how-bloomberg-used-ai/%s">
<meta property="og:image" content="https://burseraconsulting.com/internal/public-drafts/how-bloomberg-used-ai/og-bloomberg-ai.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Predictive, Generative, Agentic &mdash; a word-cloud cover over a blue and violet particle field.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,600;0,700;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,300;1,8..60,400&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>%s
%s
</style></head>''' % (part["title"], n, n, part["title"], part["file"], part["title"], n, n, part["title"], part["file"], AIJM_CSS, SITE_CSS)

    body = '''<body class="news-story">
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <a class="wordmark" href="/">Bursera <span>Consulting</span></a>
  <nav class="site-nav" aria-label="Primary">
    <a href="/">Home</a>
    <a href="/research_examples.html">Research</a>
    <a href="/llm-leadership.html">Training</a>
    <a href="/advisory.html">Advisory</a>
    <a href="/about.html">About</a>
    <a href="/news.html">Updates</a>
  </nav>
</header>
%s
<div class="site-coverband">
  <img class="site-coverband__img site-coverband__img--p%d" src="ai-history-bloomberg-header.jpg" width="1376" height="768" alt="Predictive, Generative, Agentic &mdash; a word-cloud cover over a blue and violet particle field.">
  <div class="site-coverband__body">
    <div class="site-coverband__partnum">Part %d of 3</div>
    <h1>%s</h1>
    <p class="site-coverband__tagline">%s</p>
    <p class="site-coverband__meta">Hugh McCutchen &middot; Bursera Consulting &middot; September 2026 &middot; Public Draft</p>
  </div>
</div>
<main id="main" class="doc">
%s
</main>
%s
%s
%s
%s
%s
</body>
</html>''' % (
        build_stickyhead(part),
        n,
        n, part["title"], part["tagline"],
        main_html,
        build_pagefoot(n),
        LIGHTBOX_JS,
        BACKTOTOP_HTML,
        BACKTOTOP_JS,
        SCROLLSPY_JS,
    )

    return head + "\n" + body

for part in PARTS:
    html = build_part(part)
    out_path = os.path.join(SCRATCH, part["file"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(part["file"], len(html), "chars")
print("DONE")
