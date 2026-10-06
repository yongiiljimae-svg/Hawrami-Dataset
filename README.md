# Hawrami-Dataset

# Hawrami Language Dataset (هۆرامی)

An open-source, community-verified parallel dataset designed to preserve, standardize, and advance Natural Language Processing (NLP) and Machine Learning research for the **Hawrami (Gorani / Kurdish)** language.

---

## 📌 Overview

Hawrami is an endangered Northwestern Iranian language spoken primarily in the Hawraman region of Kurdistan (across western Iran and northeastern Iraq). Due to the scarcity of structured digital corpora, this repository provides clean, structured, and linguistically categorized data collected via native speaker contributions and strict community review workflows.

All records in this repository are crowdsourced, dialect-tagged, and validated by native speakers before inclusion.

---

## 📂 Dataset Structure

Data is stored in standardized, UTF-8 encoded CSV files inside the `dataset/` directory:

### 1. `vocabulary.csv`
Contains single words and compound terms with grammatical annotations:
* `id`: Unique identifier
* `category`: Thematic category (e.g., Nature, Home, Daily Life)
* `word_hac`: Hawrami word (written in Sorani-based Kurdish orthography: ە, ێ, ۆ, ڕ, ڵ)
* `word_fa`: Persian translation
* `word_type`: Part of speech (noun, verb, adjective, etc.)
* `dialect`: Sub-dialect region (e.g., Hawraman Takht, Luhon, Zhalanayi)
* `gender`: Grammatical gender distinction where applicable
* `example_hac`: Contextual usage sentence in Hawrami
* `example_fa`: Persian translation of the context sentence

### 2. `sentences.csv`
Parallel sentence pairs for Machine Translation (MT) and linguistic analysis:
* `id`: Sentence record identifier
* `fa_text`: Persian source sentence
* `hac_translation`: Hawrami target translation
* `dialect`: Dialect tag of the contributor
* `variations`: Associated morphological and grammatical markers

### 3. `literary_texts.csv`
High-register literary excerpts, classical poetry stanzas, and cultural expressions:
* `id`: Unique text identifier
* `fa_text`: Persian literary source text
* `hac_translation`: Literary Hawrami translation
* `dialect`: Dialect classification

---

## 🔄 Verification & Automation Pipeline

1. **Crowdsourcing**: Data is submitted through an interactive Telegram bot platform.
2. **Community Consensus**: Submissions enter a public verification queue where native speakers vote on translation accuracy, spelling, and dialect consistency.
3. **Automated Synchronization**: A daily GitHub Actions pipeline extracts entries meeting the required consensus threshold, formats them into the CSV files, and commits the updates automatically.

---

## 🚀 Use Cases

* **Machine Translation (MT)**: Low-resource parallel corpora for sequence-to-sequence translation models.
* **Large Language Models (LLMs)**: Pre-training and fine-tuning corpora for Kurdish and Iranian regional language understanding.
* **Speech Technology**: Baseline data for Automatic Speech Recognition (ASR) and Text-to-Speech (TTS) alignment.
* **Digital Preservation**: Creating verifiable open access to Hawrami linguistic heritage.

---

## 📄 License

This dataset is distributed under the **MIT License**. See the `LICENSE` file for details. Academic researchers, language developers, and AI teams are welcome to utilize this repository for non-commercial and commercial research purposes with proper attribution.
