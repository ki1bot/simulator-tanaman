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
    SELECTED_BORDER,
    SOIL_INNER,
    SOIL_LINE,
    SOIL_OUTER,
    WATER_BLUE,
)


def plot_bounds(position):
    row = (
        position - 1
    ) // GRID_COLS

    col = (
        position - 1
    ) % GRID_COLS

    x1 = (
        CANVAS_MARGIN
        + col
        * (
            CELL_SIZE
            + CELL_GAP
        )
    )

    y1 = (
        CANVAS_MARGIN
        + row
        * (
            CELL_SIZE
            + CELL_GAP
        )
    )

    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE

    return x1, y1, x2, y2


def pixel_to_plot(x, y):
    total = (
        GRID_ROWS
        * GRID_COLS
    )

    for position in range(
        1,
        total + 1,
    ):
        x1, y1, x2, y2 = (
            plot_bounds(position)
        )

        if (
            x1 <= x <= x2
            and y1 <= y <= y2
        ):
            return position

    return None


def draw_garden(
    canvas,
    garden,
    selected_plot=None,
):
    canvas.delete("all")

    canvas.create_rectangle(
        0,
        0,
        CANVAS_WIDTH,
        CANVAS_HEIGHT,
        fill="#f8f2e8",
        outline="",
    )

    draw_watering_can(canvas)
    draw_shovel(canvas)

    for plot in garden.plots:
        draw_plot(
            canvas,
            plot,
            selected=(
                plot.position
                == selected_plot
            ),
        )


def draw_watering_can(canvas):
    x = 42
    y = CANVAS_HEIGHT - 38

    canvas.create_oval(
        x - 14,
        y - 22,
        x + 20,
        y + 10,
        fill="#9cab86",
        outline="#69795d",
        width=2,
    )

    canvas.create_arc(
        x - 24,
        y - 22,
        x + 6,
        y + 10,
        start=25,
        extent=250,
        style="arc",
        outline="#69795d",
        width=3,
    )

    canvas.create_polygon(
        x + 16,
        y - 10,
        x + 46,
        y - 3,
        x + 36,
        y + 7,
        x + 12,
        y + 1,
        fill="#9cab86",
        outline="#69795d",
        width=2,
    )

    canvas.create_line(
        x + 41,
        y + 1,
        x + 54,
        y - 7,
        fill="#69795d",
        width=2,
    )


def draw_shovel(canvas):
    x = CANVAS_WIDTH - 58
    y = 118

    canvas.create_line(
        x,
        y,
        x + 24,
        y - 24,
        fill="#9a673e",
        width=6,
    )

    canvas.create_oval(
        x + 20,
        y - 29,
        x + 35,
        y - 14,
        fill="#a97243",
        outline="#81532f",
        width=2,
    )

    canvas.create_polygon(
        x - 12,
        y + 6,
        x + 1,
        y - 9,
        x + 16,
        y + 4,
        x + 2,
        y + 19,
        fill="#b8b8b8",
        outline="#858585",
        width=2,
    )


def draw_plot(
    canvas,
    plot,
    selected=False,
):
    x1, y1, x2, y2 = (
        plot_bounds(
            plot.position
        )
    )

    canvas.create_rectangle(
        x1 + 4,
        y1 + 5,
        x2 + 4,
        y2 + 5,
        fill=GRID_SHADOW,
        outline="",
    )

    canvas.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        fill=SOIL_OUTER,
        outline=(
            SELECTED_BORDER
            if selected
            else GRID_BORDER
        ),
        width=(
            4
            if selected
            else 2
        ),
    )

    pad = 9

    canvas.create_rectangle(
        x1 + pad,
        y1 + pad,
        x2 - pad,
        y2 - pad,
        fill=SOIL_INNER,
        outline="",
    )

    if plot.plant is None:
        draw_empty_soil(
            canvas,
            x1 + pad,
            y1 + pad,
            x2 - pad,
            y2 - pad,
        )
    else:
        draw_plant(
            canvas,
            plot.plant,
            x1 + pad,
            y1 + pad,
            x2 - pad,
            y2 - pad,
        )

    canvas.create_oval(
        x1 + 5,
        y1 + 5,
        x1 + 26,
        y1 + 26,
        fill="#fff4dc",
        outline="",
    )

    canvas.create_text(
        x1 + 15.5,
        y1 + 15.5,
        text=str(
            plot.position
        ),
        fill="#725333",
        font=(
            "Arial",
            9,
            "bold",
        ),
    )


def draw_empty_soil(
    canvas,
    x1,
    y1,
    x2,
    y2,
):
    canvas.create_line(
        x1 + 14,
        y2 - 26,
        x2 - 14,
        y2 - 23,
        fill=SOIL_LINE,
        width=3,
        smooth=True,
    )

    canvas.create_line(
        x1 + 17,
        y2 - 43,
        x2 - 18,
        y2 - 40,
        fill=SOIL_LINE,
        width=3,
        smooth=True,
    )

    canvas.create_line(
        x1 + 20,
        y2 - 60,
        x2 - 20,
        y2 - 57,
        fill=SOIL_LINE,
        width=3,
        smooth=True,
    )


