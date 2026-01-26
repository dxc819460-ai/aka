
import os
from importlib.metadata import metadata
from operator import length_hint
from os import mkdir
from datetime import datetime
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def check_md5(md5_str:str):
    #检查传入的MD5是否以及被处理过
    if not os.path.exists(config.md5_path):
        open(config.md5_path,'w',encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path,'r',encoding='utf-8').readlines():
            line = line.strip()
            if line==md5_str:
                return True
    return False

def save_md5(md5_str:str):
    #将传入的md5字符串记录到文件内保存
    with open(config.md5_path,'a',encoding='utf-8') as f:
        f.write(md5_str+"\n")
    pass

def get_string_md5(input_str:str,encoding='utf-8'):
    #将传入的字符串转换为MD5字符串
    str_bytes=input_str.encode(encoding=encoding)

    md5_obj=hashlib.md5()#得到md5对象
    md5_obj.update(str_bytes)#更新内容（传入即将要转换的字节数组）
    md5_hex=md5_obj.hexdigest()#得到 md5的16进制字符串
    return md5_hex



class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory,exist_ok=True)
        self.persist_directory=config.persist_directory
        self.chroma=Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory,
        ) #向量存储的实例
        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,#分割后的段
            chunk_overlap=config.chunk_overlap,#重叠
            separators=config.separators,
            length_function=len,
        ) #文本分割器的对象

    def upload_by_str(self, data,filename):
        #将传入的字符串进行向量化存入向量数据库
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已存在知识库中"
        if len(data) > config.max_split_char_number:
            knowledge_chunk:list[str]=self.spliter.split_text(data)
        else:
            knowledge_chunk=[data]

        metadata={
            "source":filename,
            "creat_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"小邓",
        }
        self.chroma.add_texts(
            knowledge_chunk,
            metadatas=[metadata for _ in range(len(knowledge_chunk))],
        )
        save_md5(md5_hex)
        return "[成功]内容已经载入向量库"

if __name__ == '__main__':
    service = KnowledgeBaseService()
    r=service.upload_by_str("周杰伦","testfile")
    print(r)
