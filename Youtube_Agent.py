from typing import TypedDict
import random 
from typing import Literal
#from Ipython.display import Image,display
from langgraph.graph import StateGraph,START,END


class State(TypedDict):
    graph_info:str

#defining node functions
def play_start(state:State):
    print("Start Play Node is started")
    return {"graph_info":state["graph_info"]+ "I am Planning to Play"}
def cricket(state:State):  
    print("cricket Node started")
    return {"graph_info":state["graph_info"]+ " cricket"}
def horseriding(state:State):
    print("horseriding Node started")
    return {"graph_info":state["graph_info"]+ " "}
def decide_play(state:State) -> Literal["cricket","horseriding"]:
    res = random.randint()
    if res > 0.5:
        return "cricket"
    else:
        return "horseriding"


#creating stategrpah
grpah = StateGraph(State)

graph.add_node("start_play",play_start)
graph.add_node("cricket",cricket)
grpah.add_node("horseriding",horseriding)


graph.compile()