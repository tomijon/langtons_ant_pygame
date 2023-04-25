import pygame
import numpy
from enum import IntEnum


class Direction(IntEnum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def get_vector(direction):
        match direction:
            case Direction.UP:
                return (0, -1)
            case Direction.RIGHT:
                return (1, 0)
            case Direction.DOWN:
                return (0, 1)
            case Direction.LEFT:
                return (-1, 0)
        return None


    def rotate(direction, way):
        if way == RIGHT:
            return (direction % 4) + 1
        return ((direction - 2) % 4) + 1


# CONSTANTS
ON_COLOR = (0, 0, 0)
OFF_COLOR = (255, 255, 255)
BG_COLOR = (60, 60, 60)
SCALE = 8

ON = 1
LEFT = 1
RIGHT = 2
WIDTH = 100
HEIGHT = 100

# Automata variables
last_direction = LEFT
world = numpy.zeros((WIDTH, HEIGHT), dtype=int)
ant = (WIDTH // 2, HEIGHT//2)
ant_direction = Direction.RIGHT

# Init window
pygame.init()
window = pygame.display.set_mode(
    (WIDTH * SCALE, HEIGHT * SCALE),
    pygame.DOUBLEBUF)
window.fill(BG_COLOR)
pygame.display.update()

def render_world(world):
    world_render = pygame.Surface((WIDTH, HEIGHT))
    
    for x in range(WIDTH):
        for y in range(HEIGHT):
            world_render.set_at(
                (x, y),
                ON_COLOR if world[x, y] == ON else OFF_COLOR
                )
    return pygame.transform.scale_by(world_render, SCALE)


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return -1

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_event = pygame.event.Event(pygame.QUIT)
                pygame.event.post(quit_event)
    return 1


def update():
    global world
    global ant
    global ant_direction

    current = world[ant[0], ant[1]]

    # Change direciton of ant
    if current == ON:
        ant_direction = Direction.rotate(ant_direction, RIGHT)
        world[ant[0], ant[1]] = 0
    else:
        ant_direction = Direction.rotate(ant_direction, LEFT)
        world[ant[0], ant[1]] = ON

    dir_vec = Direction.get_vector(ant_direction)
    ant = (ant[0] + dir_vec[0], ant[1] + dir_vec[1])


# Main loop.
while True:
    if handle_events() == -1:
        break

    try:
        update()
    except:
        pass

    # Update render
    window.blit(render_world(world), (0, 0))
    pygame.display.update()

pygame.quit()
        
