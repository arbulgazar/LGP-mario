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
            else:
                chromosome[i] = randint(MIN_TIME, MAX_TIME)
    return chromosome


def fix_chromosome_length(chromosome):
    n_instructions = randint(MIN_INSTRUCTIONS, MAX_INSTRUCTIONS)
    if len(chromosome)*2 < n_instructions:
        print "Fixed length of chromosome from", len(chromosome), "to", n_instructions
        for j in range(len(chromosome), n_instructions):
            random_command = randint(1, N_COMMANDS)
            random_time = randint(MIN_TIME, MAX_TIME)
            chromosome.append(random_command)
            chromosome.append(random_time)
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
    file_path_fitness = os.path.join(POPULATION_FOLDER, '{}_fitness.txt'.format(population_name))

    if os.path.isfile(file_path):
        population = []
        with open(file_path, 'rb') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                population.append(map(int, row))
        bestChromosome = (population[0])[:]
        bestLastIndex = len(bestChromosome) - 4 # to be safe

        temp_index = 0
        while (temp_index < bestLastIndex):
            print "Finding bestDistanceb\tbestlastIdx", bestLastIndex
            bestDistance, temp_index = decode_chromosome(bestChromosome)
            print "Finding bestDistance\tdistance ", bestDistance, "lastIdx ", temp_index, "bestlastIdx", bestLastIndex

    else:
        population = initialize_population()
        print population[0:20]

    for generation in range(N_GENERATIONS):
        for i, chromosome in enumerate(population):
            print('Run number: {}'.format(generation+1))
            chromosome = fix_chromosome_length(chromosome)
            distance, lastIndex = decode_chromosome(chromosome)
            print "distance ", distance, "bestDist ", bestDistance, "lastIdx ", lastIndex, "bestlastIdx", bestLastIndex

        if distance > bestDistance:
            bestChromosome = chromosome[0:lastIndex+2]
            bestDistance = distance
            bestLastIndex = lastIndex
        else:
            chromosome = bestChromosome[:]
            lastIndex = bestLastIndex

        new_chromosome = mutate(chromosome, lastIndex)
        population[0] = new_chromosome
        # for i, chromosome in enumerate(population):
        #     new_chromosome = mutate(chromosome, lastIndex)
        #     population[i] = new_chromosome

        if generation % SAVE_FREQUENCY == 0:
            if os.path.isfile(file_path):
                os.remove(file_path)
            if not os.path.exists(os.path.dirname(file_path)):
                try:
                    os.makedirs(os.path.dirname(file_path))
                    os.makedirs(os.path.dirname(file_path_fitness))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(file_path, 'wb') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                for row in population:
                    writer.writerow(row)
            with open(file_path_fitness, 'a') as csv_file_2:
                writer_2 = csv.writer(csv_file_2, delimiter=';')
                writer_2.writerow([bestDistance])

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
