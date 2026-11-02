#!/usr/bin/env python3
"""Memory figures of the reading page virtual Methods in Depth (l9_virtual.rst).

    python3 virtual_memory.svg.py                  # SVGs only, next to this file
    python3 virtual_memory.svg.py --png            # SVGs and 300 dpi PNGs in ../ (images/l9)
    python3 virtual_memory.svg.py --png vtable_memory   # one figure

vtable_memory: robotaxi and taxi on the stack, each with its hidden pointer to its class's
vtable, and each vtable entry pointing to the code of the class's own method.

slicing_virtual_memory: Vehicle copy{taxi}; with a virtual drive: the copy gets the values of
the Vehicle part and its own hidden pointer, to Vehicle's vtable.

Measured on 2026-11-02 (g++ 13.3, -std=c++20), on the small classes of the L9 slides (Vehicle
with two doubles and a virtual drive):
  - g++ -fdump-lang-class: the vtables of Vehicle, RoboTaxi and Taxi have 5 entries each:
    offset 0, the type information, the destructor twice, then drive, each pointing to the
    class's own version. The figure draws one destructor entry and the drive entry.
  - sizeof Vehicle 24, Taxi 56; the hidden pointer at offset 0, max_speed_ at 8, speed_ at 16,
    driver_name_ at 24 in a Taxi; values 13.4, 0 and "Ana".
  - gdb "info vtbl": taxi's pointer is on Taxi's vtable, copy's on Vehicle's.
The derived classes' own members (RoboTaxi's in vtable_memory) are drawn as one dashed row,
without a size, since the slides leave them out.

The style and the helpers are the slides' L7 ones (lecture7/figures/svg/av_shared_ptr_states.svg.py
in the slides repo, enpm702-fall-2026-beamer), imported, not copied, as the slides' own
inheritance_memory.svg.py does. The slides repo must sit at ../../latex/ beside this docs repo.
"""
import importlib.util
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 6))      # the docs repo
L7 = os.path.join(REPO, "..", "..", "latex", "enpm702-fall-2026-beamer", "slides", "lectures",
                  "lecture7", "figures", "svg", "av_shared_ptr_states.svg.py")
spec = importlib.util.spec_from_file_location("l7", L7)
l7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(l7)

PNGDIR = os.path.dirname(HERE)
ROW, CAP = l7.ROW, l7.CAP
SLATE, SLATE_BODY, SLATE_FIELD = "#4a4f57", "#eef0f3", "#fafbfc"   # vtables and code: not stack


def rows(x, y, w, items, title, fill=l7.FIELD, line=l7.BLUE, dash_last=False):
    """A part: its caption above, then one row per (name, value). Returns the parts and the bottom."""
    o = [l7.txt(x + w / 2, y + CAP - 14, title, l7.SMALL, l7.INK, l7.FS, "bold")]
    ry0 = y + CAP
    o.append(l7.rrect(x, ry0, w, ROW * len(items), 10, fill, line, 3))
    for k, (m, v) in enumerate(items):
        ry = ry0 + k * ROW
        if k:
            o.append(f'<line x1="{x}" y1="{ry}" x2="{x + w}" y2="{ry}" stroke="{line}" stroke-width="2"/>')
        color = l7.GRAY if (dash_last and k == len(items) - 1) else l7.INK
        o.append(l7.txt(x + 18, ry + ROW / 2 + 12, m, l7.SMALL - 2, color, l7.FM, "bold", "start"))
        if v:
            o.append(l7.txt(x + w - 18, ry + ROW / 2 + 12, v, l7.SMALL - 2, l7.DIM, l7.FM, "normal", "end"))
    return o, ry0 + ROW * len(items)


def region(x, y, w, h, label):
    """A slate box with a header band and a word: the vtables, or the code."""
    return [l7.rrect(x, y, w, h, 14, SLATE_BODY, SLATE, 4),
            l7.header_band(x, y, w, l7.HEAD, 14, SLATE),
            l7.txt(x + w / 2, y + l7.HEAD / 2 + 0.36 * l7.TITLE, label, l7.TITLE, "#ffffff", l7.FS, "bold")]


