#!/usr/bin/env python3
"""Figures of the reading material "Mobile Robot Messages".

    python3 robot_messages_figures.py              # every figure
    python3 robot_messages_figures.py rmsg_axes    # one figure, by name

Each figure is written as svg/<name>.svg, then exported by Inkscape to ../<name>.png at
300 dpi on an opaque white background, trimmed to 15 px of white on each side. The ROS
graph (rmsg_odometry_sources) is drawn with Graphviz in the style of the L10 figures: a
node is a white rounded box with its name in bold code font, a topic a navy box with its
name and message type. The other figures are drawn here as SVG.

What each figure draws, and where it comes from:
    rmsg_axes             REP 103: x forward, y left, z up; yaw grows counterclockwise
    rmsg_twist            three Twist commands (values chosen for the example) and the path
                          each one drives: straight, a turn in place, a circle to the left
                          of radius linear.x / angular.z
    rmsg_odometry_sources the ROSbot's topics (rosbot_controller/launch/controller.yaml:
                          differential_drive_controller/odom to odometry/wheels,
                          imu_broadcaster/imu to imu/data; rosbot_localization: the node
                          "ekf" fuses odom0 odometry/wheels and imu0 imu/data and publishes
                          odometry/filtered), and GP1's stand-in robot
    rmsg_pose             a pose in the odom frame: x = 2.0 m, y = 1.0 m, yaw = 90 degrees
                          (the values of the page's measured example)
    rmsg_scan             LaserScan beams: the angle of beam i is angle_min + i *
                          angle_increment (the message's own comments); left, a general scan
                          drawn with large angles; right, GP1's three beams at -0.1, 0 and
                          0.1 rad, drawn to scale
"""
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PNGDIR = os.path.dirname(HERE)

NAVY = "#14325c"
DIM = "#5a5a5a"
LIGHT = "#e8edf4"
RED, GREEN, BLUE = "#c0392b", "#1e8449", "#1f4e99"
FONT, MONO = "Fira Sans", "Fira Mono"


# ---------------------------------------------------------------- SVG helpers

def svg(width, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">\n'
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="white"/>\n'
            '<defs>\n'
            + "".join(f'<marker id="head_{n}" viewBox="0 0 10 10" refX="9" refY="5" '
                      f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                      f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>\n'
                      for n, c in (("navy", NAVY), ("red", RED), ("green", GREEN),
                                   ("blue", BLUE), ("dim", DIM)))
            + '</defs>\n' + body + '</svg>\n')


def text(x, y, s, size=17, color=NAVY, anchor="start", font=FONT, weight="normal"):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>\n')


def line(x1, y1, x2, y2, color=NAVY, width=2.5, head=None, dash=None):
    marker = f' marker-end="url(#head_{head})"' if head else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
            f'stroke-width="{width}"{d}{marker}/>\n')


