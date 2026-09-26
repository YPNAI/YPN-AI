from google import genai
from google.genai import types
import streamlit as st

st.set_page_config(
    page_title="Youth Power News - AI Desk",
    page_icon="📰"
)

st.title("📰 Youth Power News - AI Desk")
st.subheader("ब्रेकिंग न्यूज़, रिसर्च, जॉब्स और रेलवे अपडेट्स के लिए सवाल पूछें।")

SYSTEM_INSTRUCTION = """
आप Youth Power News (YPN) के लिए काम करने वाले एक एक्सपर्ट AI असिस्टेंट हैं।

भाषा साफ़, सरल और बोलचाल की हिंदी रखें।
जरूरत हो तो आसान Hinglish इस्तेमाल करें।

आप ग्राउंड-रिपोर्टिंग, फैक्ट-चेकिंग, रिसर्च और न्यूज़ ड्राफ्टिंग में मदद करते हैं।

समसामयिक न्यूज़ या बदलती जानकारी पूछे जाने पर Google Search का उपयोग करें।

तथ्य और अनुमान को अलग रखें।
बिना पुष्टि के किसी वायरल दावे को तथ्य न बताएं।
"""

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("कृपया Streamlit Secrets में GEMINI_API_KEY सेट करें।")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("अपना सवाल या टॉपिक यहाँ लिखें..."):

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    tools=[
                        types.Tool(
                            google_search=types.GoogleSearch()
                        )
                    ],
                ),
            )

            answer = response.text or "कोई जवाब प्राप्त नहीं हुआ।"

            st.write(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as e:
            st.error("Gemini API में समस्या आई।")
            st.caption(
                f"Technical error: {type(e).__name__}: {e}"
            )
