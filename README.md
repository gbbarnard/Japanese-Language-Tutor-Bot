# Japanese Language Tutor Bot 🇯🇵

Author: **Gavin Barnard**  
Course: **CSI-4130 – Artificial Intelligence**  
Date: **Fall 2025**

---

## 1. Project Overview

The **Japanese Language Tutor Bot** is a small web app that helps beginners understand and pronounce Japanese sentences.

You type an **English sentence**, and the app returns:

- ✅ A natural **Japanese translation**
- 🔡 **Romaji** and a **syllable-style romaji breakdown**
- 🏷️ An approximate **JLPT level** (N5–N1)
- 🧩 Short **grammar and vocabulary explanations** in simple English
- 🔊 **Audio** for:
  - the **full Japanese sentence**, and  
  - each **key word / phrase** from the explanation

The goal is to act like a mini-tutor that you can quickly ask:

> “How do I say this in Japanese, how hard is it, and how do I pronounce it?”

---

## 2. Problem Statement

Learning Japanese is difficult for English speakers because of:

- Three writing systems (hiragana, katakana, kanji)  
- Different word order  
- Small particles like **は, が, を, に, で** that change sentence meaning  
- Verb endings like **～ます** that can feel confusing  

Most tools (textbooks, flashcards, fixed apps) have limitations:

- They show **pre-written example sentences** instead of sentences the learner actually wants.  
- Explanations are often long or hard to understand.  
- Pronunciation practice is limited or missing.

This project explores whether a simple **LLM + text-to-speech** app can:

1. Give **instant translations** of any English sentence the learner types.  
2. Provide short, clear **grammar and vocabulary explanations**.  
3. Let the learner **hear** both the full sentence and important words.

---

## 3. Solution Overview

The app is built with:

- **Streamlit** for the web interface  
- **Cohere’s Command-R (command-r-08-2024)** as the Large Language Model  
- **gTTS** for Japanese text-to-speech (`lang="ja"`)  
- **python-dotenv** to securely load the `COHERE_API_KEY` from `.env`

### What happens when you type a sentence?

1. You enter an English sentence in the chat box.  
2. The app builds a prompt and sends it to **Cohere Command-R**.  
3. The model responds in a fixed format:

   ```text
   Japanese: ...
   Romaji: ...
   Romaji breakdown: ...
   JLPT: ...
   Explanation:
   - 日本語 (ni•hon•go): means "Japanese language".
   - ...
The app parses that response and displays it nicely in the UI.

The app calls gTTS to create:

one audio clip for the whole sentence, and

shorter clips for each key word / phrase mentioned in the explanation bullets.

## 4. How It Works (High Level)
**Front-end (Streamlit)**

- Chat-style layout: user messages on one side, tutor messages on the other.

- Custom CSS in Styles/style.css for a light, Japanese-inspired theme.

**Backend Logic**

- Load COHERE_API_KEY from .env.

- Create ClientV2 from the Cohere Python SDK.

- On each user message:

- Build a prompt describing the tutor’s role and required output format.

- Call co.chat(model="command-r-08-2024", ...).

- Parse the lines for Japanese:, Romaji:, Romaji breakdown:, JLPT:, and Explanation: bullets.

**Audio (Text-to-Speech)**

- Helper function japanese_tts(text) uses gTTS(text, lang="ja").

- Streamlit’s st.audio(...) plays:

- full-sentence audio

- word-level audio for each explanation bullet

 ## 5. Setup & Running the App
**5.1. Clone the repository**
- git clone https://github.com/gbbarnard/Japanese-Language-Tutor-Bot.git
- cd Japanese-Language-Tutor-Bot

**5.2. Create and activate a virtual environment (optional but recommended)**
- python -m venv venv

# Windows
- venv\Scripts\activate

# macOS / Linux
- source venv/bin/activate

**5.3. Install dependencies**
pip install -r requirements.txt

**5.4. Set up API key**

Create a file named .env in the project root:

-COHERE_API_KEY=your_real_cohere_api_key_here

If you dont want to get a key from Cohere, Request mine

**5.5. Run the app**
-streamlit run app.py
