#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/3 13:16
# @Author  : Shutian
# @File    : simpleChain2.py
# @Description    :

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
model = ChatOpenAI(openai_api_key='')
output_parser = StrOutputParser()

chain = prompt | model | output_parser

print(chain.invoke({"topic": "ice cream"}))
