from random import randint, random, uniform
import numpy as np
import os.path
import os
import errno
import csv
import sys
import pygame as pg
import cProfile
from data import marioMain

MIN_INSTRUCTIONS = 3000
MAX_INSTRUCTIONS = 3000
MIN_TIME = 100
MAX_TIME = 100
N_COMMANDS = 3

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
        if i > lastIndex - 10:
            if i % 2 == 0:
                chromosome[i] = randint(1, N_COMMANDS)
    return chromosome


# Run game in this function
def decode_chromosome(chromosome):
    distance, lastIndex = marioMain.mainMario(chromosome, redraw=DRAW_FRAMES)
    return distance, lastIndex

def main():
    bestDistance = 0
    bestChromosome = []
    time = 0
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


    for generation in range(N_GENERATIONS):
        for i, chromosome in enumerate(population):
            print('Run number: {}'.format(generation+1))
            distance, lastIndex = decode_chromosome(chromosome)

        if distance > bestDistance:
            bestChromosome = chromosome
            bestDistance = distance
        else:
            chromosome = bestChromosome

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
