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
from ui.i18n import setup_i18n

_ = setup_i18n()


def get_language():
    """
    Returns a Gradio Dropdown component for selecting language.
    """
    return gr.Dropdown(
        choices=[("English", "en"), ("简体中文", "cn"), ("日本語", "ja")],
        value="en",
        label=_("Language"),
        info=_(
            "Select the language for the interface. Currently, only part of texts are translated."
        ),
        elem_id="language-select",
        interactive=True,
    )


def update_inventory_ui_by_language(language):
    setup_i18n(language)
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


def get_currency():
    """
    Returns a Gradio Radio component for selecting currency.
    """
    return gr.Radio(
        choices=[(_("Gold"), "gold"), (_("Gems"), "gems")],
        value="gold",
        type="value",
        label="Currency",
        info="Select the currency.",
        interactive=True,
        elem_id="currency-radio",
        render=True,
    )


def get_budget():
    """
    Returns a Gradio Number component for budget input.
    """
    return gr.Number(
        value=0,
        label=_(_("Budget")),
        info=_(_("Enter your budget amount.")),
        elem_id="budget-number",
        interactive=True,
        precision=0,
        minimum=0,
        maximum=50000,
        step=1000,
    )


def get_blooms_acquisition_rate():
    """
    Returns a Gradio Dropdown component for Blooms Acquisition Rate.
    """
    return gr.Dropdown(
        choices=[
            _("0(Gabby's Acquisition)"),
            _("+100%(HVA for Shop Level 1 & 2)"),
            _("+200%(HVA for Shop Level 3 & 4)"),
            _("+300%(HVA for Shop Level 5 & 6)"),
        ],
        value=_("0(Gabby's Acquisition)"),
        type="index",
        label="Blooms Extra Acquisition Rate",
        info="Select your high-value acquisition rate for Bewildering Blooms.",
        interactive=True,
    )


def get_confiserie_acquisition_rate():
    """Returns a Gradio Dropdown component for Confiserie Acquisition Rate."""
    return gr.Dropdown(
        choices=[
            _("0(Andre's Acquisition)"),
            _("+100%(HVA for Shop Level 1 & 2)"),
            _("+200%(HVA for Shop Level 3 & 4)"),
            _("+300%(HVA for Shop Level 5 & 6)"),
        ],
        value=_("0(Andre's Acquisition)"),
        type="index",
        label="Confiserie Extra Acquisition Rate",
        info="Select your high-value acquisition rate for The Confiserie.",
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

    checkbox_group_component = gr.CheckboxGroup(
        choices=filtered_plants_labels,
        value=default_value,
        type="value",
        label=_("Plants"),
        info=_("Select plants"),
        interactive=True,
    )
    return checkbox_group_component


def update_plants_selector(language, currency):
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
        label=_("Dishes"),
        info=_("Select dishes."),
        interactive=True,
    )


def update_dishes_selector(language, currency):
    new_choices = _generate_dish_choices(language, currency)

    return gr.update(choices=new_choices)


def prerender_inventory_inputs() -> list[gr.Number]:
    """Returns Gradio Number components for inventory input."""

    def _get_inventory_input(row, visible=True, **kwargs) -> gr.Number:
        """
        Returns a Gradio Number component for inventory input based on the dataframe row data."""
        return gr.Number(
            label=_(
                PLANTS_LABELS[row["name"]]
                if row["name"] in PLANTS_LABELS
                else DISHES_LABELS[row["name"]]
            ),
            info=_(
                f"{TIERS_LABELS[row['tier']]} ${row['gold'] if row['gold'] > 0 else row['gems']}"
            ),
            value=0,
            precision=0,
            minimum=0,
            maximum=2000,
            visible=visible,
            interactive=True,
            key=f"{row['name']}-{row['tier']}",
            **kwargs,
        )

    return [
        _get_inventory_input(row, visible=False) for _, row in PLANTS_DF.iterrows()
    ] + [_get_inventory_input(row, visible=False) for _, row in DISHES_DF.iterrows()]


def update_inventory_inputs(
    selected_plants: Sequence[str], selected_dishes: Sequence[str], currency: str
) -> list[gr.Number]:
    """
    Updates the inventory inputs based on the selected plants and dishes.
    """
    _out = []
    for _, row in PLANTS_DF.iterrows():
        _out.append(
            gr.Number(
                visible=True and row[currency] > 0 and row["tier"] != "feeble",
            )
            if row["name"] in selected_plants
            else gr.Number(value=0, visible=False)
        )
    for _, row in DISHES_DF.iterrows():
        _out.append(
            gr.Number(
                visible=row[currency] > 0,
            )
            if row["name"] in selected_dishes
            else gr.Number(value=0, visible=False)
        )

    return _out


def get_strategy():
    """
    Returns a Gradio Radio component for selecting the selling strategy.
    """
    return gr.Radio(
        choices=[
            (_("Prioritize high-priced items"), "MaximizeStock"),
            (_("Prioritize low-priced items"), "MinimizeStock"),
        ],
        value="MinimizeStock",
        type="value",
        label=_("Selling Strategy"),
        info=_("Select the strategy for selling plants."),
        interactive=True,
        elem_id="strategy-radio",
    )
