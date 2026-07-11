![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)
![Google Colab](https://img.shields.io/badge/Google-Colab-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

# ChitraBhasha VQA Pipeline

A Google Colab-based Vision Language Model (VLM) pipeline for generating multilingual, code-switched, and transliteration-aware Visual Question Answering (VQA) datasets from images using **Qwen2.5-VL**.

---

## 📖 Overview

ChitraBhasha automates VQA dataset generation for Indian languages. Given an image and its metadata, the pipeline generates three types of question-answer pairs, enabling researchers to train and evaluate Vision Language Models (VLMs) across India's linguistic diversity.

---

## 🚀 Features

- **Code-Switched QA** — Questions and answers mixing English with an Indian language.
- **Transliteration-Aware QA** — Romanized script while preserving native pronunciation.
- **Indic Language QA** — Questions and answers entirely in a regional language using its native script.
- Automatic checkpointing and resume-on-interruption.
- Image ID-to-filename matching.
- Batch-wise JSONL processing.
- Google Colab and Google Drive compatible.

---

## 📂 Dataset Format (Input)

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

## 🤖 Model

- Qwen2.5-VL-3B-Instruct
- Qwen2.5-VL-7B-Instruct

Framework:
- Hugging Face Transformers

---

## ⚙️ Workflow

1. Unzip image batch.
2. Install dependencies.
3. Load the JSONL dataset and build an ID lookup.
4. Load the Qwen2.5-VL model.
5. Match each image to its corresponding record.
6. Run inference and generate QA pairs.
7. Parse the structured output.
8. Save results after every image (auto-resume).
9. Download the final JSON output.

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python main.py \
  --input_jsonl data/sample.jsonl \
  --image_folder data/images \
  --output_jsonl output/output.jsonl
```

---

## 🛠 Technologies

- Python
- PyTorch
- Hugging Face Transformers
- Pillow
- Google Colab
- JSONL
- Accelerate
- Qwen-VL-Utils

---

## 👨‍💻 Author

**Sanjeet Kumar**  
B.Tech CSE (AI & ML) | Research Intern

GitHub: https://github.com/sanjeetworld

---

## 📄 License

This project is licensed under the MIT License.
