from constants import (
    CANVAS_HEIGHT,
    CANVAS_MARGIN,
    CANVAS_WIDTH,
    CELL_GAP,
    CELL_SIZE,
    GRID_BORDER,
    GRID_COLS,
    GRID_ROWS,
    GRID_SHADOW,
    HIGHLIGHT,
    SELECTED_BORDER,
    SOIL_INNER,
    SOIL_LINE,
    SOIL_OUTER,
)


def plot_bounds(position):
    row = (position - 1) // GRID_COLS
    col = (position - 1) % GRID_COLS

    x1 = CANVAS_MARGIN + col * (CELL_SIZE + CELL_GAP)
    y1 = CANVAS_MARGIN + row * (CELL_SIZE + CELL_GAP)
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE

    return x1, y1, x2, y2


def pixel_to_plot(x, y):
    for position in range(1, GRID_ROWS * GRID_COLS + 1):
        x1, y1, x2, y2 = plot_bounds(position)
        if x1 <= x <= x2 and y1 <= y <= y2:
            return position
    return None


def draw_garden(canvas, garden, selected_plot=None):
    canvas.delete("all")

    canvas.create_rectangle(
        0,
        0,
        CANVAS_WIDTH,
        CANVAS_HEIGHT,
        fill="#f7f1e8",
        outline="",
    )

    draw_decorations(canvas)

    for plot in garden.plots:
        draw_plot(canvas, plot, plot.position == selected_plot)


def draw_decorations(canvas):
    # Penyiram kiri bawah
    base_x = 54
    base_y = CANVAS_HEIGHT - 48

    canvas.create_oval(base_x - 18, base_y - 20, base_x + 18, base_y + 12,
                       fill="#9bb089", outline="#6f7f62", width=2)
    canvas.create_arc(base_x - 24, base_y - 20, base_x + 8, base_y + 8,
                      start=30, extent=240, style="arc",
                      outline="#6f7f62", width=3)
    canvas.create_polygon(
        base_x + 16, base_y - 8,
        base_x + 44, base_y - 2,
        base_x + 34, base_y + 8,
        base_x + 12, base_y + 2,
        fill="#9bb089",
        outline="#6f7f62",
        width=2,
    )
    canvas.create_line(base_x + 40, base_y + 1, base_x + 55, base_y - 8,
                       fill="#6f7f62", width=2)

    # Sekop kanan atas
    sx = CANVAS_WIDTH - 70
    sy = 175

    canvas.create_line(sx, sy, sx + 28, sy - 28, fill="#9e6a3f", width=6)
    canvas.create_oval(sx + 24, sy - 32, sx + 40, sy - 16,
                       fill="#9e6a3f", outline="#8a5730", width=2)
    canvas.create_polygon(
        sx - 12, sy + 6,
        sx + 2, sy - 10,
        sx + 18, sy + 4,
        sx + 2, sy + 20,
        fill="#b9b9b9",
        outline="#8f8f8f",
        width=2,
    )


def draw_plot(canvas, plot, selected=False):
    x1, y1, x2, y2 = plot_bounds(plot.position)

    canvas.create_rectangle(
        x1 + 4,
        y1 + 6,
        x2 + 4,
        y2 + 6,
        fill=GRID_SHADOW,
        outline="",
    )

    border_color = SELECTED_BORDER if selected else GRID_BORDER
    border_width = 4 if selected else 3

    canvas.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        fill=SOIL_OUTER,
        outline=border_color,
        width=border_width,
    )

    inner_pad = 10
    canvas.create_rectangle(
        x1 + inner_pad,
        y1 + inner_pad,
        x2 - inner_pad,
        y2 - inner_pad,
        fill=SOIL_INNER,
        outline="",
    )

    if plot.plant is None:
        draw_empty_soil(canvas, x1 + inner_pad, y1 + inner_pad, x2 - inner_pad, y2 - inner_pad)
    else:
        draw_plant(canvas, plot.plant, x1 + inner_pad, y1 + inner_pad, x2 - inner_pad, y2 - inner_pad)

    canvas.create_oval(x1 + 6, y1 + 6, x1 + 28, y1 + 28, fill="#fff4dd", outline="")
    canvas.create_text(x1 + 17, y1 + 17, text=str(plot.position), fill="#7a5b39", font=("Arial", 10, "bold"))


