"""
Module Name: genetic_algorithm.py
Description: Need to update!

Last Updated: 2024-09-01
"""

import random

import numpy as np
import pandas as pd
import pygad

from src.modules.fitness_functions import martin_ratio, profit_factor, total_return
from src.modules.pattern_evaluation import evaluate_candlestick_pattern
from src.modules.pattern_generator import CandlestickPatternGenerator
from src.utils.logger import logger


class GeneticAlgorithm:
    # TODO : Add docstrings
    def __init__(
        self,
        df: pd.DataFrame,
        pop_size,
        num_gens: int,
        num_conds: int,
        max_lag: int,
        fitness_type: str,
        bullish_focus: bool,
    ):
        self.num_generations = num_gens
        self.population_size = pop_size
        self.num_conds = num_conds
        self.max_lag = max_lag
        self.training_data = df
        self.fitness_function_type = fitness_type
        self.bullish_focus = bullish_focus

    def create_instance(self):
        """
        Create an instance of the Genetic Algorithm.

        Returns :
        -------
            - `ga_instance` : Instance of the GA class from the pygad library
        """
        generator = CandlestickPatternGenerator(self.max_lag, self.num_conds)
        initial_population = generator.get_patterns(self.population_size)

        ga_instance = pygad.GA(
            num_generations=self.num_generations,
            num_parents_mating=len(initial_population),
            fitness_func=self._fitness_func,
            initial_population=initial_population,
            parent_selection_type="rws",  # Roulette Wheel Selection
            keep_elitism=1,  # Keep the best solution from the previous generation
            crossover_type=self._crossover_func,  # Single-point crossover function
            mutation_type=self._mutation_func,  # TODO : Implement mutation function
            on_start=self._on_start,
            on_generation=self._on_generation,
            on_stop=self._on_stop,
            suppress_warnings=True,  # set to False while debugging
            save_solutions=False,  # TODO : Looks into how this effect performance
            gene_type=int,
            gene_space=[
                gene
                for _ in range(self.num_conds)
                for gene in (
                    list(range(4)),  # Alleles: Open, High, Low, Close
                    list(range(self.max_lag + 1)),  # Alleles: 0, 1, ..., max_lag
                    list(range(2)),  # Alleles: <, >
                    list(range(4)),  # Alleles: Open, High, Low, Close
                    list(range(self.max_lag + 1)),  # Alleles: 0, 1, ..., max_lag
                )
            ],
        )

        return ga_instance

    def _fitness_func(
        self,
        ga_instance: pygad.GA,
        solution: np.ndarray,
        solution_idx: np.int64,
    ) -> float:
        """
        Fitness function for the Genetic Algorithm

        Parameters :
        -------
            - `ga_instance` : Instance of the GA class from the pygad library
            - `solution` : Chromosome (candlestick pattern)
            - `solution_idx` : Index of Chromosome in the population

        Returns :
        -------
            - `fitness_value` : Fitness value of `solution` (candlestick pattern)
        """
        
        log_returns = evaluate_candlestick_pattern(
            self.training_data, solution, self.max_lag, self.bullish_focus
        )
        if self.fitness_function_type == "total_return":
            return total_return(log_returns)
        elif self.fitness_function_type == "profit_factor":
            return profit_factor(log_returns)
        elif self.fitness_function_type == "martin_ratio":
            return martin_ratio(log_returns)
        else:
            raise ValueError("Invalid fitness function type")

    def _crossover_func(
        self,
        parents: list[np.ndarray],
        offspring_size: tuple[int, int],
        ga_instance: pygad.GA,
    ) -> np.ndarray:
        """
        Crossover function for a genetic algorithm.

        Parameters :
        -------
            - `parents` : List of parent chromosomes (matting pool)
            - `offspring_size` : Tuple representing the number of offspring to be generated and the number of genes in each offspring (number of chromosomes in population, size of each chromosome)
            - `ga_instance` : Instance of the GA class

        Returns :
        -------
            - `offsprings_population` : Array of offspring chromosomes (candlestick patterns)

        Note:
        -------
            - This function implements a single-point crossover
        """
        possible_splits = [s for s in range(5, offspring_size[1], 5)]
        offsprings_population = []
        while len(offsprings_population) != offspring_size[0]:
            crossover_point = random.choice(possible_splits)
            parent1_idx = random.choice(range(len(parents)))
            parent2_idx = random.choice(range(len(parents)))

            parent1 = parents[parent1_idx]
            parent2 = parents[parent2_idx]

            offspring1 = list(parent1[:crossover_point]) + list(
                parent2[crossover_point:]
            )
            offspring2 = list(parent2[:crossover_point]) + list(
                parent1[crossover_point:]
            )

            # If only one offspring is needed to fill population
            if len(offsprings_population) == offspring_size[0] - 1:
                chosen_offspring = random.choice([offspring1, offspring2])
                offsprings_population.append(chosen_offspring)
            else:
                offsprings_population.append(offspring1)
                offsprings_population.append(offspring2)

        return np.array(offsprings_population)

    def _mutation_func(
        self, offsprings: np.ndarray, ga_instance: pygad.GA
    ) -> np.ndarray:
        """
        Mutation function for a genetic algorithm.

        Parameters :
        -------
            - `offsprings` : Array of offspring chromosomes (candlestick patterns)
            - `ga_instance` : Instance of the GA class from the pygad library

        Returns :
        -------
            - `offsprings` : Array of mutated offspring chromosomes (candlestick patterns)
        """

        for idx in range(offsprings.shape[0]):
            # 2% chance to mutate whole pattern
            if random.random() < 0.02:
                new_pattern = CandlestickPatternGenerator(
                    self.max_lag, self.num_conds
                ).get_patterns(1)[0]
                offsprings[idx] = new_pattern
            # replace gene with 5% probability
            for gene_idx in range(offsprings.shape[1]):
                # TODO: make sure that only possible patters gets generated from mutation
                if random.random() < 0.05:
                    # genes < > are not allowed to mutate
                    # TODO: look into this
                    if (gene_idx - 2) % 5 != 0:
                        new_gene = random.choice(ga_instance.gene_space[gene_idx])
                        offsprings[idx, gene_idx] = new_gene
            # TODO: add mutation counter tuple[int, int] to keep track of mutation rate
        return offsprings

    def _on_generation(self, ga_instance: pygad.GA) -> None:
        """
        Logs a concise summary of the Genetic Algorithm's performance for the latest generation

        Parameters :
        -------
            - ga_instance : Instance of the GA class from the pygad library

        Example :
        -------
            - Example of log message of first generation with hyperparameters (num_conds=3, max_lag=3):
                .. code-block:: txt
                    2024-01-01 00:00:00 - INFO - Generation 1 Evaluation Completed :
                        +-----------------+----------+   Top Ranked Solutions:
                        |FITNESS METRIC   |VALUE     |   +-----+-----------------------------------------------+----------+
                        |-----------------|----------|   |RANK |CANDLESTICK PATTERN                            |FITNESS   |
                        |Best Score       |  40.06031|   |-----|-----------------------------------------------|----------|
                        |-----------------|----------|   |  1  | [0, 0, 1, 0, 3, 3, 2, 0, 2, 1, 1, 3, 0, 0, 0] |  40.06031|
                        |Average Level    |  26.69283|   |-----|-----------------------------------------------|----------|
                        |-----------------|----------|   |  2  | [0, 0, 1, 0, 3, 3, 2, 0, 2, 3, 1, 3, 0, 1, 0] |  38.79146|
                        |Fitness Variance |  14.32392|   |-----|-----------------------------------------------|----------|
                        |-----------------|----------|   |  3  | [1, 0, 1, 0, 3, 3, 2, 0, 2, 3, 1, 3, 0, 0, 0] |  38.68292|
                        |Median Point     |  31.70412|   +-----+-----------------------------------------------+----------+
                        +-----------------+----------+
        """
        fitness_values = ga_instance.last_generation_fitness

        sorted_indices = np.argsort(fitness_values)[::-1]
        top_solutions = [ga_instance.population[i] for i in sorted_indices[:3]]
        top_fitness_values = [fitness_values[i] for i in sorted_indices[:3]]

        log_message = (
            f"Generation {ga_instance.generations_completed} Evaluation Completed :\n"
        )

        ################# metrics_table #################
        metrics_table = ""
        metrics_table += "+" + "-" * 17 + "+" + "-" * 10 + "+\n"
        metrics_table += "|{:17}|{:10}|\n".format("FITNESS METRIC", "VALUE")
        metrics_table += "|" + "-" * 17 + "|" + "-" * 10 + "|\n"

        metrics = [
            ("Best Score", max(fitness_values)),
            ("Average Level", np.mean(fitness_values)),
            ("Fitness Variance", np.std(fitness_values)),
            ("Median Point", np.median(fitness_values)),
        ]

        for i, (metric, value) in enumerate(metrics):
            metrics_table += "|{:17}|{:>10.5f}|\n".format(metric, value)
            if i < len(metrics) - 1:
                metrics_table += "|" + "-" * 17 + "|" + "-" * 10 + "|\n"
            else:
                metrics_table += "+" + "-" * 17 + "+" + "-" * 10 + "+\n"

        ################# metrics_table #################

        ################# solutions_table #################

        solutions_table = "Top Ranked Solutions:\n"
        second_col_length = (
            max(len(str(top_solutions[0].tolist())), len("CANDLESTICK PATTERN")) + 2
        )
        solutions_table += (
            "+" + "-" * 5 + "+" + "-" * second_col_length + "+" + "-" * 10 + "+\n"
        )
        solutions_table += "|{:5}|{:<{}}|{:10}|\n".format(
            "RANK",
            "CANDLESTICK PATTERN",
            second_col_length,
            "FITNESS",
        )
        solutions_table += (
            "|" + "-" * 5 + "|" + "-" * second_col_length + "|" + "-" * 10 + "|\n"
        )

        for idx, (sol, fit) in enumerate(zip(top_solutions, top_fitness_values), 1):
            solutions_table += f"|{idx:^5}| {sol.tolist()} |{fit:>10.5f}|\n"
            if idx < len(top_solutions):
                solutions_table += (
                    "|"
                    + "-" * 5
                    + "|"
                    + "-" * second_col_length
                    + "|"
                    + "-" * 10
                    + "|\n"
                )
            else:
                solutions_table += (
                    "+"
                    + "-" * 5
                    + "+"
                    + "-" * second_col_length
                    + "+"
                    + "-" * 10
                    + "+\n"
                )

        ################# solutions_table #################

        max_length_first_table = max(len(line) for line in metrics_table.split("\n"))
        combined_log = log_message
        metrics_lines = metrics_table.split("\n")
        solutions_lines = solutions_table.split("\n")
        for metrics_line, solutions_line in zip(metrics_lines, solutions_lines):
            combined_log += (
                metrics_line.ljust(max_length_first_table)
                + " " * 3
                + solutions_line
                + "\n"
            )

        logger.info(combined_log)

    def _on_start(self, ga_instance: pygad.GA) -> None:
        # TODO : Add more details (initial fitness, best solution, mutations_rates, etc.)
        """
        Logs detailed initialization data of the Genetic Algorithm.
        """

        ################# info_table #################
        info_table = ""
        info_table += "+" + "-" * 41 + "+\n"
        info_table += "| {:<22} | {:<15}|\n".format("PARAMETER", "VALUE")
        info_table += "|" + "-" * 41 + "|\n"

        parameters = [
            ("Population Size", len(ga_instance.population)),
            ("Matting Pool Size", ga_instance.num_parents_mating),
            ("Number of Conditions", self.num_conds),
            ("Max Lag", self.max_lag),
            ("Fitness Function", self.fitness_function_type),
            ("Bullish Focus", str(self.bullish_focus)),
        ]

        for param, value in parameters:
            info_table += "| {:<22} | {:>15}|\n".format(param, value)

        info_table += "+" + "-" * 41 + "+\n"
        ################# info_table #################

        message = (
            "Genetic Algorithm is starting with the following settings:\n" + info_table
        )

        logger.info(message)

    def _on_stop(self, ga_instance: pygad.GA, last_population_fitness: float) -> None:
        # TODO : Implement on_stop function, add final data to log, summary
        logger.info("Genetic Algorithm is completed.")
