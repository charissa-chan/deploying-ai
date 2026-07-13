import os
os.environ["LANGSMITH_TRACING"] = "false"

from dotenv import load_dotenv

from langgraph.graph import StateGraph, MessagesState, START
from langchain.chat_models import init_chat_model
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langchain_core.messages import SystemMessage,  HumanMessage

import json
import requests

from assignment_chat.tools_dictionary import get_definition
from assignment_chat.tools_random_fact import get_random_fact
from assignment_chat.tools_search_facts import search_facts

from utils.logger import get_logger

_logs = get_logger(__name__)
load_dotenv(".env")
load_dotenv(".secrets")

chat_agent = init_chat_model(
    model="gpt-4o-mini",
    base_url="https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1",
    api_key="any",
    default_headers={"x-api-key": os.getenv("API_GATEWAY_KEY")})


tools = [get_definition, get_random_fact, search_facts]

instructions = "you are a helpful assistant. Use the search facts tool to answer questions about facts. Only use information returned by the search tool. If the search tool does not return a relevant fact, explain that you cannot find relevant facts in your database. Do not make up facts."



# @traceable(run_type="llm")
def call_model(state: MessagesState):
    """LLM decides whether to call a tool or not"""
    response = chat_agent.bind_tools(tools).invoke( [SystemMessage(content=instructions)] + state["messages"])
    return {
        "messages": [response]
    }

def get_graph():
    
    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_node(ToolNode(tools))
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        tools_condition,
    )
    builder.add_edge("tools", "call_model")
    graph = builder.compile()
    return graph