def draw_empty_soil(canvas, x1, y1, x2, y2):
    mid_x = (x1 + x2) / 2
    canvas.create_line(x1 + 16, y2 - 30, x2 - 16, y2 - 26, fill=SOIL_LINE, width=3, smooth=True)
    canvas.create_line(x1 + 18, y2 - 48, x2 - 18, y2 - 44, fill=SOIL_LINE, width=3, smooth=True)
    canvas.create_line(x1 + 20, y2 - 66, x2 - 20, y2 - 62, fill=SOIL_LINE, width=3, smooth=True)
    canvas.create_line(mid_x - 20, y2 - 16, mid_x + 20, y2 - 14, fill="#a36d3d", width=2, smooth=True)


def draw_plant(canvas, plant, x1, y1, x2, y2):
    if plant.is_dead:
        draw_dead_plant(canvas, x1, y1, x2, y2)
        draw_status_icons(canvas, plant, x1, y1, x2, y2)
        return

    stage = plant.stage_level

    if stage == 0:
        draw_sprout(canvas, plant, x1, y1, x2, y2)
    elif stage == 1:
        draw_small_plant(canvas, plant, x1, y1, x2, y2)
    elif stage == 2:
        draw_mid_plant(canvas, plant, x1, y1, x2, y2)
    else:
        draw_mature_plant(canvas, plant, x1, y1, x2, y2)

    draw_status_icons(canvas, plant, x1, y1, x2, y2)


def draw_status_icons(canvas, plant, x1, y1, x2, y2):
    if plant.watered_today:
        drop_x = x2 - 18
        drop_y = y1 + 18
        canvas.create_oval(drop_x - 6, drop_y - 2, drop_x + 6, drop_y + 10, fill="#72bce8", outline="")
        canvas.create_polygon(drop_x, drop_y - 10, drop_x - 6, drop_y + 1, drop_x + 6, drop_y + 1,
                              fill="#72bce8", outline="")

    if plant.cared_today:
        sx = x1 + 18
        sy = y1 + 18
        canvas.create_line(sx - 5, sy, sx + 5, sy, fill=HIGHLIGHT, width=2)
        canvas.create_line(sx, sy - 5, sx, sy + 5, fill=HIGHLIGHT, width=2)
        canvas.create_line(sx - 4, sy - 4, sx + 4, sy + 4, fill=HIGHLIGHT, width=2)
        canvas.create_line(sx - 4, sy + 4, sx + 4, sy - 4, fill=HIGHLIGHT, width=2)


def draw_sprout(canvas, plant, x1, y1, x2, y2):
    cx = (x1 + x2) / 2
    base_y = y2 - 18
    stem_top = y2 - 42

    canvas.create_line(cx, base_y, cx, stem_top, fill="#5f8a3d", width=3)
    canvas.create_oval(cx - 16, stem_top - 8, cx - 2, stem_top + 6,
                       fill=plant.leaf_color, outline="")
    canvas.create_oval(cx + 2, stem_top - 8, cx + 16, stem_top + 6,
                       fill=plant.leaf_color, outline="")


def draw_small_plant(canvas, plant, x1, y1, x2, y2):
    cx = (x1 + x2) / 2
    base_y = y2 - 18

    canvas.create_line(cx, base_y, cx, y2 - 60, fill="#5f8a3d", width=4)
    canvas.create_oval(cx - 26, y2 - 74, cx - 2, y2 - 50,
                       fill=plant.leaf_color, outline="")
    canvas.create_oval(cx + 2, y2 - 74, cx + 26, y2 - 50,
                       fill=plant.leaf_color, outline="")
    canvas.create_oval(cx - 30, y2 - 50, cx - 8, y2 - 30,
                       fill=plant.leaf_color, outline="")
    canvas.create_oval(cx + 8, y2 - 50, cx + 30, y2 - 30,
                       fill=plant.leaf_color, outline="")