def draw_plant(
    canvas,
    plant,
    x1,
    y1,
    x2,
    y2,
):
    if plant.is_dead:
        draw_dead_plant(
            canvas,
            x1,
            y1,
            x2,
            y2,
        )

    elif plant.stage_level == 0:
        draw_sprout(
            canvas,
            plant,
            x1,
            y1,
            x2,
            y2,
        )

    elif plant.stage_level == 1:
        draw_small_plant(
            canvas,
            plant,
            x1,
            y1,
            x2,
            y2,
        )

    elif plant.stage_level == 2:
        draw_medium_plant(
            canvas,
            plant,
            x1,
            y1,
            x2,
            y2,
        )

    else:
        draw_mature_plant(
            canvas,
            plant,
            x1,
            y1,
            x2,
            y2,
        )

    draw_status(
        canvas,
        plant,
        x1,
        y1,
        x2,
        y2,
    )


def draw_status(
    canvas,
    plant,
    x1,
    y1,
    x2,
    y2,
):
    if plant.watered_today:
        x = x2 - 14
        y = y1 + 16

        canvas.create_oval(
            x - 5,
            y,
            x + 5,
            y + 10,
            fill=WATER_BLUE,
            outline="",
        )

        canvas.create_polygon(
            x,
            y - 8,
            x - 5,
            y + 2,
            x + 5,
            y + 2,
            fill=WATER_BLUE,
            outline="",
        )

    if plant.cared_today:
        x = x1 + 16
        y = y1 + 16

        canvas.create_line(
            x - 5,
            y,
            x + 5,
            y,
            fill="#f3c85d",
            width=2,
        )

        canvas.create_line(
            x,
            y - 5,
            x,
            y + 5,
            fill="#f3c85d",
            width=2,
        )

        canvas.create_line(
            x - 4,
            y - 4,
            x + 4,
            y + 4,
            fill="#f3c85d",
            width=2,
        )

        canvas.create_line(
            x - 4,
            y + 4,
            x + 4,
            y - 4,
            fill="#f3c85d",
            width=2,
        )


def draw_sprout(
    canvas,
    plant,
    x1,
    y1,
    x2,
    y2,
):
    cx = (
        x1 + x2
    ) / 2

    base = y2 - 14
    top = y2 - 40

    canvas.create_line(
        cx,
        base,
        cx,
        top,
        fill="#5d873e",
        width=3,
    )

    canvas.create_oval(
        cx - 15,
        top - 7,
        cx - 1,
        top + 7,
        fill=plant.leaf_color,
        outline="",
    )

    canvas.create_oval(
        cx + 1,
        top - 7,
        cx + 15,
        top + 7,
        fill=plant.leaf_color,
        outline="",
    )


def draw_small_plant(
    canvas,
    plant,
    x1,
    y1,
    x2,
    y2,
):
    cx = (
        x1 + x2
    ) / 2

    base = y2 - 14

    canvas.create_line(
        cx,
        base,
        cx,
        y2 - 56,
        fill="#5d873e",
        width=4,
    )

    leaves = (
        (
            cx - 24,
            y2 - 67,
            cx - 2,
            y2 - 47,
        ),
        (
            cx + 2,
            y2 - 67,
            cx + 24,
            y2 - 47,
        ),
        (
            cx - 28,
            y2 - 47,
            cx - 8,
            y2 - 28,
        ),
        (
            cx + 8,
            y2 - 47,
            cx + 28,
            y2 - 28,
        ),
    )

    for leaf in leaves:
        canvas.create_oval(
            *leaf,
            fill=plant.leaf_color,
            outline="",
        )


def draw_medium_plant(
    canvas,
    plant,
    x1,
    y1,
    x2,
    y2,
):
    cx = (
        x1 + x2
    ) / 2

    base = y2 - 14

    canvas.create_line(
        cx,
        base,
        cx,
        y2 - 70,
        fill="#5d873e",
        width=4,
    )

    leaves = (
        (
            cx - 31,
            y2 - 76,
            cx - 7,
            y2 - 52,
        ),
        (
            cx + 7,
            y2 - 76,
            cx + 31,
            y2 - 52,
        ),
        (
            cx - 35,
            y2 - 53,
            cx - 11,
            y2 - 29,
        ),
        (
            cx + 11,
            y2 - 53,
            cx + 35,
            y2 - 29,
        ),
        (
            cx - 16,
            y2 - 90,
            cx + 4,
            y2 - 67,
        ),
        (
            cx - 4,
            y2 - 90,
            cx + 16,
            y2 - 67,
        ),
    )

    for leaf in leaves:
        canvas.create_oval(
            *leaf,
            fill=plant.leaf_color,
            outline="",
        )


def draw_mature_plant(
    canvas,
    plant,
    x1,
    y1,
    x2,
    y2,
):
    if plant.kind == "tomat":
        draw_tomato(
            canvas,
            plant,
            x1,
            y1,
            x2,
            y2,
        )

    elif plant.kind == "wortel":
        draw_carrot(
            canvas,
            plant,
            x1,
            y1,
            x2,
            y2,
        )

    elif plant.kind == "stroberi":
        draw_strawberry(
            canvas,
            plant,
            x1,
            y1,
            x2,
            y2,
        )

    else:
        draw_sunflower(
            canvas,
            plant,
            x1,
            y1,
            x2,
            y2,
        )


