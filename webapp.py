
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
import os

st.set_page_config(page_title="🦜🔗 JC-Web-App")
st.title("ChatGPT-Web-Puls")

openai_api_keys = st.sidebar.text_input('OpenAI API Key')
os.environ["OPENAI_API_BASE"] = "https://api.jingcheng.love/v1"
model = st.sidebar.selectbox(
    "请选择你的模型",
    ("gpt-3.5-turbo", "gpt-3.5-turbo-16k","gpt-3.5-turbo-0613","gpt-3.5-turbo-16k-0613" ,"gpt-4","gpt-4-0613")
)

llm = ChatOpenAI(temperature=0.3,model=model,openai_api_key=openai_api_keys,handle_parsing_errors=True, streaming=True)
tools = load_tools(["ddg-search","requests_all"])
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True, verbose=True
)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    messages = [{"role": "system", "content": prompt}]
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(messages, callbacks=[st_callback])
        st.write(response)
