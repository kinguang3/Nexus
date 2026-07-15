import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFileRec # 导入streamlit库


#添加标题
st.title("文件上传")


# 上传文件
uploaded_file = st.file_uploader( 
    "上传文件",
    type=["txt"],
    # 允许上传多个文件
    accept_multiple_files=False,# 不允许上传多个文件  
)


if uploaded_file is not None:
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size / 1024# 转换为KB
    st.subheader(f"文件信息{file_name}")# 显示文件名,subheader标题为1级标题
    st.write(f"文件类型: {file_type}")#write方法用于显示文本内容
    st.write(f"文件大小: {file_size:.2f} KB")
    #get_value方法用于获取文件内容
    uploaded_file_content = uploaded_file.getvalue()
    uploaded_file_content = uploaded_file_content.decode('utf-8')# 转换为字符串
    st.write(uploaded_file_content)


