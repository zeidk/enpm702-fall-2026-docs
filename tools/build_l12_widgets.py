#!/usr/bin/env python3
"""Build the L12 lecture page's "Try it" panels from the interactive slides.

Source: the interactive slides page as the docs serve it,
docs/source/_extra/lectures/lecture12/interactive/L12_interactive.html (the copy of the slides repo's
slides/lectures/lecture12/interactive/L12_interactive.html). Run this script from anywhere; paths come from its own place.

Writes:
  docs/source/_static/l12w/l12w.css       the slides' widget styles, scoped to .l12w, sized for the docs column
  docs/source/_static/l12w/l12w-core.js   the slides' helpers and frame scripts, without the slide navigation
  docs/source/lectures/lecture12/widgets/<name>.html   one panel per interactive slide, included by l12_lecture.rst
  docs/source/lectures/lecture12/widgets/_head.html, _scripts.html   loaded once, before the first and after the last panel
and, once, adds each panel's include (and a one-sentence lead-in) to l12_lecture.rst after the section it illustrates.
It only adds lines to the page: a panel already included is left alone, and no existing line changes.

Each panel is one slide's content (its controls, drawing and readouts), with the slide's numbers and words.
The slides stay the source: change a slide there, copy the page into _extra, then run this script again.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs/source/_extra/lectures/lecture12/interactive/L12_interactive.html"
STATIC = ROOT / "docs/source/_static/l12w"
WDIR = ROOT / "docs/source/lectures/lecture12/widgets"
PAGE = ROOT / "docs/source/lectures/lecture12/l12_lecture.rst"

# name; the ids that find the slide (an id inside it); the panel's title; the docs heading after whose text it goes;
# the sentence before it in the docs. Slides that belong together are joined (a key per slide).
WIDGETS = [
    # ---- section 1
    ("twist", ["tw-svg"], "Build a TwistStamped and see its path", "Command the ROSbot and Read Its Pose",
     "Move the two sliders to build a command and see the path the robot would drive for 3 s."),
    ("drive", ["dr-svg"], "Drive the ROSbot and watch the numbers", "Command the ROSbot and Read Its Pose",
     "Drag the knob on the pad to drive the robot, and watch its speeds, its wheels and its pose change."),
    ("world", ["pw-box"], "Turn the patrol world in 3D", "The Patrol World",
     "Drag to turn and tilt the world, right-drag (or Shift+drag) to pan, and scroll to zoom. The tags are the figure's."),
    ("launch-args", ["la-t"], "Build the launch command", "Launch Arguments",
     "Click a value in each row to build the launch command."),
    ("brake", ["cv-svg"], "Messages at 10 Hz, and the 0.5 s brake", "Drive Forward and Turn",
     "Press Start publishing, then press Ctrl+C, to see when the controller brakes."),
    ("sim-time", ["st-off"], "Run it with use_sim_time off, then on", "Run It: use_sim_time Off, Then On",
     "Switch use_sim_time between off and on to see the first lines the node printed."),
    ("pause", ["pz-svg"], "Pause Gazebo: which timer stops", "Pause Gazebo: Which Timer Stops",
     "Replay the measured run, or watch it again, to see which timer stops while Gazebo is paused."),
    # ---- section 2
    # "graph" (cg-svg) left out: the slide became a still drawing (user, 2026-11-22), and the page shows control_graph.png
    ("loop", ["lc-svg"], "The four steps of the loop", "What a Controller Does",
     "Click a step, or press Play, to see what each step adds to the picture."),
    ("error", ["tc-svg"], "The error of a turn", "The Error of a Turn",
     "Move the heading and the target to see the error the short way round."),
    ("yaw", ["qy"], "Yaw from a quaternion", "Yaw from the Odometry's Quaternion",
     "Move the yaw to see the quaternion that gives it, and the yaw the function returns."),
    ("law", ["pc-svg"], "The control law", "The Proportional Control Law",
     "Change the gain and the error to see the command the controller sends."),
    ("turn-log", ["rp-svg"], "The measured log of a turn", "Step 4: Build and Run in Gazebo",
     "Replay the log of the turn, or step through it one line at a time."),
    # ---- section 3
    ("why-params", ["q42-t"], "Numbers in the code, or parameters", "Why the Controller Needs Parameters",
     "Switch between numbers in the code and parameters, and step through the three reasons."),
    ("declare", ["q45-b"], "Declare a parameter: change a default", "Declare, Then Read",
     "Pick a default for line 39 to see which type the parameter gets."),
    ("param-list", ["q46-b0"], "ros2 param list and get", "Command-Line Tools: list and get",
     "Pick a command to see what it prints for the running node."),
    ("set-no-effect", ["q47-log"], "Set a value the node already read", "Setting a Value the Node Already Read",
     "Step through the measured log to see that the set changes the stored value only."),
    ("at-start", ["q49-b0"], "Set a parameter at start", "On the Command Line, at Start",
     "Pick the value of kp_angular to see what the node reads."),
    ("yaml", ["q50-b"], "A parameter file", "From a YAML File",
     "Pick a node to see which values it gets from the file."),
    ("use-sim-time", ["q51-b0"], "use_sim_time, with and without the file", "use_sim_time for a Node That Runs with Gazebo",
     "Pick how the node was started to see its use_sim_time value."),
    ("launch-yaml", ["q52-b0"], "A launch file and its parameter file", "From a Launch File: a YAML File Named by an Argument",
     "Pick how the launch file was started to see which parameter file the node gets."),
    ("gains", ["q54-svg"], "Three gains, three runs", "Three Gains, Three Separate Runs",
     "Pick a run to read the time of each of its 90 degree turns."),
    ("validator", ["q57-svg"], "The callback: try a value", "The Callback, Part 1: Refuse a Bad Value",
     "Pick a parameter and a value to see what the callback answers."),
    ("store", ["q58-in"], "The callback: follow one value", "The Callback, Part 2: Store the New Values",
     "Pick a parameter and a value to follow it through the callback."),
    ("gain-change", ["q59-svg"], "Change a gain while the ROSbot turns", "Change a Gain While the ROSbot Turns",
     "Replay the measured run to see the command change when the gain changes."),
    # section 4 (namespaces and remapping) left the deck for the Namespaces and Remapping reading (2026-11-23); its four
    # panels are frozen copies in reading_material/remapping/widgets/
]

SVG_TAGS = {"svg", "g", "path", "text", "tspan", "line", "rect", "circle", "ellipse", "polyline", "polygon", "use", "defs",
            "marker", "clipPath", "linearGradient", "stop", "pattern", "mask", "symbol", "image", "foreignObject"}

# the content width of a slide frame (1248 px less 2 x 40 px of padding): one slide px is 1/1168 of a panel's width
CONTENT = 1168


def die(msg):
    sys.exit("build_l12_widgets: " + msg)


def px_to_u(value, font=False):
    """Frame px to the docs column: N px becomes calc(N * var(--u)); fonts keep a floor; 1 to 5 px stay (borders)."""
    def one(m):
        n = float(m.group(1))
        return m.group(0) if n < 6 else f"calc({m.group(1)} * var(--u))"
    if font:
        m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)px\s*(!important)?\s*", value)
        if m:
            return f"max(var(--fmin), calc({m.group(1)} * var(--u))){(' ' + m.group(2)) if m.group(2) else ''}"
    return re.sub(r"(?<![\w.#-])(\d+(?:\.\d+)?)px", one, value)


def scale_decls(decls):
    out = []
    for d in decls.split(";"):
        if ":" not in d:
            out.append(d)
            continue
        k, v = d.split(":", 1)
        prop = k.strip().lower()
        if prop.startswith("--") or prop in ("border", "border-top", "border-bottom", "border-left", "border-right",
                                             "outline", "outline-offset", "box-shadow", "text-shadow", "stroke-width"):
            out.append(d)
        else:
            out.append(k + ":" + px_to_u(v, font=(prop == "font-size")))
    return ";".join(out)


# ---------------------------------------------------------------- CSS
DROP = re.compile(r"^(html|body|\*$|#viewport|#world|#title|#nav|#where|#corner|#hotspot|#help|#ink|#laser|#modebadge|#ph-|"
                  r"#deck|#band|#bibpop|\.secblock|\.sechead|\.card|\.opener|\.toc|\.lo\b|\.stack|\.pipe|svg\.pipe|\.handoff|"
                  r"\.hcard|\.harrow|\.av-|\.grid$|\.fitin|\.tyre-|\.clockrow|\.refs|\.cite|\.ph-|\.rb-|#nx-list|\.key\b|\.sr\b)")


def map_selector(sel):
    sel = sel.strip()
    if not sel:
        return None
    if sel.startswith("#whypop"):
        return None
    dark = False
    m = re.match(r':root\[data-theme="dark"\]\s*(.*)$', sel)
    if m:
        dark, sel = True, m.group(1)
    if sel in (":root", ""):
        return 'html[data-theme="dark"] .l12w' if dark else ".l12w"
    if sel == "*":
        return ".l12w, .l12w *"
    # the slide box itself and its chrome
    if re.match(r"^(\.plate|\.frame)(\.\w+|:[\w()-.]+|::\w+)*$", sel) or re.match(r"^\.plate( \.bolt|::|\.plan|:not)", sel) \
            or re.match(r"^\.frame( > \.fit| \.fhead| h2|:not\(\.titlepage\)|\.titlepage)", sel) or sel.startswith(("body.", ".plate .bolt")):
        return None
    sel = re.sub(r"^(\.plate|\.frame)\s+", "", sel)
    if DROP.match(sel):
        return None
    return ('html[data-theme="dark"] .l12w ' if dark else ".l12w ") + sel


def split_selectors(prelude):
    """Split a selector list at the commas outside parentheses (:is(a,b) stays whole)."""
    out, depth, cur = [], 0, ""
    for ch in prelude:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    return out + [cur]


def parse_rules(css):
    """Top-level rules as (prelude, body); @media and @supports bodies are parsed again by the caller."""
    i, n, out = 0, len(css), []
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        prelude = css[i:j].strip()
        depth, k = 1, j + 1
        while depth and k < n:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        out.append((prelude, css[j + 1:k - 1]))
        i = k
    return out


def scope_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = []
    for prelude, body in parse_rules(css):
        if prelude.startswith("@font-face"):
            continue
        if prelude.startswith("@keyframes"):
            out.append(f"{prelude}{{{body}}}")
            continue
        if prelude.startswith("@media"):
            inner = scope_css(body)
            if inner.strip():
                out.append(f"{prelude}{{\n{inner}\n}}")
            continue
        sels = [s for s in (map_selector(p) for p in split_selectors(prelude)) if s]
        if sels:
            out.append(",".join(sels) + "{" + scale_decls(body) + "}")
    return "\n".join(out)


FONTS = [("Sans", "Light", 300, "normal"), ("Sans", "Regular", 400, "normal"), ("Sans", "Italic", 400, "italic"),
         ("Sans", "SemiBold", 600, "normal"), ("Sans", "SemiBoldItalic", 600, "italic"), ("Sans", "Bold", 700, "normal"),
         ("Sans", "BoldItalic", 700, "italic"), ("Mono", "Regular", 400, "normal"), ("Mono", "Bold", 700, "normal")]
# the slides' own fonts (SIL OFL, in the slides' asset folder), under their own family names so the rest of the page
# keeps its fonts; the path is from _static/l12w/ to the slides' copy that the docs serve
FONT_FACES = "".join(
    f'@font-face{{font-family:"L12W Fira {fam}";font-style:{st};font-weight:{w};font-display:swap;'
    f'src:url("../../lectures/lecture12/interactive/L12_interactive_assets/fonts/Fira{fam}-{n}.woff2") format("woff2")}}\n'
    for fam, n, w, st in FONTS)


DOCS_CSS = r"""/* Generated by tools/build_l12_widgets.py from the L12 interactive slides: do not edit by hand.
   Each .l12w panel is one slide's content. Sizes are the slides' frame px times --u, so a panel keeps the slide's
   proportions in the docs column; text never goes under --fmin. Nothing here styles the rest of the page. */
