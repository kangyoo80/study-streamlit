import streamlit as st

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langsmith import Client
from langchain.chains import RetrievalQA
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

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

def get_ai_message(user_message):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    index_name = "tax-markdown-index"
    
    # 기존 인덱스 사용
    database = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )

    llm = ChatOpenAI(model="gpt-4o")

    client = Client()
    prompt = client.pull_prompt("rlm/rag-prompt")
    retriever = database.as_retriever(search_kwargs={'k': 4})


    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )


    dictionary = ["사람을 나타내는 표현 -> 거주자"]

    prompt = ChatPromptTemplate.from_template(f"""
        사용자의 질문을 보고, 우리의 사전을 참고해서 사용자의 질문을 변경해주세요.
        만약 변경이 필요가 없다고 판단되면, 사용자의 질문을 변경하지 않아도 됩니다.
        그런 경우에는 질문만 리턴해주세요.  
        사전: {dictionary} 
        질문: {{question}}                      
    """)

    dictionary_chain = prompt | llm | StrOutputParser()
    tax_chain = {"query": dictionary_chain} | qa_chain  # query는 dictionary_chain의 결과이며, qa_chain에 넘겨줌
    ai_message = tax_chain.invoke({"question": user_message})
    # return ai_message
    return ai_message["result"]

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
        ai_message = get_ai_message(user_question)

    # 5. 챗봇이 메시지를 입력하는 부분(5. ai 답변 가상 데이터 테스트)
    with st.chat_message("ai"):
        st.write(ai_message)
    st.session_state.message_list.append({"role": "ai", "content": ai_message})
# print(f"after user message === {st.session_state.message_list}")





