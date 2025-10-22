# **Multimodal RAG-Based Food Recommendation System**

A production-style, portfolio-ready implementation of a **Multimodal Retrieval-Augmented Generation (RAG)** recommender that understands **text + images** to deliver **personalized, context-aware food recommendations** for a restaurant aggregator use-case.

---

## 🧠 Overview

Traditional recommenders depend only on text. This project augments retrieval with **visual semantics** using Amazon Bedrock models and stores dense vectors in **FAISS** for sub-second similarity search. The **Streamlit** app provides an interactive chat experience that accepts **text or image queries** and returns grounded recommendations.

---

## 🏗️ Architecture

> **Place your architecture diagram image here** (e.g., `![Architecture](./docs/architecture.png)`)

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


---

## 🧭 Prerequisites

- Active **AWS account** with permissions for **Bedrock** + **S3**.  
- **AWS CLI** installed and configured locally.  
- Python **3.10.4** available on your machine.  
- (Optional) EC2 access for cloud deployment.

---

## 1) 🔑 Request Model Access on **AWS Bedrock**

1. Log in to the **[AWS Management Console](https://aws.amazon.com/console)**.  
2. Search **“Bedrock”** → **Get Started**.  
3. Left nav → **Manage model access**.  
4. Select these models (ensure your region supports them, e.g., `us-east-1`):
   - **Titan Text Embeddings v2**  
   - **Claude Sonnet (Multimodal)**
5. Click **Request model access** and wait for status to become **Granted**.

> _Screenshot placeholders (optional):_  
> `![Bedrock Getting Started](reference-images/aws-bedrock/1.png)`  
> `![Manage Model Access](reference-images/aws-bedrock/2.png)`

---

## 2) 🗂️ Data Setup — S3 or Local

### A) Using **Amazon S3**
1. Open **S3** → **Create bucket** (unique name, correct region).  
2. **Upload**:
   - `restaurants_menu_data.csv`
   - `menu_descriptions_data.csv` (or generate later)
   - `images/` folder

### B) Using **Local Folders**
- Mirror the structure under `data/` and point your app config to local paths.

---

## 3) 🐍 Environment Setup (Virtual Env)

> **Python version:** 3.10.4

### Windows
```bash
cd C:\path\to\project
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt


