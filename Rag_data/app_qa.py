from nt import read

import streamlit as st
from rag import RagService
import config_data as config

#标题
st.title("智能客服")
st.divider() # 分隔线

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "有什么问题嘛？"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 在页面最下方添加输入框
promot = st.chat_input("请输入您的问题：")



if promot:
    # 输入用户的问题并显示在页面上
    st.chat_message("user").write(promot)
    st.session_state["message"].append({"role": "user", "content": promot})
    with st.spinner("思考中..."):
        results_stream = st.session_state["rag"].chain.stream({"input": promot}, config=config.session_config)
        
        res = st.chat_message("assistant").write_stream(results_stream)
        st.session_state["message"].append({"role": "assistant", "content": res})