.l12w{display:block;margin:1.1em 0 1.6em;padding:12px 14px 14px;border:1px solid var(--plate-edge);border-radius:10px;
  background:var(--plate);color:var(--ink);font-family:"Fira Sans","Segoe UI",system-ui,sans-serif;line-height:1.35}
/* the docs theme loads Bootstrap: its .row (negative margins, every child 100% wide) must not reach the slides' .row */
.l12w .row{margin-left:0;margin-right:0;--bs-gutter-x:0;--bs-gutter-y:0}
.l12w .row > *{width:auto;max-width:none;margin-top:0;flex-shrink:0}
.l12w .l12w-title{font-weight:700;color:var(--slate);margin:0 0 6px;font-size:1.02em}
.l12w .l12w-title .l12w-kick{display:inline-block;font-size:.78em;font-weight:700;color:var(--on-accent);background:var(--live);
  border-radius:5px;padding:1px 7px;margin-right:8px;vertical-align:1px}
/* position:relative: the math's hidden screen-reader copy (position:absolute) stays inside the panel's own scroll box */
.l12w .l12w-in{container-type:inline-size;--fmin:13px;overflow-x:auto;position:relative}
.l12w .rng .rv{font-size:max(11px, calc(20 * var(--u)))}
/* --u: one slide frame px in this column (1168 px of slide content); on a phone it stops at 0.42 px, so controls stay
   usable and a wide panel scrolls inside itself instead of the page */
