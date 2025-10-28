from datetime import datetime

import numpy as np
from numpy.typing import NDArray
from pyscipopt import Model, quicksum

from ui.display import format_results

from data_loader import (
    DISHES_DF,
    LABELS,
    PLANTS_DF,
)


def optimize(budget, strategy, stocks, sold_prices):
    """
    Calculate the optimal solution of item sales based on the given budget
    and inventory constraints.

    Args:
        - budget (int): The total budget available for purchasing items.
        - strategy (str): The strategy to use for optimization, either "MinimizeStock" or "MaximizeStock".
        - stocks (NDArray[int]): An array representing the available stock of each item.
        - sold_prices (NDArray[int]): An array representing the selling price of each item.

    Returns:
        - dict: A dictionary containing the solution, total price, total count,
    """
    # Initialize the master problem
    model = Model("Knapsack")

    # Decision variables in master problem
    x = [
        model.addVar(
            vtype="I", name=f"x_{i}", lb=0, ub=int(stocks[i]) if stocks[i] else 0
        )
        for i in range(len(stocks))
    ]

    obj1 = quicksum(sold_prices[i] * x[i] for i in range(len(stocks)))
    obj2 = quicksum(x[i] for i in range(len(stocks)))

    # Objective: maximize total value of sold plants
    model.setObjective(obj1, "maximize")

    model.addCons(obj1 <= budget)

    # first optimize
    model.hideOutput()
    model.optimize()

    if model.getStatus() == "optimal":
        optimal_total_value = model.getObjVal()
        model.freeTransform()

        model.setObjective(
            obj2, "maximize" if strategy == "MinimizeStock" else "minimize"
        )
        model.addCons(obj1 == optimal_total_value)
        model.optimize()

        # Final solution processing
        solution = [0] * len(x)
        total_value = 0
        total_count = 0

        if model.getStatus() == "optimal":
            for i, var in enumerate(x):
                if (n := round(model.getVal(var))) > 0 and sold_prices[i] > 0:
                    solution[i] = n
                    total_count += n
                    total_value += n * sold_prices[i]

            return {
                "solution": solution,
                "total_price": int(total_value),
                "total_count": int(total_count),
                "remaining": int(budget - total_value),
            }
    raise ValueError(
        f"Optimization failed with status: {model.getStatus()} at {datetime.now()}"
    )


def get_results(
    language,
    currency,
    budget,
    plants_prices_extra_rate,
    dishes_prices_extra_rate,
    talent_price_bonus,
    strategy,
    *inventory,
):
    talent_price_bonus = talent_price_bonus or 0
    prices: NDArray[np.int16] = np.concat(
        [
            PLANTS_DF[currency] * (1 + plants_prices_extra_rate),
            np.floor(
                DISHES_DF[currency]
                * (1 + dishes_prices_extra_rate)
                * (1 + talent_price_bonus / 100)
            ).astype(
                np.int16
            ),  # Licet(@discord)'s data shows that all values are rounded down: https://docs.google.com/spreadsheets/d/1CWv0VmgfKKWWlqUty9hqGwWt86_G94x5K89DP4b4eRI
        ],
        dtype=np.int16,
    )
    outputs = optimize(
        budget,
        strategy,
        np.array([n if n else 0 for n in inventory], dtype=np.int16),
        prices,
    )
    plants_solution = outputs["solution"][: len(PLANTS_DF)]
    dishes_solution = outputs["solution"][
        len(PLANTS_DF) : len(PLANTS_DF) + len(DISHES_DF)
    ]
    results = {}
    results["solution"] = {
        f"{LABELS[language]['plants'][PLANTS_DF.iloc[i]['name']]} ({LABELS[language]['tiers'][PLANTS_DF.iloc[i]['tier']]}, {int(prices[i])} {currency})": plants_solution[
            i
        ]
        for i in range(len(PLANTS_DF))
        if plants_solution[i] > 0
    }
    results["solution"].update({
        f"{LABELS[language]['dishes'][DISHES_DF.iloc[i]['name']]} ({LABELS[language]['tiers'][DISHES_DF.iloc[i]['tier']]}, {int(prices[len(PLANTS_DF) + i])} {currency})": dishes_solution[
            i
        ]
        for i in range(len(DISHES_DF))
        if dishes_solution[i] > 0
    })
    results["total_price"] = outputs["total_price"]
    results["total_count"] = outputs["total_count"]
    results["remaining"] = outputs["remaining"]
    return format_results(results, language)
