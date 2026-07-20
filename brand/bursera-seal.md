# The Bursera Provenance Seal — reference

**Status:** standard component (BURSBUILD-S16, 2026-07-19). Style-guide entry: SITE_DESIGN_PRINCIPLES.md §2.
**What it is:** the B mark + stacked "Human / Led" link placed in the top-right of every published
piece's cover. Links to the piece's own rendered provenance block (`id="provenance"`). Hover shows
"Full Provenance Below". A one-time ~3s gold glow runs on page open (CSS only; respects
prefers-reduced-motion). Implements the provenance-link half of the Being-Bursera Charter §5.3 seal;
the /verify/<id> link is added when RES-449 builds.

## Canonical assets
- Mark: `favicon.svg` (repo root) · live at https://burseraconsulting.com/favicon.svg
- Styles: `.bseal*` rules + `@keyframes bglow` in `styles.css` (section 14) · live at https://burseraconsulting.com/styles.css
- Colors: navy #0F172A · gold #C9A33D · light-cover text #8b6a3b (Regime A brass/slate family)

## Markup (copy verbatim)
Host container needs `bseal-host` class (or `position:relative`). Use `bseal--light` on light/parchment covers.

```html
<a class="bseal" href="#provenance" aria-label="Full provenance below"><svg class="bmark" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true"><rect width="100" height="100" rx="18" fill="#0F172A" stroke="#C9A33D" stroke-width="4"/><text x="50" y="72" text-anchor="middle" font-family="Georgia,serif" font-weight="600" font-size="66" fill="#C9A33D">B</text></svg><span class="btext"><span>Human</span><span>Led</span></span><span class="btip">Full Provenance Below</span></a>
```

The target document must contain a rendered provenance block carrying `id="provenance"`.

## Using it from another project
- On any page that links the site stylesheet: `<link rel="stylesheet" href="https://burseraconsulting.com/styles.css">` + the markup above.
- Standalone (no stylesheet): copy the `.bseal` CSS block from styles.css section 14 into the page's own styles.
- From a Cowork session: read `C:\github\research\brand\bursera-seal.md` (this file) and `C:\github\research\styles.css`.
