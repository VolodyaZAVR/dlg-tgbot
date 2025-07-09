import random
from math import ceil
from typing import Dict, List, Any


POPULATION_SIZE = 100
GENERATIONS = 150
MUTATION_RATE = 0.1
TOURNEY_SIZE = 5


def calculate_min_pallets(items, weight_limit, volume_limit):
    total_weight = sum(item["Вес"] for item in items)
    total_volume = sum(item["Объем"] for item in items)
    return ceil(max(total_weight / weight_limit, total_volume / volume_limit))


def fitness(solution, items, weight_limit, volume_limit):
    pallets = {}
    for idx, pallet_id in enumerate(solution):
        if pallet_id not in pallets:
            pallets[pallet_id] = {"weight": 0, "volume": 0}
        pallets[pallet_id]["weight"] += items[idx]["Вес"]
        pallets[pallet_id]["volume"] += items[idx]["Объем"]

    penalty = 0
    for p in pallets.values():
        if p["weight"] > weight_limit:
            penalty += (p["weight"] - weight_limit) * 1000
        if p["volume"] > volume_limit:
            penalty += (p["volume"] - volume_limit) * 1000

        weight_utilization = p["weight"] / weight_limit
        volume_utilization = p["volume"] / volume_limit
        balance_penalty = abs(weight_utilization - volume_utilization)
        penalty += balance_penalty * 10

        if weight_utilization < 0.8 or volume_utilization < 0.8:
            penalty += (1 - max(weight_utilization, volume_utilization)) * 100

    return len(pallets) + penalty


def generate_individual(num_items, max_pallets):
    return [random.randint(0, max_pallets - 1) for _ in range(num_items)]


def crossover(parent1, parent2):
    point = random.randint(0, len(parent1) - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]


def mutate(individual, max_pallets, generation):
    mutation_rate = MUTATION_RATE * (1 - generation / GENERATIONS)
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, max_pallets - 1)
    return individual


def tournament_selection(population, fitnesses):
    selected = random.sample(list(zip(population, fitnesses)), TOURNEY_SIZE)
    return min(selected, key=lambda x: x[1])[0]


def genetic_algorithm(items, pallet_count, weight_limit, volume_limit):
    num_items = len(items)
    population = [generate_individual(num_items, pallet_count) for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        fitnesses = [fitness(ind, items, weight_limit, volume_limit) for ind in population]
        best_idx = fitnesses.index(min(fitnesses))
        new_population = [population[best_idx]]

        while len(new_population) < POPULATION_SIZE:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, pallet_count, generation)
            child2 = mutate(child2, pallet_count, generation)
            new_population.extend([child1, child2])

        population = new_population

    final_fitnesses = [fitness(ind, items, weight_limit, volume_limit) for ind in population]
    best_solution = population[final_fitnesses.index(min(final_fitnesses))]
    return best_solution


def is_valid_solution(solution, items, weight_limit, volume_limit):
    pallets = {}
    for idx, pallet_id in enumerate(solution):
        if pallet_id not in pallets:
            pallets[pallet_id] = {"weight": 0, "volume": 0}
        pallets[pallet_id]["weight"] += items[idx]["Вес"]
        pallets[pallet_id]["volume"] += items[idx]["Объем"]

    for p in pallets.values():
        if p["weight"] > weight_limit or p["volume"] > volume_limit:
            return False
    return True


def solution_to_output(order_number: str, items: List[Dict[str, Any]], solution: List[int]) -> List[Dict[str, Any]]:
    """
    Преобразование результата ГА в требуемый формат
    :param order_number: номер заказа
    :param items: входные товары
    :param solution: решение ГА
    :return: отформатированный словарь с палетами
    """
    pallets_dict = {}

    for idx, pallet_id in enumerate(solution):
        if pallet_id not in pallets_dict:
            pallets_dict[pallet_id] = {
                "номер_паллета": f"{order_number}-{pallet_id + 1}",
                "Итого": {"Вес": 0, "Объем": 0},
                "Товары": []
            }
        item = items[idx].copy()
        pallet = pallets_dict[pallet_id]
        pallet["Итого"]["Вес"] += item["Вес"]
        pallet["Итого"]["Объем"] += item["Объем"]
        pallet["Товары"].append({
            "Артикул": item["Артикул"],
            "Номенклатура": item["Номенклатура"],
            "Количество": item["Количество"],
            "Маркер": item["Маркер"],
            "Вес": item["Вес"],
            "Объем": item["Объем"]
        })

    # Сортировка внутри палеты:
    # 1. По убыванию массы
    # 2. При одинаковой массе — по убыванию объема
    for pallet in pallets_dict.values():
        pallet["Товары"] = sorted(pallet["Товары"], key=lambda x: (x["Вес"], x["Объем"]), reverse=True)

    # Присвоение номеров палетам
    result = []
    for i, pallet in enumerate(pallets_dict.values(), start=1):
        pallet["номер_паллета"] = f"{order_number}-{i}"
        result.append(pallet)

    return result


def process_pallet(order_number, items_data, weight_limit, volume_limit):
    """
    Основная логика распределения товаров по палетам
    """
    items = [
        {
            "Артикул": item.Артикул,
            "Номенклатура": item.Номенклатура,
            "Количество": item.Количество,
            "Маркер": item.Маркер,
            "Вес": item.Масса,
            "Объем": item.Объем
        } for item in items_data
    ]

    # Минимальное количество палет можно предсказать как максимум по вместительности одной из величин:
    # Общего веса / допустимый вес палеты или общего объема / допустимый объем палеты
    current_pallet_count = calculate_min_pallets(items, weight_limit, volume_limit)

    # Пробуем 10 раз получить оптимизацию ГА, если не получается увеличиваем число палет на 1
    max_attempts = 10
    found = False
    best_solution = None

    while current_pallet_count <= calculate_min_pallets(items, weight_limit, volume_limit) * 2:
        attempts = 0
        while attempts < max_attempts:
            best_solution = genetic_algorithm(items, current_pallet_count, weight_limit, volume_limit)
            # Если распределение по палетам превышает одно из граничных значений, то не принимаем такое решение
            if is_valid_solution(best_solution, items, weight_limit, volume_limit):
                found = True
                break
            attempts += 1

        if found:
            break
        else:
            current_pallet_count += 1

    if not found:
        raise ValueError("Не удалось найти допустимое решение")

    output = solution_to_output(order_number, items, best_solution)
    return output
