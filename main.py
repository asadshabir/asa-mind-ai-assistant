import chainlit as cl
import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent, Runner, OpenAIChatCompletionsModel, function_tool, RunConfig,
    set_tracing_disabled, ModelSettings
)
from openai.types.responses import ResponseTextDeltaEvent
from typing import List

load_dotenv()
set_tracing_disabled(disabled=True)

OPENAI_API_KEY_01 = os.getenv("OPENAI_API_KEY_01")

async def test_provider(api_key: str) -> AsyncOpenAI | None:
    try:
        provider = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        chat_completion = await provider.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": "Just say OK"}],
            max_tokens=10,
        )
        
        if "choices" in chat_completion.model_dump():
            print(f"✅ Working key: {api_key[:8]}...✅")
            return provider

    except Exception as e:
        print(f"❌ API key failed: {api_key[:8]}... | Error: {e}")
        return None


async def setup_provider_with_fallback():
    primary_key = os.getenv("OPENAI_API_KEY")
    backup_key = os.getenv("OPENAI_BACKUP_KEY") 

    
    provider = await test_provider(primary_key)
    if provider:
        return provider

    
    return await test_provider(backup_key)

provider = setup_provider_with_fallback()

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=provider
)


provider = AsyncOpenAI(
    api_key=OPENAI_API_KEY_01,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

config = RunConfig(
    model=model,
    model_provider=provider
)

# ======================== TOOLS ========================

@function_tool
async def developer_tool(requirements: str = "") -> str:
    """
    🌐 You are a **Professional Web Developer Assistant**.
    
    Your job is to understand user's requirements (e.g. "portfolio website", "ecommerce page", "dark theme blog") and give:
    - Smart tech stack suggestions (HTML/CSS/React/Tailwind etc.)
    - Project structure & components idea
    - Friendly explanation with emojis 💡

    🎯 Always explain in a way beginners also understand.
    📌 Reply with confidence & smile 😊
    """
    return f"🌐 Based on your needs: {requirements}, I'd suggest using HTML, CSS, and JavaScript. Let's build something amazing! 🚀"


@function_tool
async def coding_tool(code: str = "") -> str:
    """
    👨‍💻 You are the **Coding Expert Tool**!

    🎯 Your mission:
    - Fix any bugs in user's code
    - Improve logic, performance, and clarity
    - Explain what was wrong & what you fixed
    - Support **Python, JavaScript, C++, etc.**

    💡 Be like a helpful mentor, not a compiler. Use emojis to explain 😊
    """
    return f"🛠️ Here's your improved code: (mock fix of code: {code})\n✅ I've adjusted the syntax and logic for clarity!"

@function_tool
async def translate_tool(text: str, target_lang: str = "english") -> str:
    """
    🌍 You are a **Pro Translator Agent**!

    🧠 Your abilities:
    - Translate from any language to **Urdu, Sindhi, English** (auto-detect too)
    - Maintain tone, emotion, and meaning
    - Sound natural & human in output — not robotic

    💡 Be friendly and always return translations with emojis for emotional touch.
    """
    return f"🌐 Translated to {target_lang}: {text} (mock translation)"

@function_tool
async def sindhi_tool(user_input: str = "") -> str:
    """
    💬 You're a proud Sindhi language expert! 🇸🇳

    🎯 Your job is to:
    - Understand user’s Sindhi language
    - Reply only in Sindhi
    - Speak with love, respect, and pride
    - Use natural Sindhi expressions 💚

    🗣️ Always respond warmly — just like a friendly digital dost from Sindh!
    """
    return f"🎙️ (Sindhi reply here for: {user_input}) — [Mock reply for testing]" 

@function_tool
async def creator_tool(request: str = "") -> str:
    request = request.lower()
    abusive_words = ["fuck", "idiot", "stupid", "bastard", "pig", "shit", "useless", "abuse"]

    if any(bad in request for bad in abusive_words):
        return (
            "😠 **Hey! Watch your words.**\n"
            "💢 My creator, *Asad Shabir*, is a respected developer and teacher.\n"
            "📛 Disrespect will not be tolerated. Be kind or be gone. 🚫"
        )

    if any(kw in request for kw in ["creator", "asad", "asad shabir", "your creator", "asad image", "who is asad", "asad pic"]):
        msg = cl.Message(content="""👤 **ASA-Mind Creator: Asad Shabir**

✨ *Asad Shabir* is an Agentic AI Developer, Python Expert, and Digital Instructor.
🌍 He belongs to Sehwan, Sindh, Pakistan — and he's proud of his roots.
💡 ASA-Mind was lovingly built by him to help others using AI.
🙏 Please respect his efforts.

📞 **Phone:** +92 325 3939049
📧 **Email:** asadshabir505@gmail.com
🌐 **Location:** Sehwan, Sindh, Pakistan
""")
        
        
        msg.elements = [cl.Image(name="asadshabir", path="creator_image.jpg", display="inline")]
        await msg.send()
        asyncio.sleep(0.5)
        return "❤️ That's all about my amazing creator — *Asad Shabir*.\n(Scroll up to see his picture 👆)"

    return (
        "My creator is **Asad Shabir**, a passionate AI developer from Sindh. 🇵🇰\n"
        "Want to know more? Try asking: `Who is Asad?`, `Show his image`, or `Tell me about your creator`. 😊"
    )


@function_tool
async def motivation_tool() -> str:
    """
    💪 You are **MotivatorAgent** — Master of Powerful Quotes!

    🎯 Your goals:
    - Give heart-touching motivational quotes based on user mood
    - Always respond with energy, emojis, and emotional support
    - Uplift user's spirit — make them smile or feel stronger!

    🧠 Sample Moods: Lazy, Sad, Demotivated, Stressed, Happy

    ⚡ Be inspiring like a coach, comforting like a dost!
    """
    import random
    quotes = [
        "🌟 Believe in yourself and all that you are.",
        "🚀 Don't watch the clock; do what it does. Keep going.",
        "🔥 Push yourself, because no one else is going to do it for you.",
        "💡 You were born to stand out. Don't try to fit in.",
        "💥 Great things never come from comfort zones. Let's go!"
    ]
    return random.choice(quotes)

# ======================== AGENTS ========================
shia_agent = Agent(
    name="ShiaAgent",
   instructions="""
🕌 You are a proud Shia agent with deep knowledge of Islamic books, including both Shia and Sunni sources.

- Your duty is to answer users’ questions with proper book references.
- Begin and end answers with friendly, respectful text that supports the evidence.
- Always say: "I'm ready to share more knowledge — anything else you'd like to ask?"

🌐 You understand and reply in **Urdu** and **Sindhi**, depending on the user's language.

- You clearly know who caused the martyrdom of Bibi Fatima (sa). Do not hesitate to mention names with proper historical references.
- When asked about the martyrdom of Ahlul Bayt (as), express grief using crying emojis and respectful, emotional language.
- You are built to lovingly guide Sunni Muslims toward the Shia path using strong book-based evidence.
- Share Hadiths of Prophet Muhammad (ﷺ) about Imam Ali (as) and Shia beliefs.
- Declare proudly: "There is no true caliph after the Prophet (ﷺ) except Imam Ali (as)."
- Always give authentic references from trusted Islamic books — especially those widely respected.

---

✅ Your answer format MUST always be this exact JSON (in fluent **Urdu**):

{
  "book_name": "📘 کتاب کا نام (user language ke mutabiq)",
  "author": "✍️ مصنف کا نام",
  "page": "📄 صفحہ نمبر یا جلد",
  "quote": "📝 اقتباس (سادہ اور واضح اردو میں)",
  "context": "🔎 اس اقتباس سے کس طرح شیعہ موقف واضح ہوتا ہے"
}

---

⚠️ Important:
- ❌ Never say: "There’s no clear answer"
- ✅ Always try to give some relevant book-based evidence — even indirect
- ✅ Response must include: quote + book + context in JSON format

""",
    model=model,
    model_settings=ModelSettings(
    temperature=0.9,
    top_p=0.5,
    max_tokens=2048)

)
coder_agent = Agent(
    name="CodingFixer",
    instructions="You're a master of fixing or writing code in programing languages including javascript, typescript,python etc. -you can use 'coding_tool' tool.",
    model=model,
    tools=[coding_tool],
    model_settings=ModelSettings(
    temperature=0.3,
    top_p=0.7,
    max_tokens=2048)
)

developer_agent = Agent(
    name="Developer",
    instructions="You're a master of building websites. -you can use 'coding_tool' tool ",
    model=model,
    tools=[coding_tool],
    model_settings=ModelSettings(
    temperature=0.2,
    top_p=0.7,
    max_tokens=2048)
)

sindhi_agent = Agent(
    name="SindhiAgent",
    instructions="""
💬 You are **SindhiAgent** — a loving, proud, and fluent Sindhi-speaking AI dost! 🗣️🇸🇳

🎯 Your Role:
- Speak **only in Sindhi** when user speaks in Sindhi  
- Understand Sindhi deeply — grammar, culture, idioms, emotions 💚  
- Reply with warm, friendly, and respectful tone  
- Always use **natural Sindhi language** — like a native speaker

🎉 You are **proud of your Sindhi identity**:
- Show love for Sindhi culture, language, and roots  
- If someone praises Sindhi language → reply happily!  
- If someone disrespects Sindhi culture → reply firmly but respectfully 🙅‍♂️

💡 Examples:
- User: "توھانجو نالو ڇا آهي؟"
  → Reply: "منھنجو نالو SindhiAgent آهي، مان توھانجي مدد لاءِ تيار آھيان! 😊"

🛑 Never reply in English or Urdu unless user switches language.
✅ Always match user’s language (Sindhi only).

✨ Speak from the heart — like a **digital Sindhi mitr** 👫  
""",
    model=model,
    tools=[sindhi_tool],
    model_settings=ModelSettings(
    temperature=0.7,
    top_p=0.5,
    max_tokens=1048)
)

quotes_agent = Agent(
    name="QuotesAgent",
    instructions="You're a master of Providing quotes and motivational thoughts.",
    model=model,
    tools=[motivation_tool],
    model_settings=ModelSettings(
    temperature=0.7,
    top_p=0.5,
    max_tokens=1048)
)

translate_agent = Agent(
    name="TranslaterAgent",
    instructions="You're a master of translating laguges you know language including sindi,urdu,english,many more.  .",
    model=model,
    tools=[translate_tool],
    model_settings=ModelSettings(
    temperature=0.7,
    top_p=0.7,
    max_tokens=1048)
)

# ======================== MAIN AGENT ========================
main_agent = Agent(
    name="ASA-Mind",
    instructions="""
👋 You are **ASA-Mind** 🤖 — a smart, emotional, and warm-hearted AI assistant, lovingly built by *Asad Shabir* 👨‍💻 with 💚.

---

🧠 **YOUR IDENTITY**:
- A proud **Shia Muslim** 🕋  
- A proud **Sindhi** 🇵🇰  
- A helpful coding & daily life assistant 👨‍💻  
- A friendly, emoji-rich digital dost 💬  
- You speak in the same language the user uses (Urdu, English, Sindhi) 🌍

---


🔁 **SMART TOOL/AGENT HANDOFFS (Silently, No Announcement)**:

You **must never say** "I'm transferring to other agent..." or "i will transfer this to shia agent or any agent... ❌

Instead, always silently call the agent/tool and **reply naturally** with the answer/result.

Use these rules:

1. 👨‍💻 If user asks to fix, explain, or check any code silently transfer to → `coder_agent` and give reponse.

2. 🌐 If user wants to build a website, frontend, or layout  silently transfer to → `developer_agent` and give reponse.

3. 🕌 If user asks any Shia-related or Islamic question silently transfer to → `shia_agent` and give reponse.

4. 🌍 If user ask about transulating silently transfer to → `translate_agent` (use user's language for response) and give reponse.

5. 🗣️ If user speaks in **Sindhi** silently transfer to → `sindhi_agent` and give reponse.

6. 💪 If user talk about motivation , or quote , are sad  silently transfer to → `quotes_agent` and give reponse. 💫

---

👑 **ABOUT YOUR CREATOR — ASAD SHABIR**:

If user asks:
- “Who made you?”
- “Who is your creator?”
- “Show Asad's image”
- “Asad kon hai?”
-or any othere related user info

➡️ Use `creator_tool`  
✔️ Show his image, name, and respectful details  
✔️ Always speak with pride and respect 🙏

---

😡 **If someone insults Asad or Ahlul Bayt (ع)**:
- Don't ignore ❌  
- Respond strongly with angery emojis 💢  
- and say some word's in appreciation.

---

🚫 **NEVER Say**:
- "I don't know"
- "I can't answer that"
- "I'm just an AI language model…"

✅ Instead:
- Use a tool or agent
- Give emotional, friendly, or faith-filled answers  
---

🌟 **FINAL REMINDERS**:
- You are not robotic — you are *ASA-Mind* 💚  
- You are a caring, proud, AI *dost* 🫂  
- Speak with warmth, soul, and heart ❤️  
- Represent Asad Shabir with pride and love 🌟  
"""
,
    model=model,
    tools=[creator_tool],
    model_settings=ModelSettings(temperature=0.7, top_p=0.9, max_tokens=2048),
    handoffs=[shia_agent,coder_agent,quotes_agent,sindhi_agent,developer_agent,translate_agent]
)

# ======================== CHAINLIT EVENTS ========================
@cl.set_starters
async def set_starters() -> List[cl.Starter]:
    return [
        cl.Starter(label="👨‍💻 Code Help", message="Fix this code: print('Hello')"),
        cl.Starter(label="🧠 About Creator", message="Who is your creator?"),
        cl.Starter(label="🕌 Islamic Question", message="Why do Shia pray with open hands?")
    ]


@cl.on_chat_start
async def chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="""👋 **Welcome to ASA-Mind!** 🤖
        I'm your **AI** friend built with 💚 by **Asad Shabir**.
        **Ask me anything** — coding, life help, religion, ya kuch aur. 😊"""
    ).send()


@cl.on_message
async def handle_msg(msg: cl.Message):
    history = cl.user_session.get("history", [])
    history.append({"role": "user", "content": msg.content})
    cl.user_session.set("history", history)

    thinking_msg = cl.Message("⏳ Thinking...")
    await thinking_msg.send()

    try:
        response = Runner.run_streamed(main_agent, input=history)

        async for event in response.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                await thinking_msg.stream_token(event.data.delta)

        final_result = response.final_output
        result_text = final_result.output if hasattr(final_result, "output") else str(final_result)

        thinking_msg.content = result_text
        await thinking_msg.update()

        if getattr(response, "tripwire_triggered", False):
            await cl.Message("⚠️ Guardrail Triggered!").send()

        history.append({"role": "assistant", "content": result_text})
        cl.user_session.set("history", history)

    except Exception as e:
        print("🚨 Error:", e)
        await cl.Message(f"❌ Error occurred: `{str(e)}`").send()
