import time
from itertools import count

import streamlit as st
st.title("知识库更新服务")
from knowledge_base import KnowledgeBaseService
#file_uploader
uploader_file=st.file_uploader(
    "请上传TXT文件",
    type=['txt'],
    accept_multiple_files=False,#仅接受一个文件的上传
)
service=KnowledgeBaseService()
if "service" not in st.session_state:
    st.session_state["service"]=KnowledgeBaseService()



if uploader_file is not None:
    file_name=uploader_file.name
    file_type=uploader_file.type
    file_size=uploader_file.size/1024 #KB

    st.subheader(f"文件名{file_name}")
    st.write(f"格式：{file_type},大小{file_size}")

    #get_value->bytes->decode('utf-8)
    text=uploader_file.getvalue().decode()
    with st.spinner("载入知识库"):
        time.sleep(1)
        result=st.session_state["service"].upload_by_str(text,file_name)
        st.write(result)