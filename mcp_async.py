from langgraph.graph import StateGraph,START,END
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.messages import BaseMessage, HumanMessage
from dotenv import load_dotenv
from typing import TypedDict , Literal , Annotated
from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode , tools_condition
from langchain_community.tools import DuckDuckGoSearchRun # type: ignore
from langchain_core.tools import tool
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient 

load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

client = MultiServerMCPClient(
    {
        "arith" : {
            "transport" : "stdio",
            "command" : "python",
            "args" : ["C:\\Users\\dell\\Desktop\\Langgraph-learning\\arith_server.py"],
        }
    }
)

class chatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]


async def built_graph():
    tools = await client.get_tools()
    
    llm_with_tools = llm.bind_tools(tools)
    async def chat_model(state:chatState):
        messages = state['messages']
        response = await llm_with_tools.ainvoke(messages)
        return {'messages': response}

    tool_node = ToolNode(tools)

    graph = StateGraph(chatState)
    graph.add_node("chat_node",chat_model)
    graph.add_node("tools",tool_node)
    graph.add_edge(START,"chat_node")
    graph.add_conditional_edges("chat_node",tools_condition)
    graph.add_edge("tools","chat_node")
    chatbot = graph.compile()

    return chatbot

async def main():
    chatbot = await built_graph()

    output = await chatbot.ainvoke({"messages" : [HumanMessage(content="calcaulate the sum of 45.67 and 89.23 , give the answer in cricket commentator style") ]})
    print(output['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())