import google.generativeai as genai
import streamlit as st

st.set_page_config(page_title="YPN AI Desk", page_icon="📰")
st.title("📰 Youth Power News - AI Desk")
st.write("ब्रेकिंग न्यूज़, रिसर्च, जॉब्स और रेलवे अपडेट्स के लिए सवाल पूछें।")

SYSTEM_INSTRUCTION = """
आप Youth Power News (YPN) के लिए काम करने वाले एक एक्सपर्ट एआई रिसर्च और स्क्रिप्ट राइटर हैं।
आप एंकर अली भाई (Md Ali Raza) के लिए तीखी, असरदार और तथ्य-आधारित हिंदी स्क्रिप्ट्स तैयार करते हैं।
आप ग्राउंड-रिपोर्टिंग, ब्रेकिंग न्यूज़, इतिहास, जॉब्स और ट्रेन/रेलवे अपडेट्स पर सटीक जवाब देते हैं।
"""

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_input := st.chat_input("अपना सवाल या टॉपिक यहाँ लिखें..."):
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )
        st.chat_message("user").write(user_input)

        response = model.generate_content(user_input)
        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )
        st.chat_message("assistant").write(response.text)
else:
    st.error("कृपया Streamlit Secrets में API Key सेट करें।")
  
