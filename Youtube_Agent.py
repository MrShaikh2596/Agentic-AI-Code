from typing import TypedDict
import random
from typing import Literal
# from Ipython.display import Image,display
from langgraph.graph import StateGraph, START, END
from ollama import chat
import os
from dotenv import load_dotenv
# Call it to load variables from a .env file into os.environ
load_dotenv()

class State(TypedDict):
    graph_info: str

# defining node functions


def play_start(state: State):
    print("Start Play Node is started")
    return {"graph_info": state["graph_info"] + "I am Planning to Play"}


def cricket(state: State):
    print("cricket Node started")
    return {"graph_info": state["graph_info"] + " cricket"}



def horseriding(state: State):
    print("horseriding Node started")
    return {"graph_info": state["graph_info"] + " "}


def decide_play(state: State) -> Literal["cricket", "horseriding"]:
    res = random.randint(0,1)
    if res > 0.5:
        return "cricket"
    else:
        return "horseriding"
def decide_play_llm(state:State):
    response = chat(
    model='granite4.1:3b',
    messages=[{'role': 'user', 'content': """Just output one of the following values at random each time:["cricket","horseriding"]"""}])
    return response.message.content




# creating stategrpah
graph = StateGraph(State)
graph.add_node("start_play", play_start)
graph.add_node("cricket", cricket)
graph.add_node("horseriding", horseriding)

# adding edges
graph.add_edge(START, "start_play")
#graph.add_conditional_edges("start_play", decide_play)
graph.add_conditional_edges("start_play", decide_play_llm)
graph.add_edge("cricket", END)
graph.add_edge("horseriding", END)

graph=graph.compile()
graph.invoke({"graph_info":"Initial Message"})