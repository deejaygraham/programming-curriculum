# https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

import sys
import random

from microbit import *

# Population refresh rate
refresh_rate_in_ms = 1000

# board dimensions
width, height = 5, 5

# likelihood that a cell will be alive when randomly initialised
random_population_pc = 50

# cell states
dead_cell = 0 # debug set to 2 to see all dimly lit.
live_cell = 8

# is this x, y location on the board?
def is_legal_location(x, y):
    return (0 <= x < width) and (0 <= y < height)

# ugly but works with microbit
def count_live_neighbours(x, y, population):
    live_neighbours = 0
    # to the left...
    if is_legal_location(x - 1, y - 1):
        if population[x - 1][y - 1] == live_cell:
            live_neighbours += 1

    if is_legal_location(x - 1, y):
        if population[x - 1][y] == live_cell:
            live_neighbours += 1

    if is_legal_location(x - 1, y + 1):
        if population[x - 1][y + 1] == live_cell:
            live_neighbours += 1

    # above
    if is_legal_location(x, y - 1):
        if population[x][y - 1] == live_cell:
            live_neighbours += 1

    # below
    if is_legal_location(x, y + 1):
        if population[x][y + 1] == live_cell:
            live_neighbours += 1

    # to the right...
    if is_legal_location(x + 1, y - 1):
        if population[x + 1][y - 1] == live_cell:
            live_neighbours += 1

    if is_legal_location(x + 1, y):
        if population[x + 1][y] == live_cell:
            live_neighbours += 1

    if is_legal_location(x + 1, y + 1):
        if population[x + 1][y + 1] == live_cell:
            live_neighbours += 1

    return live_neighbours

# run through the survivors, births and deaths
def create_next_generation(population):
    next_generation = empty_population()

    for x in range(0, width):
        for y in range(0, height):
            live_neighbours = count_live_neighbours(x, y, population)
            # Any live cell...
            if population[x][y] == live_cell:
                # ... with fewer than two live neighbours dies, as if caused by under-population.
                if live_neighbours < 2:
                    next_generation[x][y] = dead_cell
                # ... with two or three live neighbours lives on to the next generation.
                if live_neighbours in [2, 3]:
                    next_generation[x][y] = live_cell
                # ... with more than three live neighbours dies, as if by over-population.
                if live_neighbours > 3:
                    next_generation[x][y] = dead_cell
            # Any dead cell...
            if population[x][y] == dead_cell:
                # ... with exactly three live neighbours becomes a live cell, as if by reproduction.
                if live_neighbours == 3:
                    next_generation[x][y] = live_cell

    return next_generation

# empty initialisation
def empty_population():
    population = [[0 for x in range(width)] for y in range(height)]

    # initialise to zero
    for x in range(0, width):
        for y in range(0, height):
            population[x][y] = dead_cell
    return population

def blinker():
    population = empty_population()
    population[1][0] = live_cell
    population[1][1] = live_cell
    population[1][2] = live_cell

# randomly initialise
def random_population():
    population = empty_population()

    for x in range(0, width):
        for y in range(0, height):
            probability = random.randint(0, 100)
            if probability > random_population_pc:
                population[x][y] = live_cell
            else:
                population[x][y] = dead_cell
    return population

# are all locations dead?
def is_extinct(population):
    living = 0
    for x in range(0, width):
        for y in range(0, height):
            if population[x][y] == live_cell:
                living += 1
    return (living == 0)
    
def display_population(population):
#    display.clear()
    for x in range(0, width):
        for y in range(0, height):
            display.set_pixel(x, y, population[x][y])

def show_patronus():
    animals = [
        Image.DUCK,
        Image.RABBIT,
        Image.COW,
        Image.PACMAN,
        Image.TORTOISE,
        Image.BUTTERFLY,
        Image.GIRAFFE,
        Image.SNAKE
        ]

    display.show(random.choice(animals))

# Game start...
#display.scroll("Game of Life")

show_patronus()
sleep(2 * refresh_rate_in_ms)
display.clear()

reset_population = True
regenerate_population = True

living_cells = random_population()

# Game loop
while True:

    if is_extinct(living_cells):
        display.clear()
        display.show(Image.SAD)
        sleep(refresh_rate_in_ms)
        reset_population = True
    else:
        display_population(living_cells)

    sleep(refresh_rate_in_ms)

    # Reset the population by shaking !!!

    # button a should be used to toggle single step mode

    if button_a.was_pressed():
        reset_population = True

    if reset_population:
        living_cells = random_population()
        reset_population = False
        display.clear()

    # regenerate a new population
    if regenerate_population:
        living_cells = create_next_generation(living_cells)

