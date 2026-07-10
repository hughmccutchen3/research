/* news-flag.js — BURSBUILD-S12
   One line to update per story: set NEWS_LATEST to the newest story's date.
   Any nav link carrying [data-news-flag] gets .is-fresh (red glow, styles.css)
   while the newest story is less than 7 days old. No build step, no fetch. */
(function () {
  var NEWS_LATEST = "2026-07-10"; /* date of the newest story on /news.html */
  var ageDays = (Date.now() - new Date(NEWS_LATEST + "T00:00:00-07:00").getTime()) / 86400000;
  if (ageDays < 0 || ageDays >= 7) return;
  var mark = function () {
    var links = document.querySelectorAll("[data-news-flag]");
    for (var i = 0; i < links.length; i++) links[i].classList.add("is-fresh");
  };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mark);
  } else {
    mark();
  }
})();