def arc(cx, cy, r, a0, a1, color=NAVY, width=2.5, head=None, dash=None):
    """A counterclockwise arc on the page (y up), from angle a0 to a1, in degrees."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 0 if a1 > a0 else 1
    marker = f' marker-end="url(#head_{head})"' if head else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} {sweep} {x1:.1f},{y1:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{width}"{d}{marker}/>\n')


def robot(cx, cy, heading_deg=0.0, length=150, width=110, fill=LIGHT, stroke=NAVY):
    """A four-wheeled robot seen from above, facing heading_deg (0 = right, counterclockwise
    positive, as on the page with y up). The front is the side with the triangle."""
    h, w = length / 2, width / 2
    wl, ww = length * 0.24, width * 0.13
    parts = [f'<rect x="{-h}" y="{-w}" width="{length}" height="{width}" rx="14" '
             f'fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>']
    for sx in (-1, 1):
        for sy in (-1, 1):
            x = sx * (h - wl * 0.75) - wl / 2
            y = sy * (w + ww / 2) - ww / 2
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{wl:.1f}" height="{ww:.1f}" '
                         f'rx="3" fill="{stroke}"/>')
    t = length * 0.12
    parts.append(f'<path d="M{h - 10},0 L{h - 10 - t},{-t * 0.8} L{h - 10 - t},{t * 0.8} z" '
                 f'fill="{stroke}"/>')
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({-heading_deg:.1f})">'
            + "".join(parts) + '</g>\n')


FIGURES = {}


# ---------------------------------------------------------------- rmsg_axes

def fig_axes():
    cx, cy = 230, 270
    b = robot(cx, cy)
    b += line(cx, cy, cx + 250, cy, RED, 3, "red")
    b += text(cx + 262, cy + 6, "x: forward", 19, RED)
    b += line(cx, cy, cx, cy - 220, GREEN, 3, "green")
    b += text(cx + 12, cy - 210, "y: left", 19, GREEN)
    b += f'<circle cx="{cx}" cy="{cy}" r="11" fill="white" stroke="{BLUE}" stroke-width="3"/>\n'
    b += f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{BLUE}"/>\n'
    b += text(cx - 30, cy + 32, "z: up, out", 14, BLUE, "middle")
    b += text(cx - 30, cy + 48, "of the page", 14, BLUE, "middle")
    b += arc(cx, cy, 128, 8, 62, NAVY, 2.5, "navy")
    b += text(cx + 112, cy - 118, "positive yaw:", 17, NAVY)
    b += text(cx + 112, cy - 98, "counterclockwise", 17, NAVY)
    b += text(cx + 112, cy - 78, "(a turn to the left)", 17, NAVY)
    return svg(600, 400, b)


FIGURES["rmsg_axes"] = fig_axes


# ---------------------------------------------------------------- rmsg_twist

def fig_twist():
    b = ""
    w, top = 330, 40
    titles = [("linear.x = 0.2", "angular.z = 0.0"),
              ("linear.x = 0.0", "angular.z = 0.5"),
              ("linear.x = 0.2", "angular.z = 0.5")]
    notes = ["drives straight ahead", "turns in place, to the left",
             "drives on a circle, to the left"]
    for k, (t1, t2) in enumerate(titles):
        x0 = k * w
        b += text(x0 + w / 2, top, t1, 18, NAVY, "middle", MONO)
        b += text(x0 + w / 2, top + 24, t2, 18, NAVY, "middle", MONO)
        b += text(x0 + w / 2, 395, notes[k], 17, DIM, "middle")
    # 1: straight ahead
    rx, ry = 70, 290
    b += line(rx + 40, ry, rx + 250, ry, NAVY, 2.5, "navy", "8 6")
    b += robot(rx, ry, 0, 70, 52)
    # 2: turn in place
    rx, ry = w + w / 2, 260
    b += robot(rx, ry, 0, 70, 52)
    b += arc(rx, ry, 62, -40, 220, NAVY, 2.5, "navy", "8 6")
    # 3: a circle to the left, radius 120 px; quarter turn, then the robot drawn again
    rx, ry, r = 2 * w + 60, 330, 160
    ccx, ccy = rx, ry - r
    pts = [(ccx + r * math.sin(math.radians(a)), ccy + r * math.cos(math.radians(a)))
           for a in range(0, 91, 3)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    b += (f'<path d="{d}" fill="none" stroke="{NAVY}" stroke-width="2.5" '
          f'stroke-dasharray="8 6" marker-end="url(#head_navy)"/>\n')
    b += robot(rx, ry, 0, 70, 52)
    b += robot(ccx + r, ccy, 90, 70, 52, fill="#f2f2f2", stroke="#9a9a9a")
    b += f'<circle cx="{ccx}" cy="{ccy}" r="4" fill="{DIM}"/>\n'
    b += line(ccx, ccy, ccx + r * math.cos(math.radians(225)) * -1 * 0,
              ccy, DIM, 0)  # no-op keeps the center marker alone
    b += line(ccx, ccy, ccx, ccy + r - 34, DIM, 1.8, None, "4 4")
    b += text(ccx - 10, ccy + r / 2 + 2, "radius", 15, DIM, "end")
    return svg(3 * w, 410, b)


FIGURES["rmsg_twist"] = fig_twist


# ---------------------------------------------------------------- rmsg_pose

def fig_pose():
    ox, oy, s = 90, 360, 150          # origin of odom on the page; 150 px per meter
    rx, ry = ox + 2.0 * s, oy - 1.0 * s
    b = line(ox, oy, ox + 3.0 * s, oy, RED, 3, "red")
    b += text(ox + 3.0 * s + 10, oy + 6, "x", 19, RED)
    b += line(ox, oy, ox, oy - 2.0 * s, GREEN, 3, "green")
    b += text(ox - 6, oy - 2.0 * s - 12, "y", 19, GREEN, "middle")
    b += text(ox - 10, oy + 26, "odom", 17, NAVY, "middle", MONO, "bold")
    for m in (1, 2):
        b += line(ox + m * s, oy - 6, ox + m * s, oy + 6, RED, 2)
        b += text(ox + m * s, oy + 26, f"{m} m", 15, DIM, "middle")
    b += line(ox - 6, oy - s, ox + 6, oy - s, GREEN, 2)
    b += text(ox - 12, oy - s + 5, "1 m", 15, DIM, "end")
    b += line(rx, ry + 50, rx, oy, DIM, 1.6, None, "5 5")
    b += line(rx - 42, ry, ox, ry, DIM, 1.6, None, "5 5")
    b += robot(rx, ry, 90, 92, 68)
    b += line(rx, ry, rx + 120, ry, DIM, 1.8, None, "6 5")
    b += arc(rx, ry, 74, 4, 86, NAVY, 2.5, "navy")
    b += text(rx + 70, ry - 62, "yaw = 90° (1.57 rad)", 17, NAVY)
    b += text(rx + 34, ry + 84, "position:", 17, NAVY)
    b += text(rx + 34, ry + 106, "x = 2.0 m, y = 1.0 m", 17, NAVY)
    return svg(640, 440, b)


FIGURES["rmsg_pose"] = fig_pose


# ---------------------------------------------------------------- rmsg_scan

def fig_scan():
    b = ""
    # left: a general scan, angles drawn large
    rx, ry, L = 150, 300, 230
    angles = [-60, -40, -20, 0, 20, 40, 60]
    for i, a in enumerate(angles):
        x = rx + L * math.cos(math.radians(a))
        y = ry - L * math.sin(math.radians(a))
        strong = i in (0, len(angles) - 1)
        b += line(rx, ry, x, y, NAVY if strong else "#8aa0bd", 2.4 if strong else 1.6)
    b += robot(rx, ry, 0, 70, 52)
    x0 = rx + L * math.cos(math.radians(-60)); y0 = ry - L * math.sin(math.radians(-60))
    x6 = rx + L * math.cos(math.radians(60)); y6 = ry - L * math.sin(math.radians(60))
    b += text(x0 + 12, y0 + 8, "ranges[0]", 16, NAVY, "start", MONO)
    b += text(x6 + 12, y6 + 4, "ranges[6]", 16, NAVY, "start", MONO)
    b += arc(rx, ry, 95, -2, -58, RED, 2.2, "red")
    b += text(rx + 30, ry + 120, "angle_min", 16, RED, "end", MONO)
    b += text(rx + 30, ry + 140, "(negative: right)", 14, RED, "end")
    b += arc(rx, ry, 95, 2, 58, GREEN, 2.2, "green")
    b += text(rx + 30, ry - 112, "angle_max", 16, GREEN, "end", MONO)
    b += text(rx + 30, ry - 132, "(positive: left)", 14, GREEN, "end")
    b += arc(rx, ry, 200, 0, 20, BLUE, 2.2)
    b += text(rx + 245, ry - 28, "angle_increment", 16, BLUE, "start", MONO)
    b += text(rx + 120, 32, "a scan, angles drawn large", 17, DIM, "middle")
    # right: GP1's three beams, to scale
    ox, oy, L2 = 660, 300, 300
    for i, a in enumerate((-0.1, 0.0, 0.1)):
        x = ox + L2 * math.cos(a); y = oy - L2 * math.sin(a)
        b += line(ox, oy, x, y, NAVY, 2.4)
        b += text(x + 10, y + 6 + (8 if a < 0 else -8 if a > 0 else 0),
                  f"ranges[{i}]  ({a:+.1f} rad)".replace("+0.0", "0.0"), 15, NAVY, "start", MONO)
    b += robot(ox, oy, 0, 70, 52)
    b += text(ox + 190, 32, "GP1's three beams, to scale", 17, DIM, "middle")
    return svg(1220, 560, b)


FIGURES["rmsg_scan"] = fig_scan


# ---------------------------------------------------------------- rmsg_odometry_sources

HEAD = f"""  graph [fontname="{FONT}", bgcolor="white", pad="0.25", nodesep="0.35", ranksep="0.7",
         rankdir=LR, newrank=true];
  node [fontname="{FONT}", fontsize=16, shape=box, style="rounded", color="{NAVY}",
        fontcolor="{NAVY}", penwidth=2, margin="0.20,0.10"];
  edge [fontname="{FONT}", fontsize=14, color="{NAVY}", fontcolor="{DIM}", penwidth=1.6,
        arrowsize=0.8];
"""


def gnode(name, label, note=""):
    more = f'<br/><font point-size="12" color="{DIM}">{note}</font>' if note else ""
    return f'  {name} [label=<<b><font face="{MONO}">{label}</font></b>{more}>];\n'


def gtopic(name, label, msg_type):
    return (f'  {name} [label=<<font face="{MONO}">{label}</font><br/>'
            f'<font point-size="12" face="{MONO}">{msg_type}</font>>, style="rounded,filled", '
            f'fillcolor="{NAVY}", fontcolor="white"];\n')


def ghard(name, label):
    return (f'  {name} [label="{label}", style="rounded,dashed", color="{DIM}", '
            f'fontcolor="{DIM}"];\n')


def cluster(name, label, body):
    return (f'  subgraph cluster_{name} {{\n    graph [label="{label}", style="rounded", '
            f'color="{DIM}", fontcolor="{DIM}", fontsize=17, labeljust="l", margin=14];\n'
            + body + "  }\n")


def fig_odometry_sources():
    dot = ("digraph G {\n" + HEAD
           + cluster("rosbot", "On the ROSbot (GP2)",
                     gnode("ddc", "differential_drive_controller")
                     + gnode("imb", "imu_broadcaster")
                     + gtopic("tw", "odometry/wheels", "nav_msgs/msg/Odometry")
                     + gtopic("ti", "imu/data", "sensor_msgs/msg/Imu")
                     + gnode("ekf", "ekf", "robot_localization")
                     + gtopic("tf", "odometry/filtered", "nav_msgs/msg/Odometry")
                     + f'  you [label="your nodes"];\n')
           + cluster("gp1", "In GP1",
                     gnode("sir", "stand_in_robot_node")
                     + gtopic("tf1", "odometry/filtered", "nav_msgs/msg/Odometry")
                     + gnode("nav", "navigation_node"))
           + "  ddc -> tw; imb -> ti; tw -> ekf; ti -> ekf; ekf -> tf; tf -> you;\n"
           + "  sir -> tf1; tf1 -> nav;\n"
           + "}\n")
    return dot


FIGURES["rmsg_odometry_sources"] = fig_odometry_sources
DOT = {"rmsg_odometry_sources"}


def render(name):
    svg_path = os.path.join(HERE, f"{name}.svg")
    png_path = os.path.join(PNGDIR, f"{name}.png")
    if name in DOT:
        dot_path = os.path.join(HERE, f"{name}.dot")
        with open(dot_path, "w") as f:
            f.write(FIGURES[name]())
        subprocess.run(["dot", "-Tsvg", "-o", svg_path, dot_path], check=True)
    else:
        with open(svg_path, "w") as f:
            f.write(FIGURES[name]())
    subprocess.run(["inkscape", "--export-type=png", "--export-dpi=300",
                    "--export-background=white", "--export-background-opacity=1",
                    f"--export-filename={png_path}", svg_path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["convert", png_path, "-trim", "+repage", "-bordercolor", "white",
                    "-border", "15", "-units", "PixelsPerInch", "-density", "300", png_path],
                   check=True)
    print(f"png   {name}.png")


if __name__ == "__main__":
    for n in sys.argv[1:] or list(FIGURES):
        render(n)
