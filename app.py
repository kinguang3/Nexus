import streamlit as st
from agent.react_agent import ReactAgent
import time



st.title("智扫智能客服")
st.divider()#添加分隔线


if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])#显示历史消息


#用户输入
prompt = st.chat_input("请输入您的问题")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, chche_list):

            for chunk in generator:
                chche_list.append(chunk)
                for token in chunk:
                    time.sleep(0.01)
                    yield token
        
        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))#显示助手回复
        st.session_state["messages"].append({"role": "assistant", "content": response_messages[-1]})#保存助手回复
        st.rerun()#重新运行页面,折叠助手思考