.l12w .l12w-in > *{--u:max(calc(100cqw / 1168), 0.42px);font-size:max(var(--fmin), calc(27 * var(--u)))}
/* the page's inline-code colors do not belong in a panel */
.l12w code,.l12w .code{font-family:"L12W Fira Mono","Fira Mono",monospace}
.l12w .l12w-in svg.plot,.l12w .l12w-in img,.l12w .l12w-in video{max-width:100%;height:auto}
.l12w table{width:100%}
.l12w ul,.l12w ol{margin-top:.2em;margin-bottom:.2em}
.l12w p{margin:.3em 0}
.l12w pre{margin:0}
@container (max-width: 620px){
  .l12w .two{display:block !important}
  .l12w .two > *{margin-bottom:8px}
  .l12w .row{flex-wrap:wrap}
}
"""


# ---------------------------------------------------------------- panels
def find_section(s, key):
    for m in re.finditer(r'<section class="plate frame[^"]*"[^>]*>.*?</section>', s, re.S):
        body = m.group(0)
        if f'id="{key}"' in body:
            return body
    die(f"no slide holds {key!r}")


def section_parts(sec):
    h = re.search(r"<h2>(.*?)</h2>", sec, re.S)
    body = sec[h.end():] if h else sec
    body = re.sub(r"</section>\s*$", "", body.strip())
    body = re.sub(r'^\s*<div class="fit"><div class="fitin">', "", body)
    body = re.sub(r"</div></div>\s*$", "", body.strip())
    body = re.sub(r'<p class="docs">.*?</p>', "", body, flags=re.S)          # "more detail in the docs": these are the docs
    cls = re.match(r'<section class="plate frame([^"]*)"', sec).group(1).split()
    cls = [c for c in cls if c not in ("plan", "follow", "extra", "s1", "s2", "s3", "s4", "s5", "s6")]
    return body.strip(), cls


def deck_words(text):
    """On a docs page the slides' own name for themselves reads wrong: "The deck's example" becomes "The lecture's
    example". Only these phrases: the code's "deck" ids stay."""
    for old, new in (("the deck shows", "the lecture uses"), ("The deck's", "The lecture's"), ("the deck's", "the lecture's")):
        text = text.replace(old, new)
    return text


