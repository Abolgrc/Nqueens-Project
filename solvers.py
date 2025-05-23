from abc import ABC, abstractmethod
import random
import numpy as np

class Solver(ABC):
    @abstractmethod
    def solve(self, n):
        pass

class BacktrackingSolver(Solver):
    def solve(self, n):
        if n < 4 and n != 1:
            return None
        solution = [-1] * n
        row_attack = [False] * n
        left_diagonal_attack = [False] * (2 * n - 1)
        right_diagonal_attack = [False] * (2 * n - 1)
        
        if self._solve_util(solution, 0, row_attack, left_diagonal_attack, right_diagonal_attack, n):
            return solution
        return None
    
    def _solve_util(self, solution, col, row_attack, left_diagonal_attack, right_diagonal_attack, n):
        if col >= n:
            return True
        for row in range(n):
            if not (row_attack[row] or left_diagonal_attack[row + col] or right_diagonal_attack[col - row + n - 1]):
                solution[col] = row
                row_attack[row] = True
                left_diagonal_attack[row + col] = True
                right_diagonal_attack[col - row + n - 1] = True
                if self._solve_util(solution, col + 1, row_attack, left_diagonal_attack, right_diagonal_attack, n):
                    return True
                solution[col] = -1
                row_attack[row] = False
                left_diagonal_attack[row + col] = False
                right_diagonal_attack[col - row + n - 1] = False
        return False

class GeneticSolver(Solver):
    def solve(self, n):
        if n < 4 and n != 1:
            return None
        if n == 1:
            return [0]
        pop_size = 100
        mutation_prob = 0.1
        max_generations = 1000
        population = [list(np.random.permutation(n)) for _ in range(pop_size)]
        for _ in range(max_generations):
            fitnesses = [self._fitness(c) for c in population]
            if max(fitnesses) == 1:
                return population[fitnesses.index(1)]
            new_population = []
            for _ in range(pop_size):
                p1 = self._random_pick(population, fitnesses)
                p2 = self._random_pick(population, fitnesses)
                child = self._ox_crossover(p1, p2)
                if random.random() < mutation_prob:
                    child = self._mutate(child)
                new_population.append(child)
            population = new_population
        fitnesses = [self._fitness(c) for c in population]
        best = population[fitnesses.index(max(fitnesses))]
        return best if self._fitness(best) == 1 else None

    def _fitness(self, chromosome):
        n = len(chromosome)
        conflicts = 0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(chromosome[i] - chromosome[j]) == j - i:
                    conflicts += 1
        return 1 / (1 + conflicts)

    def _random_pick(self, population, fitnesses):
        total = sum(fitnesses)
        r = random.uniform(0, total)
        upto = 0
        for c, f in zip(population, fitnesses):
            upto += f
            if upto >= r:
                return c.copy()
        return population[-1].copy()

    def _ox_crossover(self, p1, p2):
        n = len(p1)
        k1, k2 = sorted(random.sample(range(n), 2))
        child = [None] * n
        for i in range(k1, k2 + 1):
            child[i] = p1[i]
        child_set = set(child[k1:k2 + 1])
        p2_index = 0
        for i in range(n):
            if child[i] is None:
                while p2[p2_index] in child_set:
                    p2_index = (p2_index + 1) % n
                child[i] = p2[p2_index]
                p2_index = (p2_index + 1) % n
        return child

    def _mutate(self, chromosome):
        n = len(chromosome)
        i, j = random.sample(range(n), 2)
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
        return chromosome

class CSPSolver(Solver):
    def solve(self, n):
        solution = [-1] * n
        if self._backtrack(solution, 0, n):
            return solution
        return None

    def _backtrack(self, solution, col, n):
        if col == n:
            return True
        for row in range(n):
            if self._is_safe(solution, col, row):
                solution[col] = row
                if self._backtrack(solution, col + 1, n):
                    return True
                solution[col] = -1
        return False

    def _is_safe(self, solution, col, row):
        for c in range(col):
            if solution[c] == row or abs(solution[c] - row) == abs(c - col):
                return False
        return True
