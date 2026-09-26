import google.generativeai as genai
import streamlit as st

st.set_page_config(page_title="Youth Power News - AI Desk", page_icon="📰")
st.title("📰 Youth Power News - AI Desk")
st.subheader("ब्रेकिंग न्यूज़, रिसर्च, जॉब्स और रेलवे अपडेट्स के लिए सवाल पूछें।")

SYSTEM_INSTRUCTION = """
आप Youth Power News (YPN) के लिए काम करने वाले एक एक्सपर्ट AI असिस्टेंट हैं।
आप भाषा को साफ़, हिंदी (या आवश्यकता अनुसार Hinglish) में सरल और सटीक रखते हैं।
आप ग्राउंड-रिपोर्टिंग, फैक्ट-चेकिंग, रिसर्च, न्यूज़ ड्राफ्टिंग और ट्रेंडिंग टॉपिक्स पर सटीक जवाब देते हैं।
"""

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        system_instruction=SYSTEM_INSTRUCTION,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_input := st.chat_input("अपना सवाल या टॉपिक यहाँ लिखें..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        response = model.generate_content(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
else:
    st.error("कृपया Streamlit Secrets में API Key सेट करें।")
    