def fix_markup(html_):
    html_ = re.sub(r"<style>(.*?)</style>", lambda m: "<style>" + scope_css(m.group(1)) + "</style>", html_, flags=re.S)
    html_ = re.sub(r'((?:src|poster|data-dark|data-light)=")(L12_interactive_(?:assets|media)/)', r"\1interactive/\2", html_)

    def style(m):
        return f'style="{scale_decls(m.group(1))}"'
    html_ = re.sub(r'style="([^"]*)"', style, html_)

    def sized(m):                                      # svg, img and video with a width attribute: keep the slide's share
        tag, attrs = m.group(1), m.group(2)
        w = re.search(r'\swidth="(\d+(?:\.\d+)?)"', attrs)
        if not w:
            return m.group(0)
        add = (f"width:calc({w.group(1)} * var(--u));max-width:100%;height:auto" if tag != "svg" else
               f"width:max(calc({w.group(1)} * var(--u)), calc({w.group(1)} * 12px / 20.5));max-width:none;height:auto")
        if 'style="' in attrs:
            attrs = attrs.replace('style="', f'style="{add};', 1)
        else:
            attrs += f' style="{add}"'
        return f"<{tag}{attrs}>"
    return re.sub(r"<(svg|img|video)(\s[^>]*)>", sized, html_)


# ---------------------------------------------------------------- script
def between(text, a, b):
    i = text.find(a)
    j = text.find(b, i + 1)
    if i < 0 or j < 0:
        die(f"marker not found: {a!r} or {b!r}")
    return text[i:j]


