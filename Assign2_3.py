import turtle

def draw_edge(length, depth):
    """Recursive function"""
    if depth == 0:
        turtle.forward(length)
    else:
        length /= 3.0
        draw_edge(length, depth - 1)
        turtle.right(60)
        draw_edge(length, depth - 1)
        turtle.left(120)
        draw_edge(length, depth - 1)
        turtle.right(60)
        draw_edge(length, depth - 1)

def draw_pattern(sides, side_length, depth):
    angle = 360 / sides
    for _ in range(sides):
        draw_edge(side_length, depth)
        turtle.right(angle)   # clockwise polygon so “inside” is to the right