#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/5 13:19
# @Author  : Shutian
# @File    : multiChain.py
# @Description    :

from langchain_community.chat_models import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

chain = (
    PromptTemplate.from_template(
        """Given the user question below, classify it as either being about `LangChain`, `Anthropic`, or `Other`.

Do not respond with more than one word.

<question>
{question}
</question>

Classification:"""
    )
    | ChatAnthropic(anthropic_api_key='')
    | StrOutputParser()
)

langchain_chain = (
    PromptTemplate.from_template(
        """You are an expert in langchain. \
Always answer questions starting with "As Harrison Chase told me". \
Respond to the following question:

Question: {question}
Answer:"""
    )
    | ChatAnthropic(anthropic_api_key='')
)
anthropic_chain = (
    PromptTemplate.from_template(
        """You are an expert in anthropic. \
Always answer questions starting with "As Dario Amodei told me". \
Respond to the following question:

Question: {question}
Answer:"""
    )
    | ChatAnthropic(anthropic_api_key='')
)
general_chain = (
    PromptTemplate.from_template(
        """Respond to the following question:

Question: {question}
Answer:"""
    )
    | ChatAnthropic(anthropic_api_key='')
)


def route(info):
    print(info)
    if "anthropic" in info["topic"].lower():
        return anthropic_chain
    elif "langchain" in info["topic"].lower():
        return langchain_chain
    else:
        return general_chain


full_chain = {"topic": chain, "question": lambda x: x["question"]} | RunnableLambda(
    route
)

print(full_chain.invoke({"question": "how do I use Anthropic?"}))
