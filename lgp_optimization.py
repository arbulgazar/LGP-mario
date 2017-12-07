from random import randint, random, uniform
import numpy as np
import os.path
import csv
import sys
import pygame as pg
import cProfile
from data import marioMain

MIN_INSTRUCTIONS = 10
MAX_INSTRUCTIONS = 30
MIN_TIME = 1
MAX_TIME = 1000
N_COMMANDS = 8

N_GENERATIONS = 100
POPULATION_SIZE = 10
TOURNAMENT_SIZE = 5
ELITISM_SIZE = 1
P_TOUR = 0.7
P_CROSSOVER = 0.5
P_MUTATE = 0.01

MAX_DISTANCE = 100
SAVE_FREQUENCY = 100
POPULATION_FOLDER = 'populations'


def initialize_population():
    population = []
    for i in range(0, POPULATION_SIZE):
        n_instructions = randint(MIN_INSTRUCTIONS, MAX_INSTRUCTIONS)
        chromosome = []
        for j in range(0, n_instructions):
            random_command = randint(1, N_COMMANDS)
            random_time = randint(MIN_TIME, MAX_TIME)
            chromosome.append(random_command)
            chromosome.append(random_time)
        population.append(chromosome)

    return population


def get_fitness(distance, time):
    fitness = distance/MAX_DISTANCE*100 - time/10
    return fitness


def tournament_select(fitness_list):
    population_size = len(fitness_list)
    indices = np.random.randint(population_size, size=TOURNAMENT_SIZE)
    fitness_tmp = fitness_list[indices]
    sorting = fitness_tmp.argsort()
    indices = indices[sorting]

    not_selected = True
    tournament_counter = 1

    while not_selected:
        if random() > P_TOUR or tournament_counter == TOURNAMENT_SIZE:
            index_selected = indices[0]
            not_selected = False
        else:
            indices = np.delete(indices, 0)
        tournament_counter += 1

    return index_selected


def crossover(chromosome_1, chromosome_2):
    length_c_1 = len(chromosome_1)
    length_c_2 = len(chromosome_2)
    split_1 = 2*randint(1, length_c_1/2)
    split_2 = 2*randint(split_1/2, length_c_1/2)
    split_3 = 2*randint(1, length_c_2/2)
    split_4 = 2*randint(split_3/2, length_c_2/2)

    c_1_part_1 = chromosome_1[0:split_1]
    c_1_part_2 = chromosome_1[split_1:split_2]
    c_1_part_3 = chromosome_1[split_2:length_c_1]
    c_2_part_1 = chromosome_2[0:split_3]
    c_2_part_2 = chromosome_2[split_3:split_4]
    c_2_part_3 = chromosome_2[split_4:length_c_2/2]

    new_c_1 = [c_1_part_1, c_2_part_2, c_1_part_3]
    new_c_2 = [c_2_part_1, c_1_part_2, c_2_part_3]

    new_c_1 = [value for part in new_c_1 for value in part]
    new_c_2 = [value for part in new_c_2 for value in part]

    return new_c_1, new_c_2


def mutate(chromosome):
    for i, gene in enumerate(chromosome):
        r = uniform(0, 1)
        if r < P_MUTATE:
            if i % 2 == 0:
                chromosome[i] = randint(1, N_COMMANDS)
            else:
                chromosome[i] = randint(MIN_TIME, MAX_TIME)
    return chromosome


def perform_elitism(population, best_chromosome):
    for i in range(ELITISM_SIZE):
        population[i] = best_chromosome
    return population

# Run game in this function
def decode_chromosome(chromosome):
    chromosome = [3]
    distance, time = marioMain.mainMario(chromosome)
    pg.quit()
    sys.exit()

def main():
    distance = 0
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
                population.append(row)
    else:
        population = initialize_population()

    for generation in range(N_GENERATIONS):
        best_fitness = 0
        best_chromosome = []
        fitness_list = []
        for chromosome in population:
            #TODO remove comment and (maybe) adjust fitness function after running game works
            #distance, time = run_game(chromosome)
            decode_chromosome(chromosome)
            fitness = get_fitness(distance, time)
            fitness_list.append(fitness)
            if fitness > best_fitness:
                best_chromosome = chromosome
                best_fitness = fitness
        fitness_list = np.array(fitness_list)

        tmp_population = []

        for i in range(0, POPULATION_SIZE, 2):
            index_1 = tournament_select(fitness_list)
            index_2 = tournament_select(fitness_list)
            chromosome_1 = population[index_1]
            chromosome_2 = population[index_2]

            if random() < P_CROSSOVER:
                chromosome_1, chromosome_2 = crossover(chromosome_1, chromosome_2)
            tmp_population.append(chromosome_1)
            tmp_population.append(chromosome_2)

        for i, chromosome in enumerate(tmp_population):
            new_chromosome = mutate(chromosome)
            tmp_population[i] = new_chromosome

        #TODO remove comment when running game works
        #population = perform_elitism(tmp_population, best_chromosome)

        #TODO remove line when elitism is used
        population = tmp_population

        if generation % SAVE_FREQUENCY == 0:
            if os.path.isfile(file_path):
                os.remove(file_path)
            with open(file_path, 'wb') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                for row in population:
                    writer.writerow(row)


if __name__ == "__main__":
    main()
