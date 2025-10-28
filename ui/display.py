from typing import Sequence

import gradio as gr

from data_loader import (
    DISHES_DF,
    DISHES_LABELS,
    GEMS_DISHES_DF,
    GEMS_PLANTS_DF,
    GOLD_DISHES_DF,
    GOLD_PLANTS_DF,
    LABELS,
    PLANTS_DF,
    PLANTS_LABELS,
    TIERS_LABELS,
)


def get_language(language="en"):
    """
    Returns a Gradio Radio component for selecting language.
    """
    return gr.Radio(
        choices=[("English", "en"), ("简体中文", "cn"), ("日本語", "ja")],
        value="en",
        label=LABELS[language]["ui"]["language"]["label"],
        info=LABELS[language]["ui"]["language"]["info"],
        elem_id="language-select",
        interactive=True,
    )


def update_inventory_ui_by_language(language):
    inventory_inputs = [
        gr.update(
            label=LABELS[language]["plants"][row["name"]],
            info=f"{LABELS[language]['tiers'][row['tier']]} ${row['gold'] if row['gold'] > 0 else row['gems']}",
        )
        for _, row in PLANTS_DF.iterrows()
    ] + [
        gr.update(
            label=LABELS[language]["dishes"][row["name"]],
            info=f"{LABELS[language]['tiers'][row['tier']]} ${row['gold'] if row['gold'] > 0 else row['gems']}",
        )
        for _, row in DISHES_DF.iterrows()
    ]
    return inventory_inputs


def get_currency(language="en"):
    """
    Returns a Gradio Radio component for selecting currency.
    """
    return gr.Radio(
        choices=[
            (LABELS[language]["ui"]["currency"]["gold"], "gold"),
            (LABELS[language]["ui"]["currency"]["gems"], "gems"),
        ],
        value="gold",
        type="value",
        label=LABELS[language]["ui"]["currency"]["label"],
        info=LABELS[language]["ui"]["currency"]["info"],
        interactive=True,
        elem_id="currency-radio",
        render=True,
    )


def get_budget(language="en"):
    """
    Returns a Gradio Number component for budget input.
    """
    return gr.Number(
        value=0,
        label=LABELS[language]["ui"]["budget"]["label"],
        info=LABELS[language]["ui"]["budget"]["info"],
        elem_id="budget-number",
        interactive=True,
        precision=0,
        minimum=0,
        maximum=50000,
        step=1000,
    )


def get_blooms_acquisition_rate(language="en"):
    """
    Returns a Gradio Dropdown component for Blooms Acquisition Rate.
    """
    return gr.Dropdown(
        choices=[
            (option, i)
            for i, option in enumerate(LABELS[language]["ui"]["blooms_rate"]["options"])
        ],
        label=LABELS[language]["ui"]["blooms_rate"]["label"],
        info=LABELS[language]["ui"]["blooms_rate"]["info"],
        interactive=True,
    )


def get_confiserie_acquisition_rate(language="en"):
    """Returns a Gradio Dropdown component for Confiserie Acquisition Rate."""
    return gr.Dropdown(
        choices=[
            (option, i)
            for i, option in enumerate(LABELS[language]["ui"]["blooms_rate"]["options"])
        ],
        label=LABELS[language]["ui"]["confiserie_rate"]["label"],
        info=LABELS[language]["ui"]["confiserie_rate"]["info"],
        interactive=True,
    )


def match_currency_plant(plant_name: str, currency: str) -> bool:
    """
    Checks if a plant can be purchased with the given currency.
    """
    if currency == "gold":
        return plant_name in GOLD_PLANTS_DF["name"].values
    elif currency == "gems":
        return plant_name in GEMS_PLANTS_DF["name"].values
    return False


def _generate_plant_choices(language, currency):
    return [
        (LABELS[language]["plants"][plant], plant)
        for plant in PLANTS_LABELS.keys()
        if match_currency_plant(plant, currency)
    ]


def get_plants_selector(language, currency):
    """
    Returns a Gradio CheckboxGroup component for selecting plants based on the currency.
    """
    filtered_plants_labels: list[tuple[str, str]] = _generate_plant_choices(
        language, currency
    )
    default_value = None

    checkbox_group = gr.CheckboxGroup(
        choices=filtered_plants_labels,
        value=default_value,
        type="value",
        label=LABELS[language]["ui"]["plants_selector"]["label"],
        info=LABELS[language]["ui"]["plants_selector"]["info"],
        interactive=True,
    )
    return checkbox_group


