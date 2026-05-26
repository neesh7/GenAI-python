import turtle


def draw_circle(pen, x, y, radius, color):
    """Draw a filled circle centered at (x, y)."""
    pen.penup()
    pen.goto(x, y - radius)
    pen.setheading(0)
    pen.pendown()
    pen.fillcolor(color)
    pen.begin_fill()
    pen.circle(radius)
    pen.end_fill()


def draw_eye(pen, x, y):
    """Draw a big concentric owl eye centered at (x, y)."""
    draw_circle(pen, x, y, 26, "white")        # eye socket
    draw_circle(pen, x, y, 18, "#FFB300")      # golden iris
    draw_circle(pen, x, y, 9, "black")         # pupil
    draw_circle(pen, x - 3, y + 4, 3, "white")  # glint


def draw_wing(pen, x, y, heading, color, mirror=False):
    """Draw a curved feather-style wing as a closed leaf shape."""
    pen.penup()
    pen.goto(x, y)
    pen.setheading(heading)
    pen.pendown()
    pen.fillcolor(color)
    pen.begin_fill()
    radius = 95
    extent = 70
    if not mirror:
        pen.circle(radius, extent)
        pen.left(180 - extent)
        pen.circle(radius, extent)
        pen.left(180 - extent)
    else:
        pen.circle(-radius, extent)
        pen.right(180 - extent)
        pen.circle(-radius, extent)
        pen.right(180 - extent)
    pen.end_fill()


def draw_foot(pen, x, y):
    """Draw a three-toed foot starting at (x, y)."""
    pen.pensize(4)
    pen.pencolor("#E8820C")
    for angle in (250, 270, 290):
        pen.penup()
        pen.goto(x, y)
        pen.setheading(angle)
        pen.pendown()
        pen.forward(16)
    pen.pensize(1)


def draw_owl():
    """Draw an owl using turtle graphics."""
    screen = turtle.Screen()
    screen.setup(width=800, height=700)
    screen.bgcolor("#BfE3F0")
    screen.title("Owl")

    pen = turtle.Turtle()
    pen.speed(0)
    pen.pensize(1)
    screen.tracer(0)  # draw instantly, update once at the end

    # Body
    draw_circle(pen, 0, -60, 95, "#7A5230")
    # Belly (lighter front patch)
    draw_circle(pen, 0, -75, 60, "#C9A36B")

    # Wings hugging the sides of the body
    draw_wing(pen, -38, 25, 205, "#5C3A1E")           # left wing
    draw_wing(pen, 38, 25, 335, "#5C3A1E", mirror=True)  # right wing

    # Head
    draw_circle(pen, 0, 95, 62, "#8A5E36")

    # Ear tufts
    pen.penup()
    pen.goto(-50, 135)
    pen.setheading(0)
    pen.pendown()
    pen.fillcolor("#8A5E36")
    pen.begin_fill()
    pen.goto(-28, 180)
    pen.goto(-18, 135)
    pen.goto(-50, 135)
    pen.end_fill()

    pen.penup()
    pen.goto(50, 135)
    pen.pendown()
    pen.begin_fill()
    pen.goto(28, 180)
    pen.goto(18, 135)
    pen.goto(50, 135)
    pen.end_fill()

    # Eyes
    draw_eye(pen, -28, 105)
    draw_eye(pen, 28, 105)

    # Beak (downward triangle between the eyes)
    pen.penup()
    pen.goto(-10, 90)
    pen.setheading(0)
    pen.pendown()
    pen.fillcolor("#E8820C")
    pen.begin_fill()
    pen.goto(10, 90)
    pen.goto(0, 68)
    pen.goto(-10, 90)
    pen.end_fill()

    # Feet
    draw_foot(pen, -28, -150)
    draw_foot(pen, 28, -150)

    # Title
    pen.penup()
    pen.goto(0, -250)
    pen.pendown()
    pen.pencolor("black")
    pen.write("Owl", align="center", font=("Arial", 24, "bold"))

    pen.hideturtle()
    screen.update()
    screen.mainloop()


if __name__ == "__main__":
    draw_owl()