def draw_mid_plant(canvas, plant, x1, y1, x2, y2):
    cx = (x1 + x2) / 2
    base_y = y2 - 18

    canvas.create_line(cx, base_y, cx, y2 - 78, fill="#5f8a3d", width=5)

    leaves = [
        (cx - 34, y2 - 82, cx - 6, y2 - 54),
        (cx + 6, y2 - 82, cx + 34, y2 - 54),
        (cx - 40, y2 - 58, cx - 12, y2 - 28),
        (cx + 12, y2 - 58, cx + 40, y2 - 28),
        (cx - 20, y2 - 98, cx + 6, y2 - 70),
        (cx - 6, y2 - 98, cx + 20, y2 - 70),
    ]

    for lx1, ly1, lx2, ly2 in leaves:
        canvas.create_oval(lx1, ly1, lx2, ly2, fill=plant.leaf_color, outline="")


def draw_mature_plant(canvas, plant, x1, y1, x2, y2):
    kind = plant.kind

    if kind == "tomat":
        draw_mature_tomato(canvas, plant, x1, y1, x2, y2)
    elif kind == "wortel":
        draw_mature_carrot(canvas, plant, x1, y1, x2, y2)
    elif kind == "stroberi":
        draw_mature_strawberry(canvas, plant, x1, y1, x2, y2)
    elif kind == "bunga_matahari":
        draw_mature_sunflower(canvas, plant, x1, y1, x2, y2)
    else:
        draw_mid_plant(canvas, plant, x1, y1, x2, y2)


def draw_mature_tomato(canvas, plant, x1, y1, x2, y2):
    cx = (x1 + x2) / 2
    base_y = y2 - 18

    canvas.create_line(cx, base_y, cx, y2 - 86, fill="#5f8a3d", width=5)

    leaves = [
        (cx - 38, y2 - 90, cx - 10, y2 - 62),
        (cx + 10, y2 - 90, cx + 38, y2 - 62),
        (cx - 42, y2 - 60, cx - 14, y2 - 32),
        (cx + 14, y2 - 60, cx + 42, y2 - 32),
        (cx - 18, y2 - 102, cx + 8, y2 - 74),
        (cx - 8, y2 - 102, cx + 18, y2 - 74),
    ]

    for leaf in leaves:
        canvas.create_oval(*leaf, fill=plant.leaf_color, outline="")

    fruits = [
        (cx - 28, y2 - 30, cx - 4, y2 - 6),
        (cx + 4, y2 - 30, cx + 28, y2 - 6),
        (cx - 12, y2 - 18, cx + 12, y2 + 4),
    ]

    for fx1, fy1, fx2, fy2 in fruits:
        canvas.create_oval(fx1, fy1, fx2, fy2, fill=plant.fruit_color, outline="#c85f28", width=2)
        mx = (fx1 + fx2) / 2
        canvas.create_line(mx, fy1 + 2, mx - 5, fy1 - 6, fill="#5f8a3d", width=2)
        canvas.create_line(mx, fy1 + 2, mx + 5, fy1 - 6, fill="#5f8a3d", width=2)


def draw_mature_carrot(canvas, plant, x1, y1, x2, y2):
    cx = (x1 + x2) / 2
    base_y = y2 - 18

    for offset in (-18, 0, 18):
        canvas.create_line(cx + offset, base_y - 16, cx + offset, y2 - 86, fill="#5f8a3d", width=4)
        canvas.create_oval(cx + offset - 18, y2 - 96, cx + offset + 2, y2 - 72,
                           fill=plant.leaf_color, outline="")
        canvas.create_oval(cx + offset - 2, y2 - 98, cx + offset + 18, y2 - 74,
                           fill=plant.leaf_color, outline="")
        canvas.create_polygon(
            cx + offset, base_y - 4,
            cx + offset - 10, base_y - 34,
            cx + offset + 10, base_y - 34,
            fill=plant.fruit_color,
            outline="#d46d20",
            width=2,
        )