def update_plants_selector_on_currency(language, currency):
    """
    Updates the plants selector based on the selected currency.
    """
    filtered_plants_labels: list[tuple[str, str]] = _generate_plant_choices(
        language, currency
    )

    return gr.update(choices=filtered_plants_labels, value=None)


def update_plants_selector_on_language(language, currency):
    """
    Updates the plants selector based on the selected language.
    """
    new_choices = _generate_plant_choices(language, currency)

    return gr.update(choices=new_choices)


def match_currency_dish(dish_name: str, currency: str) -> bool:
    """
    Checks if a dish can be purchased with the given currency.
    """
    if currency == "gold":
        return dish_name in GOLD_DISHES_DF["name"].values
    elif currency == "gems":
        return dish_name in GEMS_DISHES_DF["name"].values
    return False


def _generate_dish_choices(language, currency):
    return [
        (LABELS[language]["dishes"][dish], dish)
        for dish in DISHES_LABELS.keys()
        if match_currency_dish(dish, currency)
    ]


def get_dishes_selector(language, currency):
    """
    Returns a Gradio CheckboxGroup component for selecting plants based on the currency.
    """
    filtered_dishes_labels: list[tuple[str, str]] = _generate_dish_choices(
        language, currency
    )

    default_value = None

    return gr.CheckboxGroup(
        choices=filtered_dishes_labels,
        value=default_value,
        type="value",
        label=LABELS[language]["ui"]["dishes_selector"]["label"],
        info=LABELS[language]["ui"]["dishes_selector"]["info"],
        interactive=True,
    )


def update_dishes_selector_on_currency(language, currency):
    """
    Updates the dishes selector based on the selected currency.
    """

    filtered_dishes_labels: list[tuple[str, str]] = _generate_dish_choices(
        language, currency
    )

    return gr.update(choices=filtered_dishes_labels, value=None)


def update_selectors_on_currency(language, currency):
    """
    Updates the plants and dishes selector based on the selected currency.
    """
    filtered_plants_labels: list[tuple[str, str]] = _generate_plant_choices(
        language, currency
    )

    filtered_dishes_labels: list[tuple[str, str]] = _generate_dish_choices(
        language, currency
    )

    return [
        gr.update(choices=filtered_plants_labels, value=None),
        gr.update(choices=filtered_dishes_labels, value=None),
    ]


def update_dishes_selector_on_language(language, currency):
    """
    Updates the dishes selector based on the selected language.
    """
    new_choices = _generate_dish_choices(language, currency)

    return gr.update(choices=new_choices)


def prerender_inventory_inputs() -> list[gr.Number]:
    """Returns Gradio Number components for inventory input."""
    return [
        _get_inventory_input(row, visible=False) for _, row in PLANTS_DF.iterrows()
    ] + [_get_inventory_input(row, visible=False) for _, row in DISHES_DF.iterrows()]


def _get_inventory_input(row, visible=True, **kwargs) -> gr.Number:
    """
    Returns a Gradio Number component for inventory input based on the dataframe row data."""
    # Determine CSS class based on tier
    tier_class = f"tier-{row['tier'].replace('_rarecolor', '-rarecolor')}"

    return gr.Number(
        label=PLANTS_LABELS[row["name"]]
        if row["name"] in PLANTS_LABELS
        else DISHES_LABELS[row["name"]],
        info=f"{TIERS_LABELS[row['tier']]} ${row['gold'] if row['gold'] > 0 else row['gems']}",
        value=0,
        precision=0,
        minimum=0,
        maximum=2000,
        visible=visible,
        interactive=True,
        key=f"{row['name']}-{row['tier']}",
        elem_classes=[tier_class] if visible else [],
        **kwargs,
    )


def update_inventory_inputs(
    selected_plants: Sequence[str], selected_dishes: Sequence[str], currency: str
) -> list[gr.Number]:
    """
    Updates the inventory inputs based on the selected plants and dishes.
    """
    _out = []
    for _, row in PLANTS_DF.iterrows():
        if row["name"] in selected_plants:
            is_visible = row[currency] > 0 and row["tier"] != "feeble"
            tier_class = f"tier-{row['tier'].replace('_rarecolor', '-rarecolor')}"
            _out.append(
                gr.Number(
                    visible=is_visible,
                    elem_classes=[tier_class] if is_visible else [],
                )
            )
        else:
            _out.append(gr.Number(value=0, visible=False))

    for _, row in DISHES_DF.iterrows():
        if row["name"] in selected_dishes:
            is_visible = row[currency] > 0
            tier_class = f"tier-{row['tier'].replace('_rarecolor', '-rarecolor')}"
            _out.append(
                gr.Number(
                    visible=is_visible,
                    elem_classes=[tier_class] if is_visible else [],
                )
            )
        else:
            _out.append(gr.Number(value=0, visible=False))

    return _out


