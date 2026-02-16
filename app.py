import gradio as gr

from solver import get_results
from ui.display import (
    get_blooms_acquisition_rate,
    get_budget,
    get_confiserie_acquisition_rate,
    get_currency,
    get_dishes_selector,
    get_language,
    get_plants_selector,
    get_strategy,
    get_talent_price_bonus,
    prerender_inventory_inputs,
    update_all_ui_components,
    update_dishes_selector_on_language,
    update_inventory_inputs,
    update_inventory_ui_by_language,
    update_plants_selector_on_language,
    update_selectors_on_currency,
)

# Hightlight the first tier of item
css = """
/* Minimal tier distinction for inventory inputs */
.tier-radiant { background-color: #fff8dc; }
.tier-radiant-rarecolor { background-color: #fff8dc; }
.tier-flourishing { background-color: #e6e6fa; }
.tier-flourishing-rarecolor { background-color: #e6e6fa; }
.tier-hardy { background-color: #f0f8ff; }
.tier-hardy-rarecolor { background-color: #f0f8ff; }
.tier-legendary { background-color: #fff8dc; } 
.tier-epic { background-color: #e6e6fa; }
.tier-rare { background-color: #f0f8ff; }
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
    gr.HTML("""<div style="display: flex; justify-content: center; gap: 20px; ">
            <a href="https://github.com/ChanningWang2018/ArithmancySolver4HPMA" target="_blank" style="text-decoration: none; color: #2563eb; font-weight: 500;">
                💻 GitHub Repo
            </a>
            <a href="https://www.modelscope.cn/studios/OhMyDearAI/ArithmancySolver4HPMA" target="_blank" style="text-decoration: none; color: #2563eb; font-weight: 500;">
                📚 ModelScope Studio
            </a>
        </div>""")

    gr.HTML(
        """<div style="text-align: center; font-weight: bold;">
            <p>✨✨✨Click <a href="https://grimmauldplace.top/sales-optimizer" target="_blank" style="color: #2563eb;">here</a> to try another cool solver!✨✨✨</p>
            <p>🐴"Horse" you doing? Happy New Year! 🐴</p>
        </div>"""
    )
    with gr.Column(key="main"):
        language: gr.Radio = get_language("en")
        currency: gr.Radio = get_currency("en")
        budget: gr.Number = get_budget("en")

        plants_selector: gr.CheckboxGroup = get_plants_selector("en", "gold")
        dishes_selector: gr.CheckboxGroup = get_dishes_selector("en", "gold")
        with gr.Row(key="inventory_inputs"):
            inventory_inputs = prerender_inventory_inputs()
        strategy: gr.Radio = get_strategy("en")
        blooms_rate: gr.Dropdown = get_blooms_acquisition_rate("en")
        confiserie_rate: gr.Dropdown = get_confiserie_acquisition_rate("en")
        talent_price_bonus: gr.Number = get_talent_price_bonus("en")
        solve_button = gr.Button("Solve")
        results_output = gr.Textbox(label="Results", show_copy_button=True)

    gr.on(
        language.change,
        update_inventory_ui_by_language,
        inputs=[language],
        outputs=inventory_inputs,
    )

    gr.on(
        language.change,
        fn=update_plants_selector_on_language,
        inputs=[language, currency],
        outputs=plants_selector,
    )

    gr.on(
        language.change,
        fn=update_dishes_selector_on_language,
        inputs=[language, currency],
        outputs=dishes_selector,
    )

    gr.on(
        language.change,
        fn=update_all_ui_components,
        inputs=[language],
        outputs=[
            language,
            currency,
            budget,
            blooms_rate,
            confiserie_rate,
            strategy,
            talent_price_bonus,
            results_output,
            solve_button,
        ],
    )

    currency.change(
        update_selectors_on_currency,
        inputs=[language, currency],
        outputs=[plants_selector, dishes_selector],
    )

    gr.on(
        triggers=[plants_selector.change, dishes_selector.change],
        fn=update_inventory_inputs,
        inputs=[plants_selector, dishes_selector, currency],
        outputs=inventory_inputs,
    )

    solve_button.click(
        fn=get_results,
        inputs=[
            language,
            currency,
            budget,
            blooms_rate,
            confiserie_rate,
            talent_price_bonus,
            strategy,
        ]
        + inventory_inputs,
        outputs=results_output,
    )

demo.queue()
demo.launch(share=False)
