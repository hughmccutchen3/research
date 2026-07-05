/* Bursera section-nav (RES-313) — auto-builds an in-page section nav from
   <h2 id> headings. Opt in with <nav class="article-nav" data-section-nav></nav>.
   Label = data-nav-label if present, else heading text with a leading "N." stripped.
   No dependencies. */
(function () {
  var mount = document.querySelector('nav[data-section-nav]');
  if (!mount) return;
  var heads = [].slice.call(document.querySelectorAll('h2[id]'));
  if (!heads.length) return;
  var OFFSET = 46; // sticky bar height + breathing room
  var links = heads.map(function (h) {
    var label = h.getAttribute('data-nav-label');
    if (!label) label = h.textContent.replace(/^\s*\d+\.\s*/, '').trim();
    h.style.scrollMarginTop = OFFSET + 'px';
    var a = document.createElement('a');
    a.className = 'nav-link';
    a.href = '#' + h.id;
    a.textContent = label;
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var top = h.getBoundingClientRect().top + window.pageYOffset - OFFSET;
      window.scrollTo({ top: top, behavior: 'smooth' });
      history.replaceState(null, '', '#' + h.id);
    });
    mount.appendChild(a);
    return a;
  });
  var map = {};
  heads.forEach(function (h, i) { map[h.id] = links[i]; });
  function setActive(id) {
    var l = map[id];
    if (!l) return;
    links.forEach(function (x) { x.classList.remove('is-active'); });
    l.classList.add('is-active');
    // keep the active label visible on the horizontal bar (nav scroll only)
    mount.scrollLeft = l.offsetLeft - mount.clientWidth / 2 + l.clientWidth / 2;
  }
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) setActive(en.target.id); });
  }, { rootMargin: '-46px 0px -70% 0px', threshold: 0 });
  heads.forEach(function (h) { obs.observe(h); });
  setActive(heads[0].id);
})();
