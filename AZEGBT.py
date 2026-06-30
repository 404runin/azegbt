import streamlit as st
from groq import Groq
import requests
from PIL import Image
from io import BytesIO

# Groq API Açarı
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Səhifə Ayarları - Mənim kimi professional görünüş
st.set_page_config(page_title="AZEGBT AI", page_icon="🤖", layout="centered")

# Saytın Başlığı və Stil bəzəkləri
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 AZEGBT Personal AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>Sənin şəxsi süni intellekt köməkçin. Hər dildə danışır, kömək edir və şəkil çəkir.</p>", unsafe_allow_html=True)
st.divider()

def sekil_yarat(tesvir):
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(tesvir)}?width=800&height=600&enhanced=true"
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    return None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajların qəşəng vizual göstərilməsi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "is_image" in message:
            st.image(message["content"], caption="AZEGBT tərəfindən yaradıldı")
        else:
            st.markdown(message["content"])

# Giriş sahəsi
if prompt := st.chat_input("Mənə bir şey yaz və ya 'şəkil çək: ...' əmri ver"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if "şəkil çək" in prompt.lower() or "sekil cek" in prompt.lower():
        with st.chat_message("assistant"):
            with st.spinner("Şəkil yaradılır..."):
                tesvir = prompt.lower().replace("şəkil çək:", "").replace("sekil cek:", "").strip()
                img = sekil_yarat(tesvir)
                if img:
                    st.image(img)
                    st.session_state.messages.append({"role": "assistant", "content": img, "is_image": True})
                else:
                    st.error("Xəta baş verdi.")
    else:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Düşünürəm..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": "Sən AZEGBT adlı premium və çox ağıllı bir süni intellektsən. İstifadəçinin şəxsi köməkçisən. Azərbaycan dilində tam qüsursuz, qrammatik düzgün yazırsan. Mövzuları qarşı tərəfin tam anlayacağı şəkildə, aydın və dərin izah edirsən."
                        },
                        *st.session_state.messages
                    ],
                    model="llama-3.1-70b-versatile",
                )
                cavab = chat_completion.choices[0].message.content
                message_placeholder.markdown(cavab)
                st.session_state.messages.append({"role": "assistant", "content": cavab})