def build_js(main, page):
    head = []
    for pat in (r'var reduce = [^\n]*;', r'var C = \{.*?\};'):
        m = re.search(pat, main, re.S)
        if not m:
            die("not found in the slides' script: " + pat)
        head.append(m.group(0))
    m = re.search(r'NS = "[^"]+", FONT = "[^"]+"', main)
    head.append("var " + m.group(0).replace('FONT = "Fira Sans', 'FONT = "L12W Fira Sans, Fira Sans') + ";")

    helpers = between(main, "/* ---------- small helpers", 'mathIn(document.getElementById("deck"));')
    helpers = helpers.replace('var w = r.clientWidth || parseFloat(r.getAttribute("width")) || vb.width;',
                              'var inn = r.closest && r.closest(".l12w-in"), w = r.clientWidth && inn && inn.clientWidth ? r.clientWidth / Math.max(inn.clientWidth / %d, 12 / TXT_MIN) '
                              ': parseFloat(r.getAttribute("width")) || vb.width;   /* in the slide\'s own frame px (%d px of content); a frame px is never under '
                              '12 / 20.5 screen px, as the drawings\' own width (labels at least 12 px on a phone) */' % (CONTENT, CONTENT))
    if "the slide's own frame px" not in helpers:
        die("svgScale changed in the slides: update build_l12_widgets.py")

    codeboxes = between(main, "/* ---------- code boxes: color, number", "/* ---------- section 1:")
    codeboxes = codeboxes.replace('document.querySelectorAll("pre.code")', 'document.querySelectorAll(".l12w pre.code")')
    if ".l12w pre.code" not in codeboxes:
        die("code box block changed in the slides: update build_l12_widgets.py")
    frames = between(main, "/* ---------- section 1:", "/* ---------- sliders:")
    frames = frames.replace('function active(svg){ var fr = svg.closest(".plate"); return !!(fr && fr.classList.contains("active")); }',
                            'function active(svg){ return !!svg._vis; }   /* the panel is on screen */')
    if "svg._vis" not in frames:
        die("the slides' active() changed: update build_l12_widgets.py")
    # a plot that the slides draw once on show (reveal) also gets a "Draw again" button here (the TwistStamped panel has the
    # slides' own "Drive again" since 2026-11-20)
    for a, b in (('/* tags: a tag goes beside its mark', 'window.L12W_reveal = reveal;\n  /* tags: a tag goes beside its mark'),):
        if a not in frames:
            die("the slides' script changed: update build_l12_widgets.py: " + a[:50])
        frames = frames.replace(a, b, 1)
    # the 3D patrol world: the slides draw it while slide 9 is the active slide; here, while the panel is on screen
    a = 'var fr = box.closest(".plate"); if (!fr || !fr.classList.contains("active")){ running = false; return; }'
    if a not in frames:
        die("the slides' 3D world loop changed: update build_l12_widgets.py")
    frames = frames.replace(a, 'if (!box.__on){ running = false; return; }', 1)
    a = '    onShow(box, function(){ size(); draw(); if (!running){ running = true; requestAnimationFrame(loop); } });'
    if a not in frames:
        die("the slides' 3D world start changed: update build_l12_widgets.py")
    frames = frames.replace(a, a + '\n    if (window.IntersectionObserver) new IntersectionObserver(function(es){ box.__on = es[0].isIntersecting;'
                            '\n      if (box.__on){ size(); draw(); if (!running){ running = true; requestAnimationFrame(loop); } } }).observe(box);', 1)
    frames += """
document.querySelectorAll(".l12w [data-again]").forEach(function(b){ b.addEventListener("click", function(){ var svg = $id(b.dataset.again); if (window.L12W_reveal) L12W_reveal(svg, 1200); }); });
"""
    # the slide dims the lesson's last box until the last step; on the docs page it stays readable
    frames = frames.replace('$("q42-c").style.opacity = step === 4 ? 1 : 0.35;', '$("q42-c").style.opacity = 1;')
    sliders = between(main, "/* ---------- sliders:", "/* ---------- the cover")
    sliders = sliders.replace("document.querySelectorAll('input[type=\"range\"]')", "document.querySelectorAll('.l12w input[type=\"range\"]')")
    # the slider's value label: the deck's thumb is 78 px, here it scales with the column, so measure it, and move the
    # label and the ticks again when the column changes width
    old = ('function place(){ var W = inp.offsetWidth || parseFloat(getComputedStyle(inp).width) || 320, k = (+inp.value - lo) / (hi - lo);\n'
           '    rv.style.left = (k * (W - TW)) + "px"; rv.textContent = rangeText(inp); }')
    if old not in sliders:
        die("the slider label code changed in the slides: update build_l12_widgets.py")
    sliders = sliders.replace(old, 'function place(){ TW = rv.offsetWidth || TW; var W = inp.offsetWidth || parseFloat(getComputedStyle(inp).width) || 320, '
                              'k = (+inp.value - lo) / (hi - lo);\n    rv.style.left = (k * (W - TW)) + "px"; rv.textContent = rangeText(inp);\n'
                              '    w.querySelectorAll(".tk").forEach(function(t){ t.style.left = (TW / 2 + (+t.title - lo) / (hi - lo) * (W - TW)) + "px"; }); }\n'
                              '  if (window.ResizeObserver) new ResizeObserver(function(){ place(); }).observe(inp);')
    live = main[main.find("/* ---------- live values"):]
    live = live[:live.find("})();") + len("})();")]
    live = live.replace('.closest(".plate, .card")', '.closest(".l12w")')
    if '.closest(".l12w")' not in live:
        die("live values block changed in the slides: update build_l12_widgets.py")

    tags = {}
    for m2 in re.finditer(r"<([a-zA-Z]+)\b[^>]*\sid=\"([\w-]+)\"", page):
        tags.setdefault(m2.group(2), m2.group(1))
    import json
    body = "\n".join(head) + f"""
var TAGS = {json.dumps(tags, separators=(",", ":"))}, SVGT = {json.dumps({t: 1 for t in SVG_TAGS}, separators=(",", ":"))};
/* an element a script asks for: the page's, or a detached one when its panel is not on this page */
/* one stand-in per id, so a script that fills an element and reads it again finds what it put there; the stand-ins sit in
   a holder that is not in the page, so code that inserts next to one works and document.contains() still says "not here"
   (a page with only some panels, such as the setup page's 3D world) */
var STANDIN = {{}}, HOLDER = document.createElement("div");
function $id(id){{ var e = document.getElementById(id); if (e) return e; if (STANDIN[id]) return STANDIN[id]; var t = TAGS[id] || "div";
  e = SVGT[t] ? document.createElementNS(NS, t) : document.createElement(t); e.id = id; STANDIN[id] = e; HOLDER.appendChild(e); return e; }}
{helpers}
document.querySelectorAll(".l12w").forEach(function(w){{ mathIn(w); }});
/* The ticks: values the lecture itself uses for each slider; a frame script adds TICKS["slider-id"] = [...]. */
var TICKS = {{}};
/* onShow(el, fn): fn(first) runs each time el comes on screen (a third of it in view); first is true the first time
   only. A panel's drawing starts there (a line drawn gradually once, then a "Draw again" button). The slides call it
   when the frame holding el comes on screen. */
var SHOWN = [], showIO = window.IntersectionObserver ? new IntersectionObserver(function(es){{
  es.forEach(function(en){{ var e = en.target; e._vis = en.isIntersecting; if (!en.isIntersecting) return;
    SHOWN.forEach(function(s){{ if (s.el !== e) return; var first = !s.seen; s.seen = true;
      try {{ s.fn(first); }} catch (err) {{ if (window.console) console.error(err); }} }}); }}); }}, {{threshold:0.3}}) : null;
function onShow(e, fn){{ if (typeof e === "string") e = $id(e); if (!e || !document.contains(e)) return;
  SHOWN.push({{el:e, fn:fn, seen:false}});
  if (showIO) showIO.observe(e); else {{ e._vis = true; fn(true); }} }}
/* onReset(el, fn): the slides put a frame back when the viewer leaves it; a docs panel stays as the reader left it,
   so the panels register nothing (the frame scripts call it, so it must exist) */
function onReset(){{}}
/* whyOpen(b): a "?" button on a slide opens the deck's explanation window with b._why ({{t: title, b: html}}); the docs page
   has no such window, so the explanation shows in a box under the panel's log, and the next "?" replaces it */
function whyOpen(b){{ var pre = b.closest("pre") || b, box = pre.parentNode.querySelector(".l12w-why");
  if (!box){{ box = document.createElement("div"); box.className = "box l12w-why"; box.setAttribute("aria-live", "polite"); pre.parentNode.insertBefore(box, pre.nextSibling); }}
  box.innerHTML = "<b>" + b._why.t + "</b>" + b._why.b; mathIn(box); }}
{codeboxes}
{frames}
{sliders}
{live}
/* the helpers, for the panels' own extras */
window.L12W = {{el:el, txt:txt, tag:tag, tagR:tagR, halo:halo, poly:poly, frame:frame, f:f, nt:nt, tex:tex, mathIn:mathIn,
  svgScale:svgScale, C:C, NS:NS, reduce:reduce, onShow:onShow}};
"""
    body = deck_words(body)
    body = body.replace("document.getElementById(", "$id(")
    body = body.replace("function $id(id){ var e = $id(id);", "function $id(id){ var e = document.getElementById(id);")
    return ("/* Generated by tools/build_l12_widgets.py from the L12 interactive slides: do not edit by hand. */\n"
            "(function(){\n\"use strict\";\nif (!document.querySelector(\".l12w\")) return;\n" + body + "\n})();\n")


