# 💬 WhatsApp Chat Analysis

## Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Pipeline Highlights](#pipeline-highlights)
    - [Data Ingestion](#data-ingestion)
    - [Text Cleaning](#text-cleaning)
    - [Feature Engineering](#feature-engineering)
    - [NLP Preprocessing](#nlp-preprocessing)
    - [Visualizations](#visualizations)
    - [Export Outputs](#export-outputs)
4. [Libraries & Tools](#libraries--tools)
5. [Setup & Installation](#setup--installation)
6. [Real-World Application](#real-world-application)
7. [Conclusion](#conclusion)
8. [Portfolio and Contact](#portfolio-and-contact)

## Overview

This repository demonstrates my ability to apply Python for real-world data analysis — transforming raw WhatsApp chat exports into structured behavioral insights. The project covers the full data pipeline: ingestion, cleaning, NLP preprocessing, feature engineering, and visualization. It was built around a Brazilian Portuguese group chat, with multilingual NLP support and an optional topic modeling layer using BERTopic.

## Key Features

- End-to-end pipeline from raw `.txt` export to structured insights
- Custom NLP cleaning tailored for informal, multilingual chat data
- Emoji extraction, emoticon normalization, and frequency analysis
- Message frequency and behavioral pattern analysis per user
- Word cloud generation after Portuguese stopword removal
- Optional topic modeling with BERTopic (multilingual)
- Modular structure with two script versions showing project evolution

## Pipeline Highlights

### Data Ingestion
I parse the raw WhatsApp export directly into a structured DataFrame using `whatstk`:

```python
from whatstk import WhatsAppChat

chat = WhatsAppChat.from_source(filepath="your_chat.txt", auto_header=True).df
print(chat.head())
```

This produces a clean table with `username`, `date`, and `message` columns as the foundation for all downstream analysis.

### Text Cleaning
A custom `clean_text()` function handles the noise specific to chat data:

```python
def clean_text(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.replace('<Media omitted>', '').replace('This message was deleted', '')
    text = re.sub(r'(https?://\S+|www\.\S+)', '', text)  # Remove URLs
    text = re.sub(r'[0-9]+', '', text)                   # Remove numbers
    text = re.sub(r'\s+', ' ', text)                     # Normalize whitespace
    return text.lower().strip()
```

Emojis are intentionally preserved through the cleaning process and extracted separately for analysis.

### Feature Engineering
Key time and content features are derived directly from the parsed DataFrame:

```python
chat['emoji'] = chat['message'].apply(lambda x: ''.join(c for c in x if c in emoji.EMOJI_DATA))
chat['hour'] = chat['date'].dt.hour
chat['day_name'] = chat['date'].dt.day_name()
chat['week'] = (chat['date'] - pd.Timestamp('2024-01-01')).dt.days // 7
chat['message_length'] = chat['message'].apply(lambda x: len(x.split()) if x != '<Media omitted>' else 0)
```

### NLP Preprocessing
Portuguese stopwords from NLTK are combined with custom chat-specific terms and applied to the cleaned messages:

```python
from nltk.corpus import stopwords

stop_words = stopwords.words('portuguese')
custom_stopwords = ['nao', 'pra', 'ta', 'vc', 'vai', 'ja', 'q', 'gente', 'hahaha']
stop_words.extend(custom_stopwords)

chat['clean_msg'] = chat['clean_msg'].apply(
    lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words])
)
```

### Visualizations
The project produces six distinct visualizations:

- **Donut chart** — share of messages with vs. without emojis
- **Emoji bar chart** — top 5 most used emojis across the chat
- **Message count bar chart** — total messages per user
- **Word cloud** — most frequent words after stopword removal
- **Line chart (overall)** — message frequency by day of the week
- **Line chart (per user)** — per-user message patterns across the week
- **Heatmap** *(v8.49)* — message density by user and date using `seaborn`

### Export Outputs
All key datasets are exported as tab-separated `.txt` files for downstream use:

| File | Contents |
|---|---|
| `chat.txt` | Full cleaned chat DataFrame |
| `day_name_counts.txt` | Message count by weekday and user |
| `average_message_length.txt` | Average word count per user |
| `emoji_user_dataset.txt` | All (username, emoji) pairs |
| `chat_summary_by_name_and_date.csv` | Messages and word count per user per day |

## Libraries & Tools

| Library | Purpose |
|---|---|
| `whatstk` | Parse WhatsApp `.txt` exports into a DataFrame |
| `pandas` | Data manipulation and aggregation |
| `emoji` | Emoji extraction and demojization |
| `emot` | Text emoticon detection |
| `matplotlib` | Bar charts, line charts, pie/donut charts |
| `seaborn` | Heatmap visualization |
| `nltk` | Portuguese stopword removal |
| `wordcloud` | Word frequency visualization |
| `bertopic` *(optional)* | Automatic topic modeling |
| `umap-learn` *(optional)* | Dimensionality reduction for BERTopic |

## Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/FelipeLeiteDS/WhatsApp-Chat-Analysis.git
cd WhatsApp-Chat-Analysis
```

**2. Install dependencies**
```bash
pip install whatstk emoji emot pandas matplotlib seaborn nltk wordcloud bertopic umap-learn
```

**3. Download NLTK stopwords**
```python
import nltk
nltk.download('stopwords')
```

**4. Export your WhatsApp chat**
- Open the chat in WhatsApp → ⋮ Menu → More → Export Chat → Without Media
- Save the `.txt` file locally

**5. Update the file path**
```python
chat = WhatsAppChat.from_source(filepath=r"YOUR\PATH\TO\chat.txt", auto_header=True).df
```

> **Note:** Two script versions are included. `v8.49` is the most complete, adding the seaborn heatmap and a cleaner import structure. Start there.

## Real-World Application

This project has demonstrated practical value across several dimensions of data work:

- Extracting behavioral patterns from unstructured, informal text at scale
- Applying NLP preprocessing to non-English, low-formality language
- Building reproducible data pipelines from raw export to visual output
- Structuring exploratory analysis for presentation to both technical and non-technical audiences
- Laying the groundwork for topic modeling and conversational AI use cases

## Conclusion

This project reflects my approach to data analysis: start with messy, real-world data, build a robust cleaning and processing pipeline, and surface insights that are both technically sound and visually accessible. It demonstrates applied skills in Python, NLP, data visualization, and pipeline design — all grounded in a genuinely interesting dataset.

## Portfolio and Contact

Explore my work and connect with me:

<div> 
  <a href="https://linktr.ee/FelipeLeiteDS"><img src="https://img.shields.io/badge/LinkTree-1de9b6?logo=linktree&logoColor=white" target="_blank"></a>
  <a href="https://www.linkedin.com/in/felipeleiteds/" target="_blank"><img src="https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff" target="_blank"></a>
  <a href="https://www.felipeleite.ca"><img src="https://img.shields.io/badge/FelipeLeite.ca-%23000000.svg?logo=wix&logoColor=white" target="_blank"></a>
  <a href="mailto:felipe.nog.leite@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?logo=gmail&logoColor=white" target="_blank"></a>
</div>
