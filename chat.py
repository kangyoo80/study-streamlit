import streamlit as st

from dotenv import load_dotenv
from llm import get_ai_response

# print(1)
# 1. page config
st.set_page_config(
    page_title="소득세 챗봇",
    page_icon=":robot_face:",  # 또는 "./images/my_icon.png"
)

load_dotenv()

# print(2)
# 2. 페이지 제목과 설명 표시
st.title(":robot_face: 소득세 챗봇")
st.caption("소득세에 관련된 모든것을 답해드립니다!")

# print(3)
# 4. 챗팅 세션 생성(메시지 저장)
if 'message_list' not in st.session_state:
    st.session_state.message_list = []
    
# print(f"before user message === {st.session_state.message_list}")
# 5. 챗팅 메시지 표시
for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 3. 사용자 입력을 위한 chating 영역 생성
if user_question := st.chat_input(placeholder="소득세에 관련된 궁금한 내용을 말씀해주세요!"):
    
    # 사용자가 메시지를 입력하고 엔터를 치면 실행되는 부분
    # 현재는 pass로 되어있어 아무 동작도 하지 않음
    # pass

    # 사용자가 입력한 메시지를 챗봇에 전달하는 부분
    with st.chat_message("user"): # chat_message option은 "user", "assistant", "ai", "human" 네가지가 있음
        st.write(user_question)
    st.session_state.message_list.append({"role": "user", "content": user_question})
    
    with st.spinner("소득세 챗봇이 답변을 준비중입니다..."):
        ai_response = get_ai_response(user_question)

        # 5. 챗봇이 메시지를 입력하는 부분(5. ai 답변 가상 데이터 테스트)
        with st.chat_message("ai"):
            ai_message = st.write_stream(ai_response)
        st.session_state.message_list.append({"role": "ai", "content": ai_message})
# print(f"after user message === {st.session_state.message_list}")





