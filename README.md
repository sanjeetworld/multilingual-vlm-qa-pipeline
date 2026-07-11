# ChitraBhasha VQA Pipeline

A scalable Vision Language Model (VLM) pipeline for generating multilingual Visual Question Answering (VQA) datasets from images using state-of-the-art Vision Language Models.

---

## Overview

This project automates the generation of high-quality Question-Answer (QA) pairs for image datasets. It supports multilingual, code-switched, and transliteration-aware question answering, making it suitable for building and evaluating Vision Language Models on Indian language datasets.

The pipeline is designed for large-scale dataset processing with features such as image validation, checkpointing, parallel image loading, and automated QA generation.

---

## Features

- Automated Visual Question-Answer generation
- Multilingual QA generation
- Code-Switched QA generation
- Transliteration-Aware QA generation
- Large-scale dataset processing
- Parallel image loading
- Dataset validation
- Automatic checkpoint recovery
- Missing image detection
- Batch inference support
- Google Colab compatible
- Hugging Face model support

---

## Project Structure

```
chitrabhasha-vqa-pipeline/
│
├── main.py
├── processor.py
├── image_mapper.py
├── dataset_validator.py
├── qa_generator.py
├── model_handler.py
├── checkpoint_manager.py
├── config.py
├── prompts.py
│
├── data/
│   ├── sample.jsonl
│   └── sample_images/
│
├── output/
│
├── checkpoints/
│
├── notebooks/
│
├── docs/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Dataset Format

Each JSONL record contains metadata and an image reference.

Example:

```json
{
  "id": "arc_0000017",
  "image_url": "https://example.com/image.png.webp",
  "caption": "...",
  "metadata": {}
}
```

---

## Generated Output

Each processed record is enriched with three QA pairs.

```json
{
  "code_switched_qa": {
    "question": "...",
    "answer": "..."
  },
  "transliteration_qa": {
    "question": "...",
    "answer": "..."
  },
  "indic_qa": {
    "question": "...",
    "answer": "..."
  }
}
```

---

## Supported Models

- Qwen2.5-VL
- Llama 3.2 Vision
- Other Hugging Face Vision Language Models

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/chitrabhasha-vqa-pipeline.git
```

Move into the project:

```bash
cd chitrabhasha-vqa-pipeline
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the pipeline:

```bash
python main.py \
  --input_jsonl data/sample.jsonl \
  --image_folder data/sample_images \
  --output_jsonl output/output.jsonl \
  --model_name qwen \
  --batch_size 2
```

---

## Workflow

1. Load JSONL dataset
2. Validate dataset
3. Map images
4. Load images
5. Generate QA using Vision Language Model
6. Save generated output
7. Save checkpoints
8. Resume automatically if interrupted

---

## Technologies Used

- Python
- Hugging Face Transformers
- PyTorch
- Pillow
- Google Colab
- JSONL
- Vision Language Models (VLM)

---

## Research Focus

This project explores multilingual Vision Language Models for generating high-quality Visual Question Answering datasets in Indian languages, including:

- Multilingual QA
- Code-Switched QA
- Transliteration-Aware QA
- Large-scale image dataset processing

---

## Future Improvements

- Support additional VLMs
- Improved image mapping
- Distributed inference
- Faster batch processing
- Web interface
- Dataset analytics dashboard

---

## Disclaimer

This repository contains the processing pipeline only. Large datasets, pretrained model weights, and generated outputs are not included.

---

## License

This project is released under the MIT License.

---

## Author

**Sanjeet Kumar**

B.Tech CSE (AI & ML)

Research Intern

Artificial Intelligence • Computer Vision • Vision Language Models • Machine Learning

---

## Acknowledgements

- Hugging Face
- PyTorch
- Vision Language Model Community
- ChitraBhasha Dataset Contributors
