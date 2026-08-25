# 📰 GenAI News Intelligence System

## Overview

**GenAI News Intelligence System** is a machine learning and generative AI-based application designed to analyze news articles and identify potentially fake or misleading information.

The system combines **Machine Learning, Natural Language Processing (NLP), and Generative AI** to provide fake news detection, sentiment analysis, text summarization, keyword extraction, confidence scores, and explainable predictions through an interactive Streamlit interface.

---

## 🚀 Features

* Fake News Detection using Logistic Regression
* TF-IDF based Text Feature Extraction
* Prediction Confidence Score
* Probability Breakdown
* Explainable Predictions using Feature Importance
* Sentiment Analysis
* Text Summarization
* Keyword Extraction
* Batch CSV News Analysis
* Real-Time News Analysis
* RAG-based Fact Checking
* Generative AI-powered Explanations
* Interactive Streamlit Web Interface

---

## 🧠 Tech Stack

| Category         | Technologies                      |
| ---------------- | --------------------------------- |
| Language         | Python 3.10+                      |
| Machine Learning | Scikit-learn                      |
| NLP              | NLTK, TF-IDF                      |
| Generative AI    | OpenAI, Hugging Face Transformers |
| Data Processing  | Pandas, NumPy                     |
| Frontend         | Streamlit                         |
| Backend          | FastAPI                           |
| Development      | Git, GitHub, VS Code              |

---

## 📁 Project Structure

```text
GenAI-News-Intelligence-System/
│
├── backend/
│   ├── main.py
│   ├── schemas.py
│   ├── requirements.txt
│   │
│   ├── services/
│   │   ├── fake_news_service.py
│   │   ├── rag_factcheck.py
│   │   ├── realtime_service.py
│   │   └── openai_explainer.py
│   │
│   └── .gitignore
│
├── models/
│   ├── fake_news_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── src/
│   ├── preprocess.py
│   ├── sentiment.py
│   └── summarizer.py
│
├── data/
│
├── app.py
├── requirements.txt
├── README.md
└── report.pdf
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/GenAI-News-Intelligence-System.git
cd GenAI-News-Intelligence-System
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

Add the following to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

Never commit API keys or other sensitive credentials to GitHub.

---

## ▶️ Run the Application

### Streamlit

```bash
streamlit run app.py
```

### FastAPI Backend

```bash
uvicorn backend.main:app --reload
```

---

## 🔄 System Workflow

```text
News Article
     │
     ▼
Text Preprocessing
     │
     ▼
TF-IDF Vectorization
     │
     ▼
Logistic Regression
     │
     ▼
Fake / Real Prediction
     │
     ├──► Confidence Score
     ├──► Probability Breakdown
     └──► Feature Importance
              │
              ▼
        Generative AI
              │
       ┌──────┼──────┐
       ▼      ▼      ▼
    Summary Keywords Sentiment
```

---

## 🔍 Fake News Detection

The system uses **TF-IDF vectorization** to convert news text into numerical features.

A **Logistic Regression** classifier analyzes these features and predicts whether the article is likely to be:

* **Real News**
* **Fake News**

The system also provides prediction probabilities and confidence scores to improve interpretability.

---

## 😊 Sentiment Analysis

The system analyzes the emotional tone of the news article and classifies it as:

* **Positive**
* **Neutral**
* **Negative**

---

## ✨ Generative AI

Generative AI is used to enhance news analysis through:

* Text summarization
* Keyword extraction
* Prediction explanations
* Contextual analysis
* Fact-checking assistance

---

## 📊 Batch CSV Analysis

The system supports batch processing of news articles through CSV files.

The analysis can include:

| Output     | Description                    |
| ---------- | ------------------------------ |
| Prediction | Fake or Real                   |
| Confidence | Model confidence               |
| Sentiment  | Positive, Neutral, or Negative |
| Keywords   | Important terms                |
| Summary    | Generated article summary      |

---

## 🎯 Objectives

* Detect potentially fake news using Machine Learning.
* Apply NLP techniques to analyze textual information.
* Integrate Generative AI into news intelligence.
* Provide explainable and confidence-based predictions.
* Analyze sentiment and extract important keywords.
* Provide automated summaries of news articles.
* Develop an interactive web-based news analysis platform.

---

## 🔮 Future Scope

* Advanced Transformer-based fake news detection
* Multilingual news analysis
* Improved RAG-based fact checking
* Source credibility scoring
* Real-time misinformation alerts
* Image and video misinformation detection
* Browser extension for instant news verification
* Integration with additional news and fact-checking APIs
* Cloud deployment and scalable infrastructure

---

## 👨‍💻 Author

**Prathamesh S. S. Deoghare**

B.E. Computer Science & Engineering — Data Science
Prof. Ram Meghe College of Engineering & Management, Badnera-Amravati
Sant Gadge Baba Amravati University

---

## 📜 License

This project is developed for academic, educational, and research purposes.
