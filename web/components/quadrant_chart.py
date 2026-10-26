"""A labelled quadrant chart, drawn as inline SVG.

silverpoint's `bubble_chart` has no point labels, reference lines or axis
titles, which a quadrant reading needs: which profile sits in which quadrant.
The profile points are the same in every filter (they describe the whole
history), so this chart is static: built once in Python at compile time, with no
state and no JavaScript. It keeps the site's inks and type.
"""

import math
from dataclasses import dataclass

import reflex as rx

# Plot frame in viewBox units.
_W, _H = 600, 420
_LEFT, _RIGHT, _TOP, _BOTTOM = 48, 14, 34, 46

_INK = "#1F3D36"
_MUTED = "#5C7B71"
_RULE = "#5C7B71"
# One ink per profile, in the order of the data (muted, legible on the cream ground).
_COLORS = ["#2F6F86", "#A3542C", "#2C6355", "#9A7414", "#7A4E8C", "#4F6D2F"]

_FONT = 14
_CHAR = 7.0  # Average glyph width at _FONT, for label placement.


@dataclass(frozen=True)
class Axis:
    """One axis: the data key, its domain, ticks, the cut that splits it and its title."""

    key: str
    lo: float
    hi: float
    ticks: list[float]
    cut: float
    title: str
    percent: bool = False


def _fmt(props: dict) -> dict:
    """SVG attributes take strings or ints: round every float to one decimal."""
    return {
        key: f"{value:.1f}" if isinstance(value, float) else value for key, value in props.items()
    }


def _line(**props) -> rx.Component:
    return rx.el.svg.line(**_fmt(props))


def _text(text: str, **props) -> rx.Component:
    return rx.el.svg.text(text, **_fmt(props))


def _circle(**props) -> rx.Component:
    return rx.el.svg.circle(**_fmt(props))


def _label_box(x: float, y: float, text: str, side: str) -> tuple[float, float, float, float]:
    width = len(text) * _CHAR
    left = {"right": x, "left": x - width, "center": x - width / 2}[side]
    return (left, y - _FONT * 0.8, left + width, y + _FONT * 0.3)


def _anchor_x(side: str, cx: float, radius: float) -> float:
    """Where a label starts (right), ends (left) or is centred (center) beside its bubble."""
    return {"right": cx + radius + 5, "left": cx - radius - 5, "center": cx}[side]


def _overlaps(a: tuple, b: tuple) -> bool:
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