def draw_tomato(
    canvas,
    plant,
    x1,
    y1,
    x2,
    y2,
):
    draw_medium_plant(
        canvas,
        plant,
        x1,
        y1,
        x2,
        y2,
    )

    cx = (
        x1 + x2
    ) / 2

    fruits = (
        (
            cx - 25,
            y2 - 28,
            cx - 5,
            y2 - 8,
        ),
        (
            cx + 5,
            y2 - 28,
            cx + 25,
            y2 - 8,
        ),
        (
            cx - 10,
            y2 - 18,
            cx + 10,
            y2 + 1,
        ),
    )

    for fruit in fruits:
        canvas.create_oval(
            *fruit,
            fill=plant.fruit_color,
            outline="#bf5726",
            width=2,
        )


def draw_carrot(
    canvas,
    plant,
    x1,
    y1,
    x2,
    y2,
):
    cx = (
        x1 + x2
    ) / 2

    base = y2 - 14

    for offset in (
        -17,
        0,
        17,
    ):
        canvas.create_line(
            cx + offset,
            base - 15,
            cx + offset,
            y2 - 75,
            fill="#5d873e",
            width=4,
        )

        canvas.create_oval(
            cx + offset - 15,
            y2 - 86,
            cx + offset + 2,
            y2 - 66,
            fill=plant.leaf_color,
            outline="",
        )

        canvas.create_oval(
            cx + offset - 2,
            y2 - 87,
            cx + offset + 15,
            y2 - 67,
            fill=plant.leaf_color,
            outline="",
        )

        canvas.create_polygon(
            cx + offset,
            base,
            cx + offset - 9,
            base - 27,
            cx + offset + 9,
            base - 27,
            fill=plant.fruit_color,
            outline="#ca6823",
            width=2,
        )


def draw_strawberry(
    canvas,
    plant,
    x1,
    y1,
    x2,
    y2,
):
    draw_medium_plant(
        canvas,
        plant,
        x1,
        y1,
        x2,
        y2,
    )

    cx = (
        x1 + x2
    ) / 2

    fruits = (
        (
            cx - 22,
            y2 - 24,
        ),
        (
            cx + 20,
            y2 - 22,
        ),
        (
            cx,
            y2 - 10,
        ),
    )

    for fx, fy in fruits:
        canvas.create_polygon(
            fx,
            fy + 14,
            fx - 10,
            fy - 5,
            fx + 10,
            fy - 5,
            fill=plant.fruit_color,
            outline="#a92e37",
            width=2,
        )


def draw_sunflower(
    canvas,
    plant,
    x1,
    y1,
    x2,
    y2,
):
    cx = (
        x1 + x2
    ) / 2

    base = y2 - 14
    flower_y = y2 - 82

    canvas.create_line(
        cx,
        base,
        cx,
        flower_y + 10,
        fill="#5d873e",
        width=5,
    )

    canvas.create_oval(
        cx - 31,
        y2 - 58,
        cx - 6,
        y2 - 34,
        fill=plant.leaf_color,
        outline="",
    )

    canvas.create_oval(
        cx + 6,
        y2 - 58,
        cx + 31,
        y2 - 34,
        fill=plant.leaf_color,
        outline="",
    )

    petals = (
        (
            cx,
            flower_y - 19,
        ),
        (
            cx + 16,
            flower_y - 12,
        ),
        (
            cx + 22,
            flower_y + 3,
        ),
        (
            cx + 15,
            flower_y + 17,
        ),
        (
            cx,
            flower_y + 22,
        ),
        (
            cx - 15,
            flower_y + 17,
        ),
        (
            cx - 22,
            flower_y + 3,
        ),
        (
            cx - 16,
            flower_y - 12,
        ),
    )

    for px, py in petals:
        canvas.create_oval(
            px - 9,
            py - 9,
            px + 9,
            py + 9,
            fill=plant.fruit_color,
            outline="",
        )

    canvas.create_oval(
        cx - 15,
        flower_y - 15,
        cx + 15,
        flower_y + 15,
        fill="#6d4a28",
        outline="#54381e",
        width=2,
    )


def draw_dead_plant(
    canvas,
    x1,
    y1,
    x2,
    y2,
):
    cx = (
        x1 + x2
    ) / 2

    base = y2 - 14

    canvas.create_line(
        cx,
        base,
        cx - 15,
        y2 - 53,
        fill="#8d7552",
        width=4,
    )

    canvas.create_oval(
        cx - 30,
        y2 - 58,
        cx - 10,
        y2 - 41,
        fill="#99865f",
        outline="",
    )

    canvas.create_oval(
        cx - 9,
        y2 - 70,
        cx + 10,
        y2 - 52,
        fill="#99865f",
        outline="",
    )

    canvas.create_line(
        cx - 24,
        y2 - 28,
        cx + 8,
        y2 - 58,
        fill="#8d7552",
        width=3,
    )