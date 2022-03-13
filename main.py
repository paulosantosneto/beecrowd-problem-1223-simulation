import os, pygame, time, math, pymunk
from diameter import *

def create_ball(space, radius, width, height):
    # body creation, state (dynamic) and collision
    body = pymunk.Body(1, radius, body_type = pymunk.Body.DYNAMIC)
    body.position = (width/2, 50)
    shape = pymunk.Circle(body, radius)
    space.add(body, shape)
    return shape

def draw_balls(ball, screen, radius):
    # drawing the circle/ball during the simulation
    pos_x = int(ball.body.position.x)
    pos_y = int(ball.body.position.y)
    pygame.draw.circle(screen, (238, 238, 238), (pos_x, pos_y), radius)

def static_lines(space, screen, coordinates):
    # adding the rods and lateral limits in the collision space
    shape = pymunk.Segment(space.static_body, coordinates[0], coordinates[1], 0)
    space.add(shape)
    return shape

def main():
    # basic pygame settings
    os.environ["SDL_VIDEO_CENTERED"]='1'
    pygame.init()
    width, height = 1920, 1080
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # receiving inputs: number of rods, width and height
    lines_number = int(input().strip())
    width_route, height_route = list(map(int, input().strip().split(" ")))

    # store, respectively, coordinates of lines, entries of each rod, display constant and state of x_initial (0 or width)
    lines_coordinates = []
    coord = []
    const = 1
    if width_route < 10:
        const = 40
    aux = 0

    for i in range(lines_number):
        coord_aux = []
        aux = width_route - aux
        y_i, x_f, y_f = list(map(float, input().strip().split(" ")))
        x_init = ((width_route*const) - (aux*const)) + ((width/2)-((width_route*const)/2))
        coord_aux.append(y_i)
        y_i = ((height_route*const)-(y_i*const))+(height/2)-((height_route*const)/2)
        coord_aux.append(x_f)
        x_f = (x_f*const)+((width/2)-((width_route*const)/2))
        coord_aux.append(y_f)
        y_f = ((height_route*const)-(y_f*const)) + ((height/2)-((height_route*const)/2))
        coord.append(coord_aux)
        lines_coordinates.append([(x_init, y_i), (x_f, y_f)])

    # call the function to calculate the ball's minimum diameter
    diameter = calculate_minimum_diameter(lines_number, width_route, height_route, coord)
    radius = diameter/2*const

    # pymunk settings
    space = pymunk.Space()
    space.gravity = (0, 200)
    # creates and adds the ball's body in the collision space
    ball = create_ball(space, int(radius), width, height)
    # adds circuit fins to the collision space
    lines = []
    for i in range(lines_number):
        lines.append(static_lines(space, screen, lines_coordinates[i]))

    # adds the lateral limits of the circuit to the collision space
    lines.append(static_lines(space, screen, [((width/2)-((width_route*const)/2), (height/2)+((height_route*const)/2)), ((width/2)-((width_route*const)/2), (height/2)-((height_route*const)/2))]))
    lines.append(static_lines(space, screen, [((width/2)+((width_route*const)/2), (height/2)+((height_route*const)/2)), ((width/2)+((width_route*const)/2), (height/2)-((height_route*const)/2))]))

    run = True

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        screen.fill((0, 0, 0))
        space.step(1/50)
        # draw the side limits of the circuit
        pygame.draw.lines(screen, [238, 238, 238], False, [((width/2)-((width_route*const)/2), (height/2)+((height_route*const)/2)), ((width/2)-((width_route*const)/2), (height/2)-((height_route*const)/2))]) # linha lateral esquerda
        pygame.draw.lines(screen, [238, 238, 238], False, [((width/2)+((width_route*const)/2), (height/2)+((height_route*const)/2)), ((width/2)+((width_route*const)/2), (height/2)-((height_route*const)/2))]) # linha lateral direita

        draw_balls(ball, screen, radius)
        # draw the lines
        for i in range(lines_number):
            pygame.draw.lines(screen, (238, 238, 238), False, lines_coordinates[i], 1)

        pygame.display.update()


if __name__ == '__main__':
    main()
