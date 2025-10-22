# **Multimodal RAG-Based Food Recommendation System**

A production-style, portfolio-ready implementation of a **Multimodal Retrieval-Augmented Generation (RAG)** recommender that understands **text + images** to deliver **personalized, context-aware food recommendations** for a restaurant aggregator use-case.

---

## 🧠 Overview

Traditional recommenders depend only on text. This project augments retrieval with **visual semantics** using Amazon Bedrock models and stores dense vectors in **FAISS** for sub-second similarity search. The **Streamlit** app provides an interactive chat experience that accepts **text or image queries** and returns grounded recommendations.

---

## 🏗️ Architecture
<img width="485" height="375" alt="architecture_diagram" src="https://github.com/user-attachments/assets/8e5b810a-4f8d-4ba8-a350-bb58e2029ab2" />


**Flow (high-level)**

1. **Amazon S3** holds menu images + metadata (CSV).  
2. **Claude Sonnet (Multimodal)** summarizes images (captions, attributes).  
3. **Titan Text Embeddings v2** encodes text/image summaries → vectors.  
4. **FAISS** stores and retrieves vectors (ANN search).  
5. **Streamlit** UI sends user query (text/image) → retrieves top-K →  
   **Claude Sonnet** crafts conversational, grounded recommendations.

---

## 🎯 Objectives

- Build a **multimodal** RAG pipeline (text + images).  
- Use **AWS Bedrock** for summarization and embeddings.  
- Store & serve vectors with **FAISS**.  
- Deliver an **interactive Streamlit** experience for search & recommendations.

---

## ✨ Features

- Text and image query support (multimodal input).  
- Bedrock-powered summarization and embeddings.  
- Fast vector search with FAISS (local).  
- Clean, minimal **Streamlit** UI with chat-style responses.  
- Easily portable to S3/EC2 for cloud deployment.

---

## ⚙️ Tech Stack

- **Language:** Python `3.10.4`  
- **Libraries:** `boto3`, `awscli`, `pandas`, `faiss-cpu`, `langchain`, `langchain-community`, `streamlit`, `streamlit-chat`  
- **Models (Bedrock):**  
  - **Claude Sonnet (Multimodal)** — image reasoning & response generation  
  - **Titan Text Embeddings v2** — dense vector embeddings  
- **Storage:** Amazon **S3**  
- **Vector DB:** **FAISS** (CPU)  
- **UI:** **Streamlit**

---

## 🧩 Data

- **CSV metadata:** menu names, cuisines, nutrition, dietary tags, image paths, ratings, price, etc.  
- **Images folder:** dish/restaurant images aligned with CSV rows.

> You can store the data in **S3** or load it locally during development.

---

## 📦 Project Structure

```bash
├─ app.py                          # Streamlit app (UI + orchestration)
├─ utils.py                        # Helper functions (I/O, encode, retrieve)
├─ data/
│  ├─ images/                      # Menu images
│  ├─ menu_descriptions_data.csv   # Generated/cleaned captions/descriptions
│  └─ restaurants_menu_data.csv    # Raw menu metadata
├─ output/
│  └─ faiss_index/                 # Persisted FAISS index (built at setup)
├─ multimodal-llm.ipynb            # Notebook (experiments / quick tests)
├─ Multimodal RAG Presentation.pdf # Slides for overview
├─ reference-images/               # Support images for README/app
├─ requirements.txt
└─ README.md

---

### **For macOS / Linux**
```bash
cd /path/to/project
python3.10 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
