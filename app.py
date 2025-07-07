import gradio as gr
from httpx import get

from solver import get_results, optimize
from ui.components import (
    get_blooms_acquisition_rate,
    get_budget,
    get_confiserie_acquisition_rate,
    get_currency,
    get_language,
    get_selected_dishes,
    get_selected_plants,
    get_strategy,
    prerender_inventory_inputs,
    update_inventory_inputs,
)

# Hightlight the first tier of item
css = """
.highlight-gold {background-color: #fafad2}
.highlight-gems {background-color: #fed9b4}
"""

# Title Animation
js = """
function createGradioAnimation() {
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '3em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'center';
    container.style.marginBottom = '20px';

    var text = 'Arithmancy Solver for HPMA 📜';
    for (var i = 0; i < text.length; i++) {
        (function(i){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.5s';
                letter.innerText = text[i];

                container.appendChild(letter);

                setTimeout(function() {
                    letter.style.opacity = '1';
                }, 25);
            }, i * 125);
        })(i);
    }

    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(container, gradioContainer.firstChild);

    return 'Animation created';
}
"""

with gr.Blocks(js=js, css=css, theme=gr.themes.Monochrome()) as demo:
    with gr.Column(key="main"):
        lang: gr.Dropdown = get_language()
        currency: gr.Radio = get_currency()
        budget: gr.Number = get_budget()

        plants_checkboxes: gr.CheckboxGroup = get_selected_plants("gold")
        dishes_checkboxes: gr.CheckboxGroup = get_selected_dishes("gold")
        with gr.Row(key="inventory_inputs"):
            inventory_inputs = prerender_inventory_inputs()
        strategy: gr.Radio = get_strategy()
        blooms_rate: gr.Dropdown = get_blooms_acquisition_rate()
        confiserie_rate: gr.Dropdown = get_confiserie_acquisition_rate()
        solve_button = gr.Button("Solve")
        results_output = gr.Textbox(label="Results", show_copy_button=True)

    gr.on(
        triggers=[currency.change],
        fn=get_selected_plants,
        inputs=currency,
        outputs=plants_checkboxes,
    )

    gr.on(
        triggers=[currency.change],
        fn=get_selected_dishes,
        inputs=currency,
        outputs=dishes_checkboxes,
    )

    gr.on(
        triggers=[plants_checkboxes.change, dishes_checkboxes.change],
        fn=update_inventory_inputs,
        inputs=[plants_checkboxes, dishes_checkboxes, currency],
        outputs=inventory_inputs,
    )

    solve_button.click(
        fn=get_results,
        inputs=[
            currency,
            budget,
            blooms_rate,
            confiserie_rate,
            strategy,
        ]
        + inventory_inputs,
        outputs=results_output,
    )

demo.queue()
demo.launch(share=False)