def vtable_memory():
    l7.ARROWS.clear()
    l7.LABELS.clear()
    sx, sw = 20, 560                 # each object's Stack box
    vx, vw = 700, 420                # the vtables region
    cx, cw = 1240, 460               # the code region
    o, objs = [], []
    y = 6
    for name, cls in (("robotaxi", "RoboTaxi"), ("taxi", "Taxi")):
        o += l7.name_tag(sx + sw / 2, y, name, w=230, h=52, size=34)
        by = y + 62
        ix, iw = sx + 24, sw - 48
        p, b1 = rows(ix, by + l7.HEAD + 4, iw, [("(hidden pointer)", ""), ("- max_speed_", "13.4"),
                                                 ("- speed_", "0.0")], "Vehicle part")
        own = [("- driver_name_", '"Ana"')] if cls == "Taxi" else [("(its own members)", "")]
        p2, b2 = rows(ix, b1 + 6, iw, own, f"{cls} part", dash_last=(cls == "RoboTaxi"))
        bottom = b2 + 24
        o += l7.box(sx, by, sw, bottom - by, "stack", "Stack") + p + p2
        objs.append((cls, ix, iw, by + l7.HEAD + 4 + CAP))       # top of the first row
        y = bottom + 40
    total_h = y - 34
    o += region(vx - 20, 68, vw + 40, total_h - 68, "vtables")
    o += region(cx - 20, 68, cw + 40, total_h - 68, "Code")
    for k, (cls, ix, iw, r0) in enumerate(objs):
        # the vtable, its first entry level with the hidden pointer
        top = r0 - CAP
        p, vb = rows(vx, top, vw, [("destructor", ""), ("drive", "")], f"{cls}'s vtable",
                     SLATE_FIELD, SLATE)
        o += p
        mid = r0 + ROW / 2
        o += l7.path_arrow([(ix + iw, mid)], (vx, mid), (vx, r0, vx + vw, vb),
                           f"{cls} hidden pointer", l7.BLUE)
        # the code of each entry, level with it
        for j, fn in enumerate((f"{cls}::~{cls}", f"{cls}::drive")):
            fy = r0 + j * ROW
            o.append(l7.rrect(cx, fy + 6, cw, ROW - 12, 10, SLATE_FIELD, SLATE, 3))
            o.append(l7.txt(cx + cw / 2, fy + ROW / 2 + 12, fn, l7.SMALL - 2, l7.INK, l7.FM, "bold"))
            o += l7.path_arrow([(vx + vw, fy + ROW / 2)], (cx, fy + ROW / 2),
                               (cx, fy + 6, cx + cw, fy + ROW - 6), f"{cls} entry {j}", SLATE)
        if k == 0:
            o += l7.number_tag((ix + iw + vx) / 2, mid - 48, 1)
            o += l7.number_tag((vx + vw + cx) / 2, r0 + ROW + ROW / 2 + 48, 2)   # under the drive arrow
    l7.check_arrows()
    return o, cx + cw + 40, total_h + 8


def slicing_virtual_memory():
    l7.ARROWS.clear()
    l7.LABELS.clear()
    w = 720  # wide enough for (hidden pointer) and Vehicle's vtable on one row
    by = 6 + 62
    objs, o = [], []
    for x, name, vt, own, total in ((20, "taxi", "Taxi's vtable", True, "56 bytes"),
                                    (960, "copy", "Vehicle's vtable", False, "24 bytes")):
        o += l7.name_tag(x + w / 2, 6, name, w=180, h=52, size=34)
        ix, iw = x + 24, w - 48
        p, b1 = rows(ix, by + l7.HEAD + 4, iw, [("(hidden pointer)", vt), ("- max_speed_", "13.4"),
                                                 ("- speed_", "0.0")], "Vehicle part")
        b = b1
        if own:
            p2, b = rows(ix, b1 + 6, iw, [("- driver_name_", '"Ana"')], "Taxi part")
            p += p2
        objs.append((x, ix, iw, b1, b, total, p))
    bottom = max(ob[4] for ob in objs) + 28 + 60
    for x, ix, iw, b1, b, total, p in objs:
        o += l7.box(x, by, w, b + 28 + 60 - by, "stack", "Stack") + p + l7.measure(ix, ix + iw, b + 28, total)
    (tx, tix, tiw, tb1, tb, *_), (cx, cix, ciw, cb1, *_) = objs
    vtop = by + l7.HEAD + 4 + CAP
    mid = (vtop + ROW + tb1) / 2            # the middle of the two rows whose values are copied
    o += l7.path_arrow([(tx + w, mid)], (cix, mid), (cix, vtop, cix + ciw, cb1), "copied values", l7.BLUE)
    o += l7.number_tag((tx + w + cix) / 2, mid - 50, 1)
    o += l7.number_tag(tx + w + 50, tb - ROW / 2, 2)      # beside driver_name_, not copied
    o += l7.number_tag(cx + w + 50, vtop + ROW / 2, 3)    # beside copy's hidden pointer
    l7.check_arrows()
    return o, cx + w + 100, bottom + 8


