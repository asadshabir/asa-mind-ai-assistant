# 🤖 ASA-Mind – Your Emotional, Multilingual, Book-Powered AI Assistant

ASA-Mind is an intelligent, emotion-rich, and Islamic-aware AI chatbot assistant — created by 💡 **Asad Shabir**. It uses OpenAI Agents SDK + Chainlit to answer Islamic, coding, translation, and motivational queries in **Urdu**, **Sindhi**, and **English** — with beautiful JSON references, emoji-rich style, and soul-based responses.

![ASA-Mind Screenshot](creator_image.jpg)

---

## 🌟 Features

✅ Built using **OpenAI Agents SDK + Chainlit**  
✅ Answers Islamic questions (Shia + Sunni) with book references (in Urdu/Sindhi JSON)  
✅ Understands and replies in 3 languages: **Sindhi, Urdu, English**  
✅ Detects code & fixes bugs (Python, JS, C++, etc.)  
✅ Suggests web design stacks like React, Tailwind CSS  
✅ Returns emotional **motivational quotes** based on mood  
✅ Translates any language text with tone & emojis  
✅ Protects creator’s identity with a special tool  
✅ Friendly, proud, emotional — never robotic  
✅ ✅ Has **API Key fallback** logic to switch automatically if one fails  

---

## 🧠 How it Works — OpenAI Agents SDK

This AI runs on top of the **[OpenAI Agents SDK](https://github.com/openai/agents)** and uses:

- 🧱 `Agent` class for every personality/role  
- 🔧 `function_tool` decorators for callable tools  
- ⚙️ `RunConfig`, `ModelSettings` to control behavior  
- 🤖 `Runner.run_streamed()` from Chainlit to stream messages
- 🗝️ **Fallback key setup**: If primary key fails, it auto-uses the backup!

Each Agent (like `ShiaAgent`, `CodingFixer`, `SindhiAgent`, etc.) has its own behavior, model, and tools defined.

---

## 🔧 Tools & Agents Overview

| Agent Name       | Role / Purpose |
|------------------|----------------|
| `main_agent`     | ASA-Mind brain: routes to right sub-agent silently |
| `ShiaAgent`      | Islamic Q&A in fluent Urdu/Sindhi with JSON proof |
| `CoderAgent`     | Code fixing (Python, JS, TS, C++, etc.) |
| `DeveloperAgent` | Helps build websites, selects tech stack |
| `SindhiAgent`    | Speaks only in Sindhi language (natural & cultural) |
| `TranslaterAgent`| Translates any text to Urdu, Sindhi, English |
| `QuotesAgent`    | Sends motivational quotes based on mood |
| `CreatorTool`    | Returns full info + photo of Asad Shabir (creator) |

---

## 📦 Tech Stack

- ✅ **Python 3.11+**
- ✅ **Chainlit** (for frontend UI + streaming)
- ✅ **OpenAI Agents SDK**
- ✅ **AsyncOpenAI** client wrapper
- ✅ **Dotenv** for secure `.env` key handling
- ✅ **Railway.app or any Python cloud host**

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/asadshabir/asa-mind.git
cd asa-mind

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
chainlit run main.py -w

🧔 About the Creator
👨‍💻 Asad Shabir
Agentic AI Dev | Python Instructor | Muslim Tech Activist
🏠 Sehwan, Sindh, Pakistan
📧 asadshabir505@gmail.com
📞 03253939049
📸 [creator_image.jpg]

📜 License
MIT License — free to use with ❤️
Please credit Asad Shabir if you reuse the code.