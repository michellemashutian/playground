#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/1 12:29
# @Author  : Shutian
# @File    : simpleChain1.py
# @Description    :

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(openai_api_key='')
# print(llm.invoke("how can langsmith help with testing?"))

output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])

chain = prompt | llm | output_parser
print(chain.invoke({"input": "how can langsmith help with testing?"}))