# ---------------------------------------------------------------- the page
def heading_spans(lines):
    """(index of the title line, title) for every section title of the page."""
    out = []
    for i in range(1, len(lines)):
        if re.fullmatch(r'([=\-^"~])\1{3,}', lines[i]) and lines[i - 1].strip() and not re.fullmatch(r'([=\-^"~])\1{3,}', lines[i - 1]):
            out.append((i - 1, lines[i - 1].strip()))
    return out


def insert_panels(panel_names):
    """Add each panel's include to the page, at the end of the section it illustrates (before the next title and its
    label). Only adds lines. A panel that is already included stays where it is."""
    text = PAGE.read_text()
    lines = text.split("\n")
    marks = heading_spans(lines)
    adds = {}          # line index to insert before -> list of text blocks
    first_seen = "widgets/_head.html" in text
    todo = [w for w in WIDGETS if w[0] in panel_names and f"widgets/{w[0]}.html" not in text]
    for name, keys, title, after, lead in todo:
        k = [j for j, (_, t) in enumerate(marks) if t == after]
        if len(k) != 1:
            die(f"the page has {len(k)} titles {after!r}")
        j = k[0]
        end = marks[j + 1][0] if j + 1 < len(marks) else len(lines)
        # the next title may sit under an overline or a label: back up over blank lines, labels and overlines
        while end > 0 and (not lines[end - 1].strip() or lines[end - 1].startswith(".. _") or re.fullmatch(r'([=\-^"~])\1{3,}', lines[end - 1])):
            end -= 1
        block = []
        if not first_seen:
            block += [".. raw:: html", "   :file: widgets/_head.html", ""]
            first_seen = True
        block += [lead, "", ".. raw:: html", f"   :file: widgets/{name}.html", ""]
        adds.setdefault(end, []).append(block)
    out = []
    for i, line in enumerate(lines):
        if i in adds:
            if out and out[-1].strip():
                out.append("")
            for b in adds[i]:
                out += b
        out.append(line)
    new = "\n".join(out)
    if "widgets/_scripts.html" not in new:
        new = new.rstrip("\n") + "\n\n.. raw:: html\n   :file: widgets/_scripts.html\n"
    if new != text:
        PAGE.write_text(new)
    return len(todo)


