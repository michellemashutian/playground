#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/8 15:46
# @Author  : Shutian
# @File    : agentChain.py
# @Description    : about agents

from langchain import hub
from langchain.agents import AgentExecutor, tool
from langchain.agents.output_parsers import XMLAgentOutputParser
from langchain_community.chat_models import ChatAnthropic

# 首先当然是定义好咱们的model啦
model = ChatAnthropic(model="claude-2", anthropic_api_key='')

# 这里咱们的tool叫做search，自定义，示例代码直接返回了“32degree”
@tool
def search(query: str) -> str:
    """Search things about current events."""
    return "32 degrees"

@tool
def joke(query: str) -> str:
    """Search things about current events."""
    return "it's a pig day"

tool_list = [search, joke]
# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/xml-agent-convo")
# Logic for going from intermediate steps to a string to pass into model
# This is pretty tied to the prompt
def convert_intermediate_steps(intermediate_steps):
    log = ""
    for action, observation in intermediate_steps:
        print("\n")
        print(action)
        print("\n")
        print(observation)
        log += (
            f"<tool>{action.tool}</tool><tool_input>{action.tool_input}"
            f"</tool_input><observation>{observation}</observation>"
        )
    return log


# Logic for converting tools to string to go in prompt
def convert_tools(tools):
    return "\n".join([f"{tool.name}: {tool.description}" for tool in tools])

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: convert_intermediate_steps(
            x["intermediate_steps"]
        ),
    }
    | prompt.partial(tools=convert_tools(tool_list))
    | model.bind(stop=["</tool_input>", "</final_answer>"])
    | XMLAgentOutputParser()
)
agent_executor = AgentExecutor(agent=agent, tools=tool_list, verbose=True)
print(agent_executor.invoke({"input": "whats the weather in New york?"}))
print("\n\n\n")
print(agent.get_prompts())
print("\n\n\n")
agent.get_graph().print_ascii()
