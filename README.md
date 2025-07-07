---
# 详细文档见https://modelscope.cn/docs/%E5%88%9B%E7%A9%BA%E9%97%B4%E5%8D%A1%E7%89%87
domain: #领域：cv/nlp/audio/multi-modal/AutoML
# - cv
tags: #自定义标签
  -
datasets: #关联数据集
  evaluation:
  #- iic/ICDAR13_HCTR_Dataset
  test:
  #- iic/MTWI
  train:
  #- iic/SIBR
models: #关联模型
#- iic/ofa_ocr-recognition_general_base_zh

## 启动文件(若SDK为Gradio/Streamlit，默认为app.py, 若为Static HTML, 默认为index.html)
# deployspec:
#   entry_file: app.py
license: Apache License 2.0
---

#### Clone with HTTP

```bash
 git clone https://www.modelscope.cn/studios/OhMyDearAI/ArithmancySolver4HPMA.git
```

title: Arithmancy Solver for HPMA
emoji: 🎡
colorFrom: blue
colorTo: yellow
sdk: gradio
python_version: 3.11
sdk_version: 5.34.1
app_file: app.py
pinned: True

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

## Contributing

Contributions are welcome! Please feel free to submit a pull request.
