# Japanese Language Tutor Bot

#**Project Overview**

  The Japanese Language Tutor Bot is an AI-powered conversational learning tool designed to help users practice and improve their Japanese language skills.  
It uses a Large Language Model (LLM) to engage in realistic dialogues, correct grammar and vocabulary errors, and explain mistakes in simple English.  

Unlike static language-learning apps, this tutor adapts to the learner’s ability.  
As users make progress, the system automatically adjusts sentence complexity and grammar difficulty based on JLPT (Japanese-Language Proficiency Test) levels.  
Session data are logged for progress visualization and analysis.

#**Problem Statement**

 Traditional language apps rely on pre-set questions and fixed feedback, offering little personalization.  
Learners of Japanese often struggle with context, verb conjugation, and particle usage, making feedback essential.

This project explores whether a conversational AI tutor can:
- Provide instant feedback and correction in real time,  
- Offer brief, human-like explanations, and  
- Adapt its difficulty dynamically to learner performance.  

#**Proposed Method**

 1. **LLM-Driven Conversation Engine**  
   - Build a Streamlit chat interface for Japanese dialogue.  
   - Connect to an Cohere’s Aya / Command-R model via Cohere’s Chat v2 API.  
   - Maintain multi-turn conversations within daily-life topics.

2. **Grammar Correction & Feedback**  
The system analyzes each learner message to detect common errors, such as:
  - particle misuse (は / が / を / に)
  - incorrect verb form
  - unnatural phrasing
  - missing or incorrect politeness levels
    
The response includes:
  - a corrected version
  - an English explanation
  - optional JLPT grammar notes
Feedback is returned in a structured format for consistent display.

3. **Adaptive Difficulty**  
   - Track mastery scores (0 – 100) per grammar category.    
   - Adjust grammar and vocabulary difficulty automatically.

4. **Session Logging & Visualization**  
   - Log each exchange as JSON (user input, correction, topic, mastery).  
   - Plot progress and error trends with Matplotlib / Altair.

#**Data Sources**

- Synthetic data only (generated from simulated learner sessions).  
- Stored in `/logs/sessions/` as JSON for evaluation. 
