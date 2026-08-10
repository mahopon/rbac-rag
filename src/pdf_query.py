from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated

from src.vectorstore import vectorstore
from src.llm import llm

class State(TypedDict):
  query: str
  context: list[str]
  answer: str
  system_instruction: str
  
def retrieve(state: State) -> dict:
    docs = vectorstore.similarity_search(state["query"])
    return {"context": [d.page_content for d in docs]}

def generate(state: State) -> dict:
    instruction = state.get("system_instruction", "")
    prompt = f"{instruction}\n\nContext: {state['context']}\nQ: {state['query']}" if instruction else f"Context: {state['context']}\nQ: {state['query']}"
    answer = llm.invoke(prompt)
    return {"answer": answer}
  
graph = StateGraph(State)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

app = graph.compile(checkpointer=MemorySaver())