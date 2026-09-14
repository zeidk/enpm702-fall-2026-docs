#!/usr/bin/env python3
"""Generates every figure for ENPM702 L3 (Pointers and Memory Management).

Run it from anywhere; the SVGs are written next to this file and the PNGs
one directory up (the slides use the PNGs; docs/source/_static/images/l3
gets a copy).

    python3 pointers.svg.py            # SVG only
    python3 pointers.svg.py --png      # SVG + 350 dpi PNG via inkscape

The visual vocabulary is the one L2 established in visualization.svg: a
variable is a colored header bar naming the segment it lives in, over a
white body holding its value, with the name to the left and the address
underneath. Keeping it identical is the point -- a student who learned to
read the L2 diagrams can read these without being taught a second
notation.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PNGDIR = os.path.join(os.path.dirname(HERE), "png")

# --- the L2 palette, unchanged ---------------------------------------------
FS = "'Fira Sans', Helvetica, Arial, sans-serif"
FM = "'Fira Mono', 'DejaVu Sans Mono', monospace"
BLUE, BLUE_L = "#2f6fb5", "#cfe0f7"      # stack
RED, RED_L = "#c0392b", "#f8d0cc"        # heap
OLIVE = "#7d8f1c"                        # "this is allowed"
TEAL = "#1f7a6c"
INK, DIM, FAINT = "#1b1b1b", "#555555", "#8a8a8a"
GREY, GREY_L = "#9a9a9a", "#ececec"

HDR, BODY, BOXW = 44, 76, 300            # header height, body height, width

SEG = {"stack": (BLUE, "Stack"), "heap": (RED, "Heap")}


# --- primitives -------------------------------------------------------------
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, s, size=24, fill=INK, font=FS, anchor="middle", weight="normal",
        style=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'
            f'{style}>{esc(s)}</text>')


def rect(x, y, w, h, fill="#ffffff", stroke=None, sw=2.5, dash=None, rx=0):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'
    if rx:
        s += f' rx="{rx}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    if dash:
        s += f' stroke-dasharray="{dash}"'
    return s + "/>"


def line(x1, y1, x2, y2, stroke=DIM, sw=1.8, dash=None):
    s = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
         f'stroke-width="{sw}"')
    if dash:
        s += f' stroke-dasharray="{dash}"'
    return s + "/>"


def arrow(x1, y1, x2, y2, color=BLUE, sw=4.5, dash=None):
    s = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
         f'stroke-width="{sw}" marker-end="url(#a-{color[1:]})"')
    if dash:
        s += f' stroke-dasharray="{dash}"'
    return s + "/>"


def curve(x1, y1, cx, cy, x2, y2, color=BLUE, sw=4.5, dash=None):
    s = (f'<path d="M {x1},{y1} Q {cx},{cy} {x2},{y2}" fill="none" '
         f'stroke="{color}" stroke-width="{sw}" marker-end="url(#a-{color[1:]})"')
    if dash:
        s += f' stroke-dasharray="{dash}"'
    return s + "/>"


def check(x, y, color=OLIVE, s=1.0):
    """A tick mark centred on (x, y)."""
    return (f'<path d="M {x-16*s},{y} l {11*s},{13*s} l {21*s},{-27*s}" '
            f'fill="none" stroke="{color}" stroke-width="{6*s}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def cross(x, y, color=RED, s=1.0):
    """An X centred on (x, y)."""
    return (f'<path d="M {x-14*s},{y-14*s} l {28*s},{28*s} '
            f'M {x+14*s},{y-14*s} l {-28*s},{28*s}" fill="none" '
            f'stroke="{color}" stroke-width="{6*s}" stroke-linecap="round"/>')


def var_box(x, y, seg, value, name=None, addr=None, w=BOXW, mono=False,
            vsize=None, freed=False, dead=False, note=None,
            name_above=False):
    """One variable, drawn the way L2 draws variables.

    freed=True greys the whole box out: the storage is no longer ours, but
    something is still drawn there because the bits do not disappear.
    """
    color, label = SEG[seg]
    if freed or dead:
        label = f"{label} (freed)" if freed else f"{label} (gone)"
        color = GREY
    faded = freed or dead
    # One rectangle defines the whole box, header and body together, and
    # carries the outline. The colored header band is then painted over
    # the top of it, grown by half the stroke width on each side so that
    # its edges land on the OUTER edge of that stroke.
    #
    # Both adjustments matter. Drawing the header as its own full-width
    # fill-only rectangle is what made it come out narrower than the body
    # underneath: a stroke straddles the edge it is drawn on, so a
    # stroked rectangle is half a stroke wider on each side than a
    # fill-only one of the same nominal width. And matching the two
    # widths is not enough on a dashed (freed) box, where the gaps in the
    # dash would expose the difference wherever the stroke is absent.
    sw = 2.5
    o = [rect(x, y, w, HDR + BODY, fill=GREY_L if faded else "#ffffff",
              stroke=color, sw=sw, dash="10 8" if faded else None),
         rect(x - sw / 2, y - sw / 2, w + sw, HDR, fill=color),
         txt(x + w / 2, y + 31, label, 26, "#ffffff", FS, weight="600")]
    if vsize is None:
        vsize = 26 if mono else 36
    o.append(txt(x + w / 2, y + HDR + BODY / 2 + vsize * 0.35, value, vsize,
                 FAINT if faded else INK, FM if mono else FS, weight="bold"))
    if name:
        if name_above:
            o.append(txt(x + w / 2, y - 16, name, 28,
                         FAINT if faded else INK, FS, weight="bold"))
        else:
            o.append(txt(x - 16, y + HDR + BODY / 2 + 10, name, 28,
                         FAINT if faded else INK, FS, anchor="end",
                         weight="bold"))
    if addr:
        o.append(txt(x + w / 2, y + HDR + BODY + 32, addr, 21, DIM, FM))
    if note:
        o.append(txt(x + w / 2, y + HDR + BODY + (66 if addr else 34), note,
                     21, FAINT, FS))
    return o


def write(name, w, h, body, title, desc):
    markers = "".join(
        f'<marker id="a-{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{c}"/></marker>'
        for c in (BLUE, RED, DIM, OLIVE, TEAL, GREY))
    out = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" version="1.1" id="{name}">',
        f'  <title>{esc(title)}</title>',
        f'  <desc>{esc(desc)}</desc>',
        f'  <defs>{markers}</defs>',
        f'  <rect width="{w}" height="{h}" fill="#ffffff"/>',
    ]
    out += ["  " + e for e in body]
    out.append("</svg>")
    path = os.path.join(HERE, name + ".svg")
    with open(path, "w") as f:
        f.write("\n".join(out) + "\n")
    return path


def code(x, y, s, size=27, fill=INK):
    return txt(x, y, s, size, fill, FM, anchor="start")


# --- the figures ------------------------------------------------------------
# Every figure uses the same running example: the flight controller of a
# small quadrotor. altitude_m is the altitude the vehicle is holding,
# altitude_ptr points at it, and battery_pct is a reading the controller
# allocates on the heap. Names are the ones a student should be writing.


def brace_down(x0, x1, y, depth=22, q=14):
    """A horizontal curly brace spanning x0..x1 whose point faces down."""
    cx = (x0 + x1) / 2.0
    return (f'<path d="M {x0},{y - depth} q 0,{depth} {q},{depth} '
            f'L {cx - q},{y} q {q},0 {q},{q} q 0,{-q} {q},{-q} '
            f'L {x1 - q},{y} q {q},0 {q},{-depth}" fill="none" '
            f'stroke="{FAINT}" stroke-width="2.5"/>')


def f_anatomy():
    """The pointer, the object, and what each part of the picture is."""
    W = 1400
    o = [txt(W / 2, 78, "int altitude_m{120};    int* altitude_ptr{&altitude_m};",
             29, INK, FM, weight="bold")]
    px, ax, y = 180, 900, 230
    o += var_box(px, y, "stack", "0x7ffd…a04", name="altitude_ptr",
                 addr="0x7ffd…9f8", mono=True, name_above=True)
    o += var_box(ax, y, "stack", "120", name="altitude_m", addr="0x7ffd…a04",
                 name_above=True)
    mid = y + HDR + BODY / 2
    o.append(arrow(px + BOXW + 12, mid, ax - 12, mid))
    o.append(txt((px + BOXW + ax) / 2, mid - 22, "points to", 24, BLUE))
    o.append(txt(px + BOXW / 2, 452,
                 "a pointer is a variable: it has its own", 22, FAINT))
    o.append(txt(px + BOXW / 2, 480,
                 "address, and its value is another address", 22, FAINT))
    o.append(txt(ax + BOXW / 2, 452, "the object being pointed at;", 22, FAINT))
    o.append(txt(ax + BOXW / 2, 480, "it does not know about the pointer",
                 22, FAINT))
    return write("pointer_anatomy", W, 540, o,
                 "A pointer and the object it points to",
                 "Two variable boxes on the stack. The left box, named "
                 "altitude_ptr, holds the address 0x7ffd…a04 and itself sits "
                 "at address 0x7ffd…9f8. The right box, named altitude_m, "
                 "holds the value 120 and sits at address 0x7ffd…a04. A blue "
                 "arrow runs from altitude_ptr to altitude_m, labelled "
                 "points to.")


def f_ops():
    """&altitude_m and *altitude_ptr as inverse moves."""
    W = 1400
    o = [txt(W / 2, 60, "the two operators that move between the boxes",
             28, DIM, FS)]
    px, ax, y, w = 150, 950, 270, 300
    o += var_box(px, y, "stack", "0x7ffd…a04", name="altitude_ptr", mono=True,
                 name_above=True)
    o += var_box(ax, y, "stack", "120", name="altitude_m", name_above=True)
    mid = y + HDR + BODY / 2
    cx = (px + w + ax) / 2
    # &altitude_m : from the object, through the gap, into the pointer
    o.append(curve(ax - 12, mid - 22, cx, 150, px + w + 12, mid - 22,
                   color=TEAL))
    o.append(txt(cx, 178, "&altitude_m", 30, TEAL, FM, weight="bold"))
    o.append(txt(cx, 208, "the address of altitude_m,", 21, TEAL))
    o.append(txt(cx, 234, "which is what altitude_ptr stores", 21, TEAL))
    # *altitude_ptr : from the pointer, through the gap, into the object
    o.append(curve(px + w + 12, mid + 22, cx, 580, ax - 12, mid + 22,
                   color=RED))
    o.append(txt(cx, 512, "*altitude_ptr", 30, RED, FM, weight="bold"))
    o.append(txt(cx, 542, "the object at that address,", 21, RED))
    o.append(txt(cx, 568, "which is altitude_m", 21, RED))
    return write("address_of_deref", W, 620, o,
                 "The address-of and dereference operators",
                 "The boxes altitude_ptr and altitude_m. A teal arrow curves "
                 "through the gap from altitude_m to altitude_ptr, labelled "
                 "&altitude_m, the address of altitude_m, which is what "
                 "altitude_ptr stores. A red arrow curves the other way, "
                 "labelled *altitude_ptr, the object at that address, which "
                 "is altitude_m.")


def f_typed():
    """Why a pointer has a type: sizeof(p) against sizeof(*p).

    Three real objects at three different addresses, which is the whole
    of the legality question: each pointer points at an object of its own
    type, so there is no cast and no aliasing anywhere in the picture.
    The values are the ones from the sizeof example just above in the
    notes, and the bytes are what GCC really stores for them.

    The figure sits directly under "every pointer is 8 bytes", so every
    row carries BOTH numbers in sizeof() form. A bar labelled "int*" next
    to "4 bytes" reads as "an int* is 4 bytes", which is the one thing
    this page must not say.

    Pointer boxes are Stack blue because in this deck colour means
    segment, not type. The pointee bytes are tinted teal, which is no
    segment, so they cannot be misread as "this lives on the heap".
    """
    x_box, boxw = 130, 290
    sx, cw, chh = 560, 56, 64
    W, H = 1300, 900
    teal_l = "#cfe8e3"
    resx = sx + 8 * cw + 36
    o = [txt(W / 2, 62, "every pointer is 8 bytes, whatever it points at",
             30, INK, FS, weight="600"),
         txt(W / 2, 98, "the type decides what the dereference reads, "
                        "not how big the pointer is", 23, DIM),
         txt(resx, 138, "value read", 20, FAINT, FS, anchor="start")]
    # Byte patterns dumped with memcpy on the course toolchain (GCC 13,
    # little-endian), not worked out by hand. Written here in hex
    # because that is how the dump came out; drawn as bits below.
    rows = [("status_ptr", "char*", "status", "0x7ffd…a00",
             ["41"], "'A'"),
            ("altitude_ptr", "int*", "altitude_m", "0x7ffd…a04",
             ["78", "00", "00", "00"], "120"),
            ("voltage_ptr", "double*", "voltage", "0x7ffd…a08",
             ["33", "33", "33", "33", "33", "33", "26", "40"], "11.1")]
    for i, (pname, ptype, oname, addr, hexes, value) in enumerate(rows):
        rtop = 150 + i * 212
        mid = rtop + 80
        count = len(hexes)
        end = sx + cw * count
        # the pointer: a stack variable whose value is an address
        o += var_box(x_box, rtop + 20, "stack", addr, w=boxw, mono=True)
        o.append(txt(x_box + boxw / 2, rtop + 4, f"{ptype} {pname}", 24, INK,
                     FM, weight="bold"))
        o.append(txt(x_box + boxw / 2, rtop + 170, f"sizeof({pname}) == 8",
                     20, DIM, FM))
        o.append(arrow(x_box + boxw + 12, mid, sx - 12, mid))
        # the pointee: exactly the bytes this object occupies
        o.append(txt(sx, rtop + 24, f"sizeof(*{pname}) == {count}", 22, TEAL,
                     FM, anchor="start", weight="bold"))
        o.append(rect(sx, rtop + 34, cw * count, 7, fill=TEAL, rx=3))
        for k, h in enumerate(hexes):
            o.append(rect(sx + k * cw, rtop + 48, cw, chh, fill=teal_l,
                          stroke=TEAL, sw=2))
            # A byte is eight bits, so draw eight bits. L2 drew them this
            # way in visualization.svg, grouped in nibbles with the
            # all-zero bytes greyed out, and that is the only byte
            # notation the course has taught. The two nibbles are stacked
            # rather than side by side purely so they fit a 56px cell:
            # same grouping L2 used, turned through ninety degrees, which
            # costs nothing to read and saves introducing hex here.
            bits = f"{int(h, 16):08b}"
            ink = FAINT if h == "00" else INK
            cx = sx + k * cw + cw / 2
            o.append(txt(cx, rtop + 75, bits[:4], 16, ink, FM, weight="bold"))
            o.append(txt(cx, rtop + 96, bits[4:], 16, ink, FM, weight="bold"))
        # Byte order is invisible in a one-byte object and unmissable once
        # the bits are on the page, so say it where it applies.
        caption = f"{oname} at {addr}"
        if count > 1:
            caption += "  ·  little-endian"
        o.append(txt(sx, rtop + 140, caption, 19, DIM, FM, anchor="start"))
        if resx - end > 40:
            o.append(line(end + 14, mid, resx - 14, mid, stroke="#c9c9c9",
                          sw=2, dash="5 6"))
        o.append(txt(resx, mid + 8, value, 24, INK, FM, anchor="start",
                     weight="bold"))
    o.append(txt(W / 2, 810, "sizeof(p) is the pointer. sizeof(*p) is the "
                             "object it points at.", 24, INK, FS))
    o.append(txt(W / 2, 846, "the boxes on the left are all the same size. "
                             "the bytes on the right are not.", 21, DIM, FS))
    return write("typed_pointer", W, H, o,
                 "Pointer size against pointee size",
                 "Three rows, each a pointer and the object it points at. "
                 "In every row a blue stack box holds an address and is "
                 "marked sizeof(p) == 8, with an arrow to the bytes of its "
                 "object, tinted teal. char* status_ptr holds 0x7ffd…a00 "
                 "and points at status, one byte, 0100 0001, reading as "
                 "the character A. int* altitude_ptr holds 0x7ffd…a04 and "
                 "points at altitude_m, four little-endian bytes, "
                 "0111 1000 then three zero bytes, reading as 120. "
                 "double* voltage_ptr holds 0x7ffd…a08 and points at "
                 "voltage, eight little-endian bytes, 0011 0011 repeated "
                 "six times then 0010 0110 and 0100 0000, reading as "
                 "11.1. Every byte is drawn as its eight bits, split into "
                 "two nibbles on two lines, the way Lecture 2 drew them. "
                 "Each pointer is 8 bytes; the objects are 1, 4 and 8 "
                 "bytes.")


def f_where():
    """The pointer is a variable; the object it points at need not be named."""
    W, bw = 1400, 230
    px, tx = 560, 1030
    o = []
    rows = [(120, "stack", "0x7ffd…a04", "altitude_m", "0x7ffd…a04", BLUE,
             ["int altitude_m{120};", "int* altitude_ptr{&altitude_m};"],
             "altitude_ptr", "120",
             "the object has a name and a scope: it dies at the end of it"),
            (440, "heap", "0x5591…2b0", None, "0x5591…2b0", RED,
             ["int* battery_pct{new int{88}};"],
             "battery_pct", "88",
             "the object has no name and no scope: it lives until delete")]
    for k, (y, seg, pval, nm, addr, col, lines, pname, val, cap) in enumerate(rows):
        for i, ln in enumerate(lines):
            o.append(code(60, y + 76 + i * 40, ln, 25))
        o += var_box(px, y, "stack", pval, name=pname, w=bw, mono=True,
                     vsize=22, name_above=True)
        o += var_box(tx, y, seg, val, name=nm, addr=addr, w=bw,
                     name_above=True)
        if nm is None:
            o.append(txt(tx + bw / 2, y - 16, "(no name)", 24, FAINT, FS))
        o.append(arrow(px + bw + 12, y + HDR + BODY / 2, tx - 12,
                       y + HDR + BODY / 2, color=col))
        o.append(txt(W / 2 + 60, y + HDR + BODY + 78, cap, 22, FAINT))
    o.append(line(60, 390, W - 60, 390, stroke="#ececec", sw=2))
    return write("pointee_location", W, 700, o,
                 "A pointer can point into the stack or into the heap",
                 "Two rows. In the top row, int altitude_m{120}; int* "
                 "altitude_ptr{&altitude_m}; draws a stack pointer box with a "
                 "blue arrow to a named stack box holding 120. In the bottom "
                 "row, int* battery_pct{new int{88}}; draws the same pointer "
                 "with a red arrow to an unnamed heap box holding 88.")


def f_new_delete():
    """The three states around new / delete / nullptr."""
    W, bw = 1440, 280
    px, hx = 560, 1030
    stages = [
        ("int* battery_pct{new int{88}};", "88", "live",
         "new returns the address of an unnamed object on the heap"),
        ("delete battery_pct;", "88", "freed",
         "the storage is returned, but battery_pct still holds the "
         "address, so it dangles"),
        ("battery_pct = nullptr;", None, "gone",
         "now the pointer says, in a way you can test, that it owns nothing"),
    ]
    o = []
    y = 60
    for i, (src, val, state, cap) in enumerate(stages):
        o.append(f'<circle cx="70" cy="{y + 30}" r="24" fill="{DIM}"/>')
        o.append(txt(70, y + 40, str(i + 1), 30, "#ffffff", FS, weight="bold"))
        o.append(code(120, y + 40, src, 28))
        mid = y + 100 + HDR + BODY / 2
        o += var_box(px, y + 100, "stack",
                     "nullptr" if state == "gone" else "0x5591…2b0",
                     name="battery_pct", w=bw, mono=True, vsize=24,
                     name_above=True)
        if val is not None:
            o += var_box(hx, y + 100, "heap", val, w=bw,
                         freed=(state == "freed"))
            if state == "live":
                o.append(arrow(px + bw + 12, mid, hx - 12, mid, color=RED))
            else:
                o.append(arrow(px + bw + 12, mid, hx - 12, mid, color=GREY,
                               dash="12 9"))
                o.append(txt((px + bw + hx) / 2, mid - 20, "dangling", 22, RED))
        else:
            o.append(txt(hx - 12, mid + 8, "no arrow: it points nowhere", 23,
                         FAINT, FS, anchor="start"))
        o.append(txt(120, y + 100 + HDR + BODY + 36, cap, 22, FAINT, FS,
                     anchor="start"))
        y += 300
    return write("new_delete", W, 1000, o,
                 "new, delete, and the state of the pointer after each",
                 "Three numbered stages. One: int* battery_pct{new int{88}}; "
                 "a stack box named battery_pct holds a heap address and a "
                 "red arrow points to a live heap box holding 88. Two: delete "
                 "battery_pct; the heap box is greyed and labelled freed, and "
                 "the arrow is dashed and labelled dangling. Three: "
                 "battery_pct = nullptr; the pointer holds nullptr and there "
                 "is no arrow.")


def _leak_panel(W, bw=250):
    """Shared geometry for the three failure figures: one column, centred."""
    return (W - bw) / 2.0, bw


def f_memory_leak():
    """The pointer dies; the block it addressed does not."""
    W, H = 760, 560
    bx, bw = _leak_panel(W)
    o = [txt(W / 2, 60, "} // scope ends here", 24, DIM, FM)]
    o += var_box(bx, 120, "stack", "0x5591…2b0", name="battery_pct", w=bw,
                 mono=True, vsize=22, dead=True, name_above=True)
    o.append(arrow(W / 2, 250, W / 2, 330, color=GREY, dash="10 8"))
    o.append(cross(W / 2, 288, s=0.9))
    o += var_box(bx, 338, "heap", "88", w=bw)
    o.append(txt(W / 2, 512, "still allocated, and now unreachable for ever",
                 23, RED))
    return write("memory_leak", W, H, o,
                 "A memory leak",
                 "A greyed-out stack box named battery_pct, labelled Stack "
                 "(gone) because its scope has ended, with a dashed arrow "
                 "down to a live heap box holding 88. The arrow is crossed "
                 "out: the block is still allocated and nothing points at it "
                 "any more.")


def f_double_delete():
    """Two pointers, one block, two deletes."""
    W, H = 760, 560
    bx, bw = _leak_panel(W)
    pw = 200
    o = []
    o += var_box(90, 120, "stack", "0x5591…2b0", name="primary", w=pw,
                 mono=True, vsize=20, name_above=True)
    o += var_box(W - 90 - pw, 120, "stack", "0x5591…2b0", name="backup",
                 w=pw, mono=True, vsize=20, name_above=True)
    o.append(arrow(90 + pw / 2, 250, W / 2 - 40, 330, color=GREY, dash="10 8"))
    o.append(arrow(W - 90 - pw / 2, 250, W / 2 + 40, 330, color=GREY,
                   dash="10 8"))
    o += var_box(bx, 338, "heap", "88", w=bw, freed=True)
    o.append(txt(W / 2, 508, "delete primary;   delete backup;", 24, RED, FM))
    o.append(txt(W / 2, 538, "the second one is undefined behavior", 23, RED))
    return write("double_delete", W, H, o,
                 "A double delete",
                 "Two stack boxes, primary and backup, both holding the same "
                 "heap address 0x5591…2b0, with dashed arrows converging on "
                 "one greyed heap box labelled Heap (freed). Deleting through "
                 "primary and then through backup frees the same block "
                 "twice.")


def f_null_deref():
    """A pointer holding nullptr, and nothing at the other end."""
    W, H = 760, 560
    bx, bw = _leak_panel(W)
    o = []
    o += var_box(bx, 120, "stack", "nullptr", name="sensor", w=bw, mono=True,
                 vsize=26, name_above=True)
    o.append(arrow(W / 2, 250, W / 2, 330, color=GREY, dash="10 8"))
    o.append(f'<circle cx="{W / 2}" cy="400" r="62" fill="#ffffff" '
             f'stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>')
    o.append(cross(W / 2, 400, s=1.2))
    o.append(txt(W / 2, 508, "*sensor is undefined behavior:", 24, RED, FM))
    o.append(txt(W / 2, 538, "test the pointer before dereferencing it", 23,
                 RED))
    return write("null_dereference", W, H, o,
                 "A null dereference",
                 "A stack box named sensor holding nullptr, with a dashed "
                 "arrow pointing down to an empty dashed circle containing a "
                 "red cross: there is no object at the other end, so "
                 "dereferencing the pointer is undefined behavior.")


def f_vs_reference():
    """A pointer is a second object; a reference is a second name."""
    W, pw, bw = 1440, 720, 220
    o = [line(pw, 40, pw, 500, stroke="#ececec", sw=2)]
    o.append(txt(pw / 2, 78, "int* altitude_ptr{&altitude_m};", 28, INK, FM,
                 weight="bold"))
    o.append(txt(pw + pw / 2, 78, "int& alt{altitude_m};", 28, INK, FM,
                 weight="bold"))
    # pointer side
    y = 220
    mid = y + HDR + BODY / 2
    o += var_box(70, y, "stack", "0x7ffd…a04", name="altitude_ptr", w=bw,
                 mono=True, vsize=20, name_above=True)
    o += var_box(430, y, "stack", "120", name="altitude_m", w=bw,
                 name_above=True)
    o.append(arrow(70 + bw + 12, mid, 430 - 12, mid))
    o.append(txt(pw / 2, 430, "two objects: altitude_ptr holds the address",
                 22, FAINT))
    o.append(txt(pw / 2, 458, "of altitude_m, and *altitude_ptr reaches it",
                 22, FAINT))
    # reference side: one box, two names, joined by a brace
    bx = pw + (pw - bw) / 2
    o += var_box(bx, y, "stack", "120", w=bw)
    o.append(txt(bx + bw / 2 - 86, y - 62, "altitude_m", 26, INK, FS,
                 weight="bold"))
    o.append(txt(bx + bw / 2 + 86, y - 62, "alt", 26, TEAL, FS, weight="bold"))
    o.append(brace_down(bx + bw / 2 - 150, bx + bw / 2 + 150, y - 16))
    o.append(txt(pw + pw / 2, 430, "one object with two names: alt is",
                 22, FAINT))
    o.append(txt(pw + pw / 2, 458, "altitude_m, and nothing else, for ever",
                 22, FAINT))
    return write("pointer_vs_reference", W, 520, o,
                 "A pointer is another object; a reference is another name",
                 "On the left, int* altitude_ptr{&altitude_m}; draws two "
                 "stack boxes joined by an arrow: altitude_ptr holds the "
                 "address of altitude_m, which holds 120. On the right, int& "
                 "alt{altitude_m}; draws a single stack box holding 120 with "
                 "two names above it, altitude_m and alt, joined to the box "
                 "by a brace.")


def f_reference_memory():
    """What a reference is in the language, and what the compiler emits."""
    W, H, bw = 1440, 620, 240
    o = [line(700, 50, 700, 560, stroke="#ececec", sw=2)]
    o.append(txt(350, 74, "what the language says", 27, DIM, FS))
    o.append(txt(1070, 74, "what GCC actually emitted", 27, DIM, FS))

    # --- left: one object, two names -------------------------------------
    bx, by = 350 - bw / 2, 210
    o += var_box(bx, by, "stack", "120", w=bw)
    o.append(txt(bx + bw / 2 - 92, by - 62, "altitude_m", 26, INK, FS,
                 weight="bold"))
    o.append(txt(bx + bw / 2 + 92, by - 62, "alt", 26, TEAL, FS,
                 weight="bold"))
    o.append(brace_down(bx + bw / 2 - 155, bx + bw / 2 + 155, by - 16))
    o.append(txt(350, by + 168, "&alt is &altitude_m", 23, INK, FM))
    o.append(txt(350, by + 202, "sizeof(alt) is sizeof(int)", 23, INK, FM))
    o.append(txt(350, by + 240, "one object; the second name costs nothing",
                 21, FAINT, FS))

    # --- right: the two builds -------------------------------------------
    sx, sw_ = 1010, 250
    for y, tag, value, notes in [
            (150, "Debug  -O0", "0x7ffd…00c",
             ["an unnamed 8-byte slot holding the address",
              "of altitude_m, exactly like an int* const"]),
            (390, "Release  -O2", None,
             ["no slot at all: every use of alt",
              "was compiled into a use of altitude_m"])]:
        o.append(txt(790, y + 62, tag, 24, INK, FM, anchor="start"))
        if value is not None:
            o.append(rect(sx, y, sw_, HDR + BODY, fill=GREY_L, stroke=GREY,
                          sw=2.5, dash="10 8"))
            o.append(rect(sx - 1.25, y - 1.25, sw_ + 2.5, HDR, fill=GREY))
            o.append(txt(sx + sw_ / 2, y + 31, "Stack (hidden)", 24,
                         "#ffffff", FS, weight="600"))
            o.append(txt(sx + sw_ / 2, y + HDR + BODY / 2 + 9, value, 24,
                         DIM, FM, weight="bold"))
        else:
            o.append(rect(sx, y, sw_, HDR + BODY, fill="#ffffff",
                          stroke="#d8d8d8", sw=2.5, dash="10 8"))
            o.append(cross(sx + sw_ / 2, y + (HDR + BODY) / 2, s=1.1))
        for k, n in enumerate(notes):
            o.append(txt(sx + sw_ / 2, y + HDR + BODY + 34 + k * 28, n, 21,
                         FAINT, FS))
    return write("reference_memory", W, H, o,
                 "A reference in the language, and in the generated code",
                 "Two panels. On the left, what the language says: a single "
                 "stack box holding 120 with two names above it, altitude_m "
                 "and alt, joined by a brace, and the notes &alt is "
                 "&altitude_m and sizeof(alt) is sizeof(int). On the right, "
                 "what GCC emitted: in a Debug build at -O0 an unnamed "
                 "greyed-out eight-byte stack slot holds the address "
                 "0x7ffd…00c, exactly like an int* const; in a Release build "
                 "at -O2 there is no slot at all, drawn as an empty dashed "
                 "box with a cross through it.")


FIGURES = [f_anatomy, f_ops, f_typed, f_where, f_new_delete,
           f_memory_leak, f_double_delete, f_null_deref, f_vs_reference,
           f_reference_memory]


def main(png=False):
    for fn in FIGURES:
        svg = fn()
        name = os.path.basename(svg)[:-4]
        print("svg  ", name + ".svg")
        if png:
            out = os.path.join(PNGDIR, name + ".png")
            subprocess.run(["inkscape", "--export-type=png",
                            "--export-dpi=350", f"--export-filename={out}",
                            svg], check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            print("png  ", os.path.relpath(out, PNGDIR))


if __name__ == "__main__":
    main("--png" in sys.argv)
