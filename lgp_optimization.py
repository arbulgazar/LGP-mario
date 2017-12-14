from random import randint, random, uniform
import numpy as np
import os.path
import os
import errno
import csv
import sys
import pygame as pg
import cProfile

MIN_INSTRUCTIONS = 200
MAX_INSTRUCTIONS = 2000
MIN_TIME = 200
MAX_TIME = 500
#=== keybinding: ===
#     'right':1,
#     'jump':2,
#     'still': 3,
#     'action': 4,
#     'down':5,
#     'left':6,
N_COMMANDS = 2
MUTATE_BACK_ACTIONS = 3

N_GENERATIONS = 1000
POPULATION_SIZE = 1

SAVE_FREQUENCY = 1
POPULATION_FOLDER = 'populations'

DRAW_FRAMES = True


def initialize_population():
    population = []
    for i in range(0, POPULATION_SIZE):
        n_instructions = randint(MIN_INSTRUCTIONS, MAX_INSTRUCTIONS)
        chromosome = []
        chromosome.append(3)
        chromosome.append(1000)
        for j in range(0, n_instructions):
            random_command = randint(1, N_COMMANDS)
            random_time = randint(MIN_TIME, MAX_TIME)
            chromosome.append(random_command)
            chromosome.append(random_time)
        population.append(chromosome)

    return population


def get_fitness(distance, lastIndex):
    fitness = distance
    return fitness



def mutate(chromosome, lastIndex):
    for i, gene in enumerate(chromosome):
        if i > lastIndex - MUTATE_BACK_ACTIONS*2:
            if i % 2 == 0:
                chromosome[i] = randint(1, N_COMMANDS)
                chromosome[i+1] = randint(MIN_TIME, MAX_TIME)
    return chromosome


# Run game in this function
def decode_chromosome(chromosome):
    from data.marioMain import mainMario
    # chromosome = [3, 500, 1, 2000, 2, 200, 1, 1350, 2, 200, 1, 1300, 2, 200, 1, 300, 2, 200, 1, 1000, 2, 200, 1, 300,
    #               2, 200, 1, 500, 3, 860, 2, 200, 1, 500, 2, 200, 1, 1000, 2, 200, 1, 700, 2, 200, 1, 2200,
    #               2, 200, 1, 800, 2, 200, 1, 200, 6, 300, 2, 200,
    #               1, 1600, 2, 200, 1, 1000, 2, 100, 1, 1500, 2, 100, 3, 400, 6, 300,
    #               2, 100, 1, 500, 6, 300, 2, 100, 1, 1500,
    #               2, 100, 1, 500, 2, 100, 1, 200, 2, 100, 1, 100, 2, 100, 1, 500, 2, 200, 1, 1000,
    #               2, 100, 1, 500, 2, 100, 1, 200, 2, 100, 1, 100, 2, 100, 1, 500, 2, 200, 1, 1000,
    #               2, 100, 1, 500, 3, 1000, 1, 800, 2, 100, 1, 900,
    #               2, 100, 1, 500, 2, 100, 1, 200, 2, 100, 1, 100, 2, 100, 1, 500, 2, 200, 1, 1000,
    #               2, 100, 1, 2000
    #               ]
    distance, lastIndex = mainMario(chromosome, redraw=DRAW_FRAMES)
    return distance, lastIndex

def main():
    bestDistance = 0
    bestChromosome = []
    bestLastIndex = 0

    print('- Enter a name of the population \n- If the name already exists the population will be loaded '
          '\n- Otherwise a new population will be created with the selected name')
    population_name = raw_input()
    file_path = os.path.join(POPULATION_FOLDER, '{}.txt'.format(population_name))

    if os.path.isfile(file_path):
        population = []
        with open(file_path, 'rb') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                population.append(map(int, row))
    else:
        population = initialize_population()
        print population[0:20]


    for generation in range(N_GENERATIONS):
        for i, chromosome in enumerate(population):
            print('Run number: {}'.format(generation+1))
            distance, lastIndex = decode_chromosome(chromosome)
            print "distance ", distance, "bestDist ",bestDistance, "lastIdx ", lastIndex, "bestlastIdx", bestLastIndex

        if distance > bestDistance:
            bestChromosome = chromosome
            bestDistance = distance
            bestLastIndex = lastIndex
        else:
            chromosome = bestChromosome
            lastIndex = bestLastIndex

        for i, chromosome in enumerate(population):
            new_chromosome = mutate(chromosome, lastIndex)
            population[i] = new_chromosome


        if generation % SAVE_FREQUENCY == 0:
            if os.path.isfile(file_path):
                os.remove(file_path)
            if not os.path.exists(os.path.dirname(file_path)):
                try:
                    os.makedirs(os.path.dirname(file_path))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(file_path, 'wb') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                for row in population:
                    writer.writerow(row)
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