def get_talent_price_bonus(language="en"):
    """
    Returns a Gradio Number component for talent price bonus input.
    """
    return gr.Number(
        value=0,
        label=LABELS[language]["ui"]["talent_price_bonus"],
        info=LABELS[language]["ui"]["talent_price_bonus_info"],
        elem_id="talent-price-bonus",
        interactive=True,
        precision=0,
        minimum=0,
        maximum=1000,
        step=1,
    )


def get_strategy(language="en"):
    """
    Returns a Gradio Radio component for selecting the selling strategy.
    """
    return gr.Radio(
        choices=[
            (LABELS[language]["ui"]["strategy"]["maximize_stock"], "MaximizeStock"),
            (LABELS[language]["ui"]["strategy"]["minimize_stock"], "MinimizeStock"),
        ],
        value="MinimizeStock",
        type="value",
        label=LABELS[language]["ui"]["strategy"]["label"],
        info=LABELS[language]["ui"]["strategy"]["info"],
        interactive=True,
        elem_id="strategy-radio",
    )


def format_results(results, language="en"):
    """
    Format the results for display.

    Args:
        results (dict): The results dictionary containing solution, total_price, total_count, and remaining.
        language (str): The language code for localization.

    Returns:
        str: A formatted string representation of the results.
    """
    output = []
    output.append(f"{LABELS[language]['ui']['results']['solution']}: ")
    for item, count in results["solution"].items():
        output.append(f"{item}: {count}")

    output.append(
        f"\n{LABELS[language]['ui']['results']['total_value']}: {results['total_price']}"
    )
    output.append(
        f"{LABELS[language]['ui']['results']['total_count']}: {results['total_count']}"
    )
    output.append(
        f"{LABELS[language]['ui']['results']['remaining_budget']}: {results['remaining']} {'😞' if results['remaining'] else '😁'}"
    )

    return "\n".join(output)


def update_all_ui_components(language):
    """
    Update all UI components with localized text.

    Args:
        language (str): The language code for localization.

    Returns:
        list: List of gr.update objects for all components.
    """
    return [
        # Language component
        gr.update(
            label=LABELS[language]["ui"]["language"]["label"],
            info=LABELS[language]["ui"]["language"]["info"],
        ),
        # Currency component
        gr.update(
            label=LABELS[language]["ui"]["currency"]["label"],
            info=LABELS[language]["ui"]["currency"]["info"],
            choices=[
                (LABELS[language]["ui"]["currency"]["gold"], "gold"),
                (LABELS[language]["ui"]["currency"]["gems"], "gems"),
            ],
        ),
        # Budget component
        gr.update(
            label=LABELS[language]["ui"]["budget"]["label"],
            info=LABELS[language]["ui"]["budget"]["info"],
        ),
        # Blooms acquisition rate component
        gr.update(
            label=LABELS[language]["ui"]["blooms_rate"]["label"],
            info=LABELS[language]["ui"]["blooms_rate"]["info"],
            choices=[
                (option, i)
                for i, option in enumerate(
                    LABELS[language]["ui"]["blooms_rate"]["options"]
                )
            ],
        ),
        # Confiserie acquisition rate component
        gr.update(
            label=LABELS[language]["ui"]["confiserie_rate"]["label"],
            info=LABELS[language]["ui"]["confiserie_rate"]["info"],
            choices=[
                (option, i)
                for i, option in enumerate(
                    LABELS[language]["ui"]["confiserie_rate"]["options"]
                )
            ],
        ),
        # Strategy component
        gr.update(
            label=LABELS[language]["ui"]["strategy"]["label"],
            info=LABELS[language]["ui"]["strategy"]["info"],
            choices=[
                (LABELS[language]["ui"]["strategy"]["maximize_stock"], "MaximizeStock"),
                (LABELS[language]["ui"]["strategy"]["minimize_stock"], "MinimizeStock"),
            ],
        ),
        # Talent price bonus component
        gr.update(
            label=LABELS[language]["ui"]["talent_price_bonus"],
            info=LABELS[language]["ui"]["talent_price_bonus_info"],
        ),
        # Results component
        gr.update(label=LABELS[language]["ui"]["results"]["label"]),
        # Solve button
        gr.update(value=LABELS[language]["ui"]["solve_button"]),
    ]
