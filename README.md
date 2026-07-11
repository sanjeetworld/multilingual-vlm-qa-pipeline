![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)
![Google Colab](https://img.shields.io/badge/Google-Colab-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

# Multilingual VQA Pipeline

A Google Colab-based Vision Language Model (VLM) pipeline for generating multilingual, code-switched, and transliteration-aware Visual Question Answering (VQA) datasets from images using **Qwen2.5-VL**.

---

## 📖 Overview

This pipeline automates multilingual Visual Question Answering (VQA) dataset generation. Given an image and its metadata, it generates three types of question-answer pairs to support training and evaluation of Vision Language Models (VLMs) across multiple languages.

---

## 🚀 Features

- **Code-Switched QA** — Questions and answers mixing English with another language.
- **Transliteration-Aware QA** — Romanized script while preserving native pronunciation.
- **Multilingual QA** — Questions and answers generated in native language scripts.
- Automatic checkpointing and resume-on-interruption.
- Image ID-to-filename matching.
- Batch-wise JSONL processing.
- Google Colab and Google Drive compatible.

---

## 📂 Dataset Format (Input)

```json
{
  "id": "sample_0000017",
  "image_url": "https://example.com/image.png",
  "caption": "..."
}
```

---

## 📤 Output Format

```json
{
  "id": "sample_0000017",
  "code_switched_q": "...",
  "code_switched_a": "...",
  "transliteration_q": "...",
  "transliteration_a": "...",
  "language": "...",
  "multilingual_q": "...",
  "multilingual_a": "..."
}
```

---

## 🤖 Model

- Qwen2.5-VL-3B-Instruct
- Qwen2.5-VL-7B-Instruct

**Framework**
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

GitHub: https://github.com/sanjeetworld

---

## 📄 License

This project is licensed under the MIT License.