FIGS = [
    ("vtable_memory", "Each object's hidden pointer leads to its class's vtable, and each entry to a method",
     vtable_memory,
     "Three columns. On the left, two blue Stack boxes, one above the other. The upper one, under the name tag "
     "robotaxi, holds a Vehicle part with three rows: (hidden pointer), max_speed_ 13.4 and speed_ 0.0, then a "
     "RoboTaxi part with one gray row, (its own members). The lower one, under the name tag taxi, holds the same "
     "Vehicle part, then a Taxi part with one row, driver_name_ \"Ana\". In the middle, a slate box headed vtables "
     "holds two tables, RoboTaxi's vtable and Taxi's vtable, each with two entries, destructor and drive. A blue "
     "arrow tagged 1 runs from robotaxi's hidden pointer to RoboTaxi's vtable, and another from taxi's hidden "
     "pointer to Taxi's vtable. On the right, a slate box headed Code holds four boxes: RoboTaxi::~RoboTaxi, "
     "RoboTaxi::drive, Taxi::~Taxi and Taxi::drive. A slate arrow runs from each entry to the code of the same "
     "class; the one from RoboTaxi's drive entry to RoboTaxi::drive is tagged 2."),
    ("slicing_virtual_memory", "Vehicle copy{taxi}; with a virtual drive: the copy has its own hidden pointer",
     slicing_virtual_memory,
     "Two blue Stack boxes side by side. On the left, under the name tag taxi, one object in two parts. The first "
     "part, captioned Vehicle part, has three rows: (hidden pointer) Taxi's vtable, then max_speed_ 13.4 and "
     "speed_ 0.0, each marked with a minus sign for private. The second part, captioned Taxi part, has one row: "
     "driver_name_ \"Ana\", marked private, with tag 2 beside it. A measuring line under taxi reads 56 bytes. On "
     "the right, under the name tag copy, one part, captioned Vehicle part, with three rows: (hidden pointer) "
     "Vehicle's vtable, with tag 3 beside it, then max_speed_ 13.4 and speed_ 0.0. A measuring line under copy "
     "reads 24 bytes. A blue arrow tagged 1 runs from the Vehicle part of taxi to the Vehicle part of copy."),
]


def main(png, only=()):
    for name, title, make, desc in FIGS:
        if only and name not in only:
            continue
        print(name)
        body, w, h = make()
        out = [
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" version="1.1" id="{name}">',
            f'  <title>{l7.esc(title)}</title>', f'  <desc>{l7.esc(desc)}</desc>',
            f'  <rect width="{w}" height="{h}" fill="#ffffff"/>']
        out += ["  " + e for e in body] + ["</svg>"]
        path = os.path.join(HERE, f"{name}.svg")
        open(path, "w").write("\n".join(out) + "\n")
        print(f"svg   {name}.svg")
        if png:
            subprocess.run(["inkscape", "--export-type=png", "--export-dpi=300", "--export-background=white",
                            "--export-background-opacity=1",
                            f"--export-filename={os.path.join(PNGDIR, name + '.png')}", path],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"png   {name}.png")


if __name__ == "__main__":
    main("--png" in sys.argv, [a for a in sys.argv[1:] if not a.startswith("--")])
