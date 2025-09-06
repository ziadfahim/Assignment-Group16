import turtle

def draw_edge(length, depth):
    if depth == 0:
        turtle.forward(length)
    else:
        length /= 3.0
        draw_edge(length, depth - 1)
        turtle.right(60)      # flipped
        draw_edge(length, depth - 1)
        turtle.left(120)      # flipped
        draw_edge(length, depth - 1)
        turtle.right(60)      # flipped
        draw_edge(length, depth - 1)

def draw_pattern(sides, side_length, depth):
    angle = 360 / sides
    for _ in range(sides):
        draw_edge(side_length, depth)
        turtle.right(angle)   # clockwise polygon so “inside” is to the right

def main():
    turtle.speed(0)
    turtle.hideturtle()
    # optional: faster drawing
    try:
        turtle.tracer(False)
    except Exception:
        pass

    sides = int(input("Enter the number of sides: "))
    side_length = int(input("Enter the side length (pixels): "))
    depth = int(input("Enter the recursion depth: "))

    draw_pattern(sides, side_length, depth)

    try:
        turtle.update()
    except Exception:
        pass
    turtle.done()

if __name__ == "__main__":
    main()