def main():
    if not SRC.exists():
        die(f"{SRC} not found")
    page = SRC.read_text()
    scripts = re.findall(r"<script>(.*?)</script>", page, re.S)
    main_js = max(scripts, key=len)
    STATIC.mkdir(parents=True, exist_ok=True)
    WDIR.mkdir(parents=True, exist_ok=True)
    style = "\n".join(re.findall(r"<style>(.*?)</style>", page, re.S))
    css = scope_css(style)
    css = re.sub(r'"?Fira (Sans|Mono)"?(?=\s*[,;}])', lambda m: f'"L12W Fira {m.group(1)}", "Fira {m.group(1)}"', css)
    (STATIC / "l12w.css").write_text(FONT_FACES + DOCS_CSS.replace('font-family:"Fira Sans"', 'font-family:"L12W Fira Sans","Fira Sans"') + css + TAIL)
    core = build_js(main_js, page)
    # (The rule builder's preset labels were patched here until its slides left the deck, 2026-11-23: the reading's frozen
    # copy, _static/remapw/remapw-core.js, keeps them.)
    (STATIC / "l12w-core.js").write_text(core)

    (WDIR / "_head.html").write_text(
        "<!-- Generated by tools/build_l12_widgets.py: the panels' styles and the math styles, loaded once. -->\n"
        '<link rel="stylesheet" href="interactive/katex/katex.min.css">\n'
        '<link rel="stylesheet" href="../../_static/l12w/l12w.css">\n')
    (WDIR / "_scripts.html").write_text(
        "<!-- Generated by tools/build_l12_widgets.py: math and panel code, after every panel. -->\n"
        '<script src="interactive/katex/katex.min.js"></script>\n'
        '<script src="interactive/katex/contrib/auto-render.min.js"></script>\n'
        # the 3D patrol world: three.js r128 (MIT) from the slides' copy, and the world's shapes from patrol.sdf
        '<script src="interactive/L12_interactive_assets/three/three.min.js"></script>\n'
        '<script src="interactive/L12_interactive_assets/three/OrbitControls.js"></script>\n'
        '<script>var PATROL = ' + (SRC.parent / "L12_interactive_assets/patrol_world.json").read_text().strip() + ';</script>\n'
        '<script src="../../_static/l12w/l12w-core.js"></script>\n')
    used = set()
    for name, keys, title, after, lead in WIDGETS:
        secs = []
        for k in keys:
            sec = find_section(page, k)
            if sec not in secs:
                secs.append(sec)
        parts = [section_parts(sec) for sec in secs]
        body = "\n".join(p[0] for p in parts)
        cls = " ".join(sorted({c for p in parts for c in p[1]}))
        html_ = (f'<!-- Generated by tools/build_l12_widgets.py from the interactive slide with {", ".join(keys)}. -->\n'
                 f'<div class="l12w mathjax_ignore tex2jax_ignore" data-w="{name}">\n'
                 f'<div class="l12w-title"><span class="l12w-kick">Try it</span>{title}</div>\n'
                 f'<div class="l12w-in{(" " + cls) if cls else ""}">\n{fix_markup(body)}\n</div>\n</div>\n')
        if name in AGAIN:
            html_ = html_.replace("\n</div>\n</div>\n", f'\n<div class="row" style="margin:6px 0 0"><button type="button" data-again="{AGAIN[name]}">Draw again</button></div>\n</div>\n</div>\n')
        html_ = deck_words(html_)
        for w_name, old, new in WORDING:
            # "slide N" in a pattern matches any slide number: the deck numbers its frames when it is built
            pat = re.escape(old).replace(re.escape("slide N"), r"slide \d+")
            if w_name == name and re.search(pat, html_):
                html_ = re.sub(pat, lambda m: new, html_)
                used.add((w_name, old))
        (WDIR / f"{name}.html").write_text(html_)
    missing = [w for w in WORDING if (w[0], w[1]) not in used]
    if missing:
        die("slide wording not found (the slides changed?): " + "; ".join(f"{a}: {b}" for a, b, _ in missing))
    # The setup page shows the same 3D patrol world (user, 2026-11-21: "Use the dynamic world (the one used in slide 23)
    # instead of" the figure in setup/rosbot_simulation.rst, The Environment). One file with the styles, the panel and the
    # scripts, its paths moved from lectures/lecture12/ to setup/.
    setup_w = ROOT / "docs/source/setup/widgets"
    setup_w.mkdir(parents=True, exist_ok=True)
    one = "".join((WDIR / f).read_text() for f in ("_head.html", "world.html", "_scripts.html"))
    one = one.replace('="interactive/', '="../lectures/lecture12/interactive/').replace('="../../_static/', '="../_static/')
    if '="interactive/' in one or '="../../_static/' in one:
        die("a path of the world panel was not moved for the setup page")
    (setup_w / "patrol_world.html").write_text("<!-- Generated by tools/build_l12_widgets.py for setup/rosbot_simulation.rst: do not edit by hand. -->\n" + one)
    n = insert_panels({w[0] for w in WIDGETS})
    print(f"wrote {len(WIDGETS)} panels, l12w.css, l12w-core.js; added {n} includes to the lecture page")


