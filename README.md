![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)
![Google Colab](https://img.shields.io/badge/Google-Colab-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

# ChitraBhasha VQA Pipeline

A Google Colab-based Vision Language Model (VLM) pipeline for generating multilingual Visual Question Answering (VQA) datasets using **Qwen2.5-VL**. The pipeline automatically processes image datasets and generates high-quality question-answer pairs in multiple language formats.

---

## 🚀 Features

- Multilingual Visual Question Answering (VQA)
- Code-Switched QA Generation
- Transliteration-Aware QA Generation
- Indic Language QA Generation
- Automatic checkpointing and resume support
- Batch image processing
- JSONL input/output support
- Google Drive integration
- Google Colab compatible

---

## 📂 Dataset Format

Input JSONL

```json
{
  "id": "cul_0000017",
  "image_url": "https://example.com/image.png",
  "caption": "..."
}
```

---

## 📤 Output Format

```json
{
  "id": "cul_0000017",
  "code_switched_q": "...",
  "code_switched_a": "...",
  "transliteration_q": "...",
  "transliteration_a": "...",
  "indic_language": "...",
  "indic_q": "...",
  "indic_a": "..."
}
```

---

## 🤖 Model Used

- Qwen2.5-VL-3B-Instruct
- Qwen2.5-VL-7B-Instruct

Framework:
- Hugging Face Transformers
- PyTorch

---

## ⚙️ Workflow

1. Install required dependencies
2. Mount Google Drive
3. Load JSONL dataset
4. Build ID-based image mapping
5. Load Qwen2.5-VL model
6. Process images batch-wise
7. Generate multilingual QA pairs
8. Save output automatically
9. Resume processing from checkpoints if interrupted

---

## 🛠 Technologies Used

- Python
- Google Colab
- Hugging Face Transformers
- PyTorch
- Pillow
- JSONL
- Accelerate
- Qwen-VL-Utils

---

## 📁 Repository Structure

```
ChitraBhasha-VQA-Pipeline
│
├── main.py
├── processor.py
├── image_mapper.py
├── qa_generator.py
├── checkpoint_manager.py
├── config.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the pipeline in Google Colab or Python.

```bash
python main.py
```

---

## 📌 Applications

- Vision Language Models (VLM)
- Multilingual AI
- Visual Question Answering
- Indic Language Research
- Dataset Generation
- AI Research

---

## 👨‍💻 Author

**Sanjeet Kumar**

B.Tech – Computer Science & Engineering (AI & ML)

Research Intern

GitHub: https://github.com/sanjeetworld

---

## 📄 License

This project is licensed under the MIT License.