def quadrant_chart(
    points: list[dict],
    *,
    label_key: str,
    size_key: str,
    x: Axis,
    y: Axis,
    quadrants: tuple[str, str, str, str],
    title: str,
    description: str,
    chart_id: str,
) -> rx.Component:
    """Bubbles placed by `x` and `y`, sized by `size_key` and named by `label_key`.

    `quadrants` are the names of the top-left, top-right, bottom-left and
    bottom-right quadrants, split at `x.cut` and `y.cut`.
    """
    plot_w = _W - _LEFT - _RIGHT
    plot_h = _H - _TOP - _BOTTOM

    def sx(value: float) -> float:
        return _LEFT + (value - x.lo) / (x.hi - x.lo) * plot_w

    def sy(value: float) -> float:
        return _TOP + (1 - (value - y.lo) / (y.hi - y.lo)) * plot_h

    biggest = max(point[size_key] for point in points) or 1
    marks: list[rx.Component] = []

    # Grid, ticks and the two cuts.
    for tick in y.ticks:
        marks.append(
            _line(
                x1=_LEFT,
                x2=_W - _RIGHT,
                y1=sy(tick),
                y2=sy(tick),
                stroke=_RULE,
                stroke_opacity="0.18",
            )
        )
        marks.append(
            _text(
                f"{tick:g}%" if y.percent else f"{tick:g}",
                x=_LEFT - 8,
                y=sy(tick) + 4,
                text_anchor="end",
                font_size=_FONT - 1,
                fill=_MUTED,
            )
        )
    for tick in x.ticks:
        marks.append(
            _text(
                f"{tick:g}%" if x.percent else f"{tick:g}",
                x=sx(tick),
                y=_H - _BOTTOM + 18,
                text_anchor="middle",
                font_size=_FONT - 1,
                fill=_MUTED,
            )
        )
    marks += [
        _line(
            x1=_LEFT,
            x2=_W - _RIGHT,
            y1=_H - _BOTTOM,
            y2=_H - _BOTTOM,
            stroke=_RULE,
            stroke_opacity="0.6",
        ),
        _line(
            x1=sx(x.cut),
            x2=sx(x.cut),
            y1=_TOP,
            y2=_H - _BOTTOM,
            stroke=_RULE,
            stroke_dasharray="4 4",
        ),
        _line(
            x1=_LEFT,
            x2=_W - _RIGHT,
            y1=sy(y.cut),
            y2=sy(y.cut),
            stroke=_RULE,
            stroke_dasharray="4 4",
        ),
    ]

    # Quadrant names in the corners.
    corner = {"font_size": _FONT - 1, "fill": _MUTED, "font_style": "italic"}
    top, bottom = _TOP + 14, _H - _BOTTOM - 8
    marks += [
        _text(quadrants[0], x=_LEFT + 8, y=top, **corner),
        _text(quadrants[1], x=_W - _RIGHT - 8, y=top, text_anchor="end", **corner),
        _text(quadrants[2], x=_LEFT + 8, y=bottom, **corner),
        _text(quadrants[3], x=_W - _RIGHT - 8, y=bottom, text_anchor="end", **corner),
    ]

    # Axis titles.
    marks += [
        _text(
            x.title,
            x=_LEFT + plot_w / 2,
            y=_H - 8,
            text_anchor="middle",
            font_size=_FONT,
            fill=_INK,
        ),
        # The y title sits above its axis, so it never meets the tick labels.
        _text(y.title + " ↑", x=_LEFT - 40, y=_TOP - 14, font_size=_FONT, fill=_INK),
    ]

    # Bubbles first (largest at the back), then their labels, placed so they meet
    # neither another label nor another bubble.
    order = sorted(range(len(points)), key=lambda i: -points[i][size_key])
    circles = {}
    for i, point in enumerate(points):
        cx, cy = sx(point[x.key]), sy(point[y.key])
        radius = 7 + 21 * math.sqrt(point[size_key] / biggest)
        circles[i] = (cx - radius, cy - radius, cx + radius, cy + radius)
    placed: list[tuple] = []
    labels: list[rx.Component] = []
    for i in order:
        point = points[i]
        cx, cy = sx(point[x.key]), sy(point[y.key])
        radius = 7 + 21 * math.sqrt(point[size_key] / biggest)
        color = _COLORS[i % len(_COLORS)]
        marks.append(
            _circle(
                cx=cx,
                cy=cy,
                r=radius,
                fill=color,
                fill_opacity="0.22",
                stroke=color,
                stroke_width="1.5",
            )
        )
        text = str(point[label_key])
        prefer = "left" if cx + radius + 6 + len(text) * _CHAR > _W - _RIGHT else "right"
        candidates = [
            (prefer, cy + 4),
            ("left" if prefer == "right" else "right", cy + 4),
            ("center", cy - radius - 5),
            ("center", cy + radius + 15),
            (prefer, cy - radius),
            (prefer, cy + radius + 8),
        ]
        side, ty = candidates[0]

        for side_try, y_try in candidates:
            tx_try = _anchor_x(side_try, cx, radius)
            box = _label_box(tx_try, y_try, text, side_try)
            inside = box[0] >= _LEFT and box[2] <= _W - _RIGHT
            obstacles = placed + [box_ for j, box_ in circles.items() if j != i]
            if inside and not any(_overlaps(box, other) for other in obstacles):
                side, ty = side_try, y_try
                break
        tx = _anchor_x(side, cx, radius)
        placed.append(_label_box(tx, ty, text, side))
        labels.append(
            _text(
                text,
                x=tx,
                y=ty,
                text_anchor={"right": "start", "left": "end", "center": "middle"}[side],
                font_size=_FONT,
                fill=_INK,
            )
        )

    return rx.el.figure(
        rx.el.figcaption(title, class_name="text-sm text-gray-800 mb-1"),
        rx.el.svg(
            rx.el.svg.title(title),
            rx.el.svg.desc(description),
            *marks,
            *labels,
            view_box=f"0 0 {_W} {_H}",
            width="100%",
            role="img",
            aria_label=title,
            class_name="block",
        ),
        rx.el.p(description, class_name="text-xs text-gray-600 mt-1"),
        id=chart_id,
        class_name="min-w-0",
    )
