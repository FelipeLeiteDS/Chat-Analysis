# 💬 WhatsApp Chat Analysis

A Python project for analyzing WhatsApp group or personal chat exports — extracting behavioral patterns, emoji usage, message frequency, word clouds, and more. Built for exploratory data analysis with full NLP preprocessing in Brazilian Portuguese.

---

## 📌 Overview

This project takes a raw WhatsApp chat export (`.txt`) and transforms it into structured insights through data cleaning, feature engineering, visualization, and optional topic modeling. It is designed to work with multi-user group chats and handles Portuguese-language stopwords natively.

---

## 📊 What It Analyzes

- **Message frequency** — who sends the most messages and when
- **Emoji usage** — top emojis overall and per user, with donut chart visualization
- **Emoticon detection** — converts text emoticons (`:)`, `:(`) to emoji equivalents
- **Word cloud** — most frequent words after full NLP cleaning and stopword removal
- **Day-of-week patterns** — message frequency by weekday, overall and per user
- **Average message length** — word count per user
- **User activity heatmap** — message density across users and dates
- **Topic modeling** *(commented out — optional)* — BERTopic with multilingual support for automatic topic discovery

---

## 🗂️ Repository Structure

```
WhatsApp-Chat-Analysis/
├── whatsapp project_final_4.55.py   ← Earlier version (no heatmap, no seaborn)
├── whatsapp project_final_8.49.py   ← Latest version (full pipeline + heatmap)
└── README.md
```

> **Note:** The two script versions reflect the project's evolution. Version 8.49 is the most complete and recommended starting point.

---

## 🛠️ Libraries & Tools

| Library | Purpose |
|---|---|
| `whatstk` | Parse WhatsApp `.txt` exports into a structured DataFrame |
| `pandas` | Data manipulation and aggregation |
| `emoji` | Emoji extraction and demojization |
| `emot` | Text emoticon detection |
| `matplotlib` | Bar charts, line charts, pie/donut charts |
| `seaborn` | Heatmap visualization |
| `nltk` | Portuguese stopword removal |
| `wordcloud` | Word frequency visualization |
| `re` / `unicodedata` | Text cleaning and normalization |
| `bertopic` *(optional)* | Topic modeling |
| `umap-learn` *(optional)* | Dimensionality reduction for BERTopic |

---

## ⚙️ Setup & Installation

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
- Save the `.txt` file to your machine

**5. Update the file path in the script**
```python
chat = WhatsAppChat.from_source(filepath=r"YOUR\PATH\TO\chat.txt", auto_header=True).df
```

---

## 🔄 Pipeline Overview

```
Raw .txt export
      │
      ▼
Parse with whatstk → DataFrame (username, date, message)
      │
      ▼
Clean text → remove URLs, media placeholders, numbers, special characters
      │
      ▼
Feature engineering → emoji column, hour, day_name, week, message_length
      │
      ▼
NLP preprocessing → demojize, remove Portuguese stopwords
      │
      ▼
Aggregations → stats per user, per day, per emoji
      │
      ▼
Visualizations → bar charts, line charts, donut chart, word cloud, heatmap
      │
      ▼
Export → .txt / .csv outputs per dataset
```

---

## 📤 Outputs

The script exports the following files (update paths to your own machine):

| File | Contents |
|---|---|
| `chat.txt` | Full cleaned chat DataFrame |
| `day_name_counts.txt` | Message count by day of week and user |
| `average_message_length.txt` | Average word count per user |
| `emoji_user_dataset.txt` | All (username, emoji) pairs |
| `chat_summary_by_name_and_date.csv` | Messages and word count per user per day |

---

## 🔧 Customization

**Adding custom stopwords** — extend the list in the script to filter out chat-specific filler words:
```python
custom_stopwords = ['nao', 'pra', 'ta', 'vc', 'vai', 'ja', 'q', 'aqui', 'ai', 'gente']
```

**Enabling topic modeling** — uncomment the BERTopic block at the bottom of the script to run automatic topic discovery across messages.

**Enabling the heatmap** — available in version 8.49, using `seaborn` to visualize message density by user and date.

---

## 🚧 Known Limitations

- File path in the script is hardcoded for Windows — update it for your OS before running
- BERTopic and heatmap sections are commented out by default; enable them manually
- Chat format may vary slightly between WhatsApp versions — `auto_header=True` handles most cases

---

## 👤 Author

**Felipe Leite**
[GitHub](https://github.com/FelipeLeiteDS)

---

## 📄 License

This project is open source and available for personal and educational use.
