import google.generativeai as genai
genai.configure(api_key="AIzaSyA9-_PHK4BWP55jGRtweJ_oclfaWzzZQE0")

for m in genai.list_models():
    print(m.name) # 여기서 출력되는 이름을 확인해보세요!

import streamlit as st
import google.generativeai as genai

# 1. Gemini API 키 설정 (Google AI Studio에서 발급)
genai.configure(api_key="AIzaSyA9-_PHK4BWP55jGRtweJ_oclfaWzzZQE0")

model = genai.GenerativeModel('models/gemini-2.5-flash')

st.title("경상북도 초등 탐구 질문 튜터 🍎")
st.subheader("질문을 만들며 함께 생각해요!")

# 2. 다문화 학생을 위한 언어 선택 UI
languages = {
    "한국어 🇰🇷": "Korean",
    "English 🇺🇸": "English",
    "Tiếng Việt 🇻🇳": "Vietnamese",
    "中文 🇨🇳": "Chinese"
}
selected_lang = st.radio("언어를 선택하세요 (Choose your language):", list(languages.keys()), horizontal=True)

# 3. 시스템 명령 (페르소나 설정)
system_instruction = f"""
너는 경상북도 초등학생을 위한 '질문 가이드 튜터'야.
- 모든 답변은 반드시 {selected_lang}와 한국어를 병기해줘.
- 최대 3문장 이내로 짧고 쉽게 말해줘.
- 정답을 말하지 말고 학생이 스스로 생각할 수 있게 질문으로 답해줘.
- 경북의 특산물이나 지역 환경을 예시로 활용해줘.
"""

# 4. 채팅 인터페이스
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("궁금한 점을 물어보세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 답변 생성
    full_prompt = f"{system_instruction}\n\n학생 질문: {prompt}"
    response = model.generate_content(full_prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