def draw_mature_strawberry(canvas, plant, x1, y1, x2, y2):
    cx = (x1 + x2) / 2
    base_y = y2 - 20

    canvas.create_line(cx, base_y, cx, y2 - 82, fill="#5f8a3d", width=4)

    leaves = [
        (cx - 36, y2 - 86, cx - 8, y2 - 58),
        (cx + 8, y2 - 86, cx + 36, y2 - 58),
        (cx - 42, y2 - 58, cx - 12, y2 - 28),
        (cx + 12, y2 - 58, cx + 42, y2 - 28),
        (cx - 12, y2 - 104, cx + 12, y2 - 78),
    ]

    for leaf in leaves:
        canvas.create_oval(*leaf, fill=plant.leaf_color, outline="")

    fruits = [
        (cx - 26, y2 - 30),
        (cx + 18, y2 - 26),
        (cx, y2 - 12),
    ]

    for fx, fy in fruits:
        canvas.create_polygon(
            fx, fy + 16,
            fx - 12, fy - 6,
            fx + 12, fy - 6,
            fill=plant.fruit_color,
            outline="#a82b35",
            width=2,
        )
        canvas.create_arc(fx - 10, fy - 12, fx + 10, fy + 4,
                          start=0, extent=180, style="arc",
                          outline="#5f8a3d", width=2)

    # bunga kecil
    canvas.create_oval(cx - 6, y2 - 72, cx + 6, y2 - 60, fill="#f7d96d", outline="")
    for dx, dy in [(-10, -4), (10, -4), (0, -12), (-8, 8), (8, 8)]:
        canvas.create_oval(cx + dx - 5, y2 - 66 + dy - 5, cx + dx + 5, y2 - 66 + dy + 5,
                           fill="white", outline="")


def draw_mature_sunflower(canvas, plant, x1, y1, x2, y2):
    cx = (x1 + x2) / 2
    base_y = y2 - 18
    top_y = y2 - 98

    canvas.create_line(cx, base_y, cx, top_y + 12, fill="#5f8a3d", width=5)
    canvas.create_oval(cx - 34, top_y - 10, cx - 8, top_y + 16, fill=plant.leaf_color, outline="")
    canvas.create_oval(cx + 8, top_y - 10, cx + 34, top_y + 16, fill=plant.leaf_color, outline="")
    canvas.create_oval(cx - 42, top_y + 18, cx - 14, top_y + 46, fill=plant.leaf_color, outline="")
    canvas.create_oval(cx + 14, top_y + 18, cx + 42, top_y + 46, fill=plant.leaf_color, outline="")

    # kelopak
    for px, py in [
        (cx, top_y - 22),
        (cx + 18, top_y - 14),
        (cx + 26, top_y + 2),
        (cx + 18, top_y + 18),
        (cx, top_y + 26),
        (cx - 18, top_y + 18),
        (cx - 26, top_y + 2),
        (cx - 18, top_y - 14),
    ]:
        canvas.create_oval(px - 10, py - 10, px + 10, py + 10, fill=plant.fruit_color, outline="")

    canvas.create_oval(cx - 18, top_y - 18, cx + 18, top_y + 18, fill="#6b4b2a", outline="#54381d", width=2)


def draw_dead_plant(canvas, x1, y1, x2, y2):
    cx = (x1 + x2) / 2
    base_y = y2 - 18

    canvas.create_line(cx, base_y, cx - 18, y2 - 56, fill="#8a6f48", width=4)
    canvas.create_oval(cx - 34, y2 - 60, cx - 10, y2 - 42, fill="#9e8a60", outline="")
    canvas.create_oval(cx - 10, y2 - 74, cx + 12, y2 - 56, fill="#9e8a60", outline="")
    canvas.create_line(cx - 24, y2 - 30, cx + 10, y2 - 60, fill="#9e8a60", width=3)
    canvas.create_line(cx - 24, y2 - 60, cx + 10, y2 - 30, fill="#9e8a60", width=3)