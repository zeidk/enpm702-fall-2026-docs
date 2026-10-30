/*
 * vcat-hover.js: on a page that holds the definitions of make_obstacle, lookup and
 * first_pose (the code block with class vcat-defs, from
 * reading_material/value_categories/vcat_definitions.inc), each use of one of these
 * names, in the text or in a code block, shows that function's definition in a box
 * when the mouse is over it. A tap shows it too (phones have no hover), and so does
 * keyboard focus. Escape, a second tap or a tap elsewhere hides it.
 *
 * The definitions are read from the page, so the code exists in one place only.
 * Other pages have no vcat-defs block, and the script does nothing there.
 */
(function () {
  "use strict";

  var NAMES = ["make_obstacle", "lookup", "first_pose"];
  var NAME_RE = /\b(make_obstacle|lookup|first_pose)\b/g;
  // Pygments token classes whose text is not code that calls the function.
  var SKIP_TOKENS = ["c", "c1", "cm", "cp", "cpf", "s", "s1", "s2", "sb", "sc", "sd"];

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  // One entry per function: the highlighted lines of its definition, comment included.
  function readDefinitions(block) {
    var pre = block.querySelector("pre");
    if (!pre) return {};
    var copy = pre.cloneNode(true);
    copy.querySelectorAll(".linenos").forEach(function (n) { n.remove(); });
    var lines = copy.innerHTML.split("\n");
    var chunks = [[]];
    lines.forEach(function (line) {
      var text = line.replace(/<[^>]*>/g, "").trim();
      if (text === "") {
        if (chunks[chunks.length - 1].length) chunks.push([]);
      } else {
        chunks[chunks.length - 1].push(line);
      }
    });
    var defs = {};
    chunks.forEach(function (chunk) {
      var text = chunk.join("\n").replace(/<[^>]*>/g, "");
      NAMES.forEach(function (name) {
        if (!defs[name] && new RegExp("\\b" + name + "\\s*\\(").test(text) &&
            new RegExp("\\b" + name + "\\s*\\([^)]*\\)\\s*\\{").test(text)) {
          defs[name] = chunk.join("\n").replace(/^(\s*<span><\/span>)+/, "");
        }
      });
    });
    return defs;
  }

  function skipped(node, block) {
    for (var el = node.parentElement; el; el = el.parentElement) {
      if (el === block) return true;
      var tag = el.tagName;
      if (tag === "A" || tag === "SUMMARY" || /^H[1-6]$/.test(tag)) return true;
      if (el.classList && SKIP_TOKENS.some(function (c) { return el.classList.contains(c); }))
        return true;
      if (el.classList && el.classList.contains("vcat-fn")) return true;
    }
    return false;
  }

  // Wrap each use of a name, inside inline code and code blocks, in a span.vcat-fn.
  function markUses(root, block, defs) {
    var scopes = root.querySelectorAll("code.literal, div.highlight pre");
    var targets = [];
    scopes.forEach(function (scope) {
      var walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT);
      var node;
      while ((node = walker.nextNode())) {
        NAME_RE.lastIndex = 0;
        if (NAME_RE.test(node.nodeValue) && !skipped(node, block)) targets.push(node);
      }
    });
    targets.forEach(function (node) {
      var text = node.nodeValue;
      var frag = document.createDocumentFragment();
      var last = 0;
      NAME_RE.lastIndex = 0;
      var m;
      while ((m = NAME_RE.exec(text))) {
        if (!defs[m[1]]) continue;
        frag.appendChild(document.createTextNode(text.slice(last, m.index)));
        var span = document.createElement("span");
        span.className = "vcat-fn";
        span.textContent = m[1];
        span.dataset.fn = m[1];
        span.tabIndex = 0;
        frag.appendChild(span);
        last = m.index + m[1].length;
      }
      frag.appendChild(document.createTextNode(text.slice(last)));
      node.parentNode.replaceChild(frag, node);
    });
  }

  ready(function () {
    var block = document.querySelector(".vcat-defs");
    if (!block) return;
    var defs = readDefinitions(block);
    if (!Object.keys(defs).length) return;
    var root = document.querySelector("main") || document.body;
    markUses(root, block, defs);

    var tip = document.createElement("div");
    tip.className = "vcat-tip";
    tip.id = "vcat-tip";
    tip.setAttribute("role", "tooltip");
    tip.hidden = true;
    document.body.appendChild(tip);
    var current = null;

    function show(span) {
      tip.innerHTML = '<div class="highlight"><pre>' + defs[span.dataset.fn] + "</pre></div>";
      tip.hidden = false;
      current = span;
      span.setAttribute("aria-describedby", "vcat-tip");
      var r = span.getBoundingClientRect();
      var w = tip.offsetWidth, h = tip.offsetHeight, gap = 6;
      var left = Math.min(Math.max(8, r.left), window.innerWidth - w - 8);
      var top = r.bottom + gap;
      if (top + h > window.innerHeight && r.top - gap - h > 0) top = r.top - gap - h;
      tip.style.left = left + window.scrollX + "px";
      tip.style.top = top + window.scrollY + "px";
    }

    function hide() {
      if (current) current.removeAttribute("aria-describedby");
      tip.hidden = true;
      current = null;
    }

    document.addEventListener("mouseover", function (e) {
      var span = e.target.closest && e.target.closest(".vcat-fn");
      if (span && span !== current) show(span);
    });
    document.addEventListener("mouseout", function (e) {
      var span = e.target.closest && e.target.closest(".vcat-fn");
      if (span && span === current && !span.contains(e.relatedTarget)) hide();
    });
    document.addEventListener("focusin", function (e) {
      if (e.target.classList && e.target.classList.contains("vcat-fn")) show(e.target);
    });
    document.addEventListener("focusout", function (e) {
      if (e.target === current) hide();
    });
    document.addEventListener("click", function (e) {
      var span = e.target.closest && e.target.closest(".vcat-fn");
      if (span) {
        if (span === current && !tip.hidden) hide(); else show(span);
      } else if (!tip.contains(e.target)) {
        hide();
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") hide();
    });
    window.addEventListener("scroll", function () { if (current) show(current); }, { passive: true });
  });
})();
