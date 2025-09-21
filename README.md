---
title: Arithmancy Solver for HPMA
emoji: 🎡
colorFrom: blue
colorTo: yellow
sdk: gradio
python_version: 3.11
sdk_version: 5.34.1
app_file: app.py
pinned: true
thumbnail: >-
  https://cdn-uploads.huggingface.co/production/uploads/656ab7fafa91c8160906a1c2/Z-6xYlAAlZNZ75bqv4g6e.png
short_description: 'This is a web-based tool to help players of _Harry Potter: M'
---

# Arithmancy Solver for HPMA

This is a web-based tool to help players of _Harry Potter: Magic Awakened_ (HPMA) optimize their in-game trading.

## Features

- Calculate the most efficient way to get Gold and Gems.
- Support for both Plants and Dishes.
- Adjustable acquisition rates for different shop levels.
- User-friendly interface with support for multiple languages.

## How to Run

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the application:**
    ```bash
    python app.py
    ```
3.  Open your web browser and navigate to the URL provided by Gradio.

## 如何更新新的plant与dish
1. 在plants.csv中添加植物的价格数据，或在dishes.csv中添加dish的价格数据

2. 在ui/labels.json中添加翻译

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

