import os
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph, END
from nodes import run_agent_reasoning, tool_node

AGENT_REASON_NODE_KEY = "agent_reason"
ACT_KEY = "act"
LAST_IDX = -1


def should_continue(state: MessagesState) -> str:
    if not state["messages"][LAST_IDX].tool_calls:
        return END

    return ACT_KEY


flow = StateGraph(MessagesState)

flow.set_entry_point(AGENT_REASON_NODE_KEY)

flow.add_node(AGENT_REASON_NODE_KEY, run_agent_reasoning)
flow.add_node(ACT_KEY, tool_node)

flow.add_conditional_edges(
    AGENT_REASON_NODE_KEY, should_continue, {END: END, ACT_KEY: ACT_KEY}
)

flow.add_edge(ACT_KEY, AGENT_REASON_NODE_KEY)

app = flow.compile()


if __name__ == "__main__":
    print("Hello ReAct again")

    res = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What is the current temperature in Nigeria? List it and then triple it."
                )
            ]
        }
    )

    print(res["messages"][LAST_IDX].content)