# slide wording that reads wrong on a docs page: (panel, slide text, docs text); each must be found
# panels whose plot is drawn gradually but has no button of its own in the slides: the plot's id
AGAIN = {"error": "tc-svg", "law": "pc-svg"}

WORDING = [
    ("launch-args", ", the same form as <code>with_dispatcher:=false</code> last class. All optional;", ". All optional;"),
    ("use-sim-time", '(<span class="go" data-go="p30">slide N</span>)', "(see Simulation Time above)"),
]

# light theme only: two of the slides' text colors pass 4.5:1 as the slides' large text, not at the docs' body size
TAIL = """
/* a drawing wider than a phone's column scrolls sideways in its own box: its labels stay at least 12 px */
.l12w .l12w-in{overflow-x:auto}
/* docs body size: the light theme's orange and green text a little darker, to reach 4.5:1 on the panel */
.l12w{--follow:#A3561F;--ok:#2A7348}
/* the panel title carries the Try it badge, so the slide's own badge is not repeated */
.l12w .l12w-in .try{display:none}
.l12w code,html[data-theme="dark"] .l12w code{color:var(--ink)}
/* a row of picker buttons wraps inside its own box instead of running out of the panel */
.l12w .l12w-in span:has(> button){display:inline-flex;flex-wrap:wrap;gap:6px;max-width:100%}
/* a code box beside its controls: at the docs column's width the controls go under the code */
@container (max-width: 900px){
  .l12w .two[style*="max-content"]{display:block !important}
  .l12w .two[style*="max-content"] > *{margin-bottom:8px}
}
/* the slider in fixed sizes: at the docs column's scale the slide's thumb offsets and the value's box no longer agree */
.l12w .rng,.l12w .rng input[type=range]{height:34px}
.l12w .rng input[type=range]::-webkit-slider-runnable-track{height:6px}
.l12w .rng input[type=range]::-webkit-slider-thumb{width:58px;height:26px;border-radius:13px;margin-top:-10px}
.l12w .rng input[type=range]::-moz-range-thumb{width:54px;height:22px;border-radius:13px}
.l12w .rng .rv{width:58px;height:26px;top:4px;font:600 13px/26px var(--sans)}
.l12w .rng .tk{height:6px}
"""

if __name__ == "__main__":
    main()
