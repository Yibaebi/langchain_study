from typing import List, Union
from langchain.agents import tool, Tool
from langchain.agents.format_scratchpad.log import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain_anthropic import ChatAnthropic

from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.prompts import PromptTemplate
from langchain_core.tools.render import render_text_description


@tool
def get_string_length(text: str):
    """Returns the length of a string."""
    return len(text.strip("\n").strip('"'))


def find_tool_by_name(tools: List[Tool], tool_name: str):
    """Returns a tool name to be executed"""
    for tool in tools:
        if tool.name == tool_name:
            return tool

    return ValueError()


def get_agent_input(intermediate_steps: list):
    """Returns a static query with a dynamic intermediate steps"""
    return {
        "input": "What is the length of 'Elliot'?",
        "agent_scratchpad": intermediate_steps,
    }


if __name__ == "__main__":
    print("Tool calling.")

    tools = [get_string_length]

    prompt_template = """
      Answer the following questions as best you can. You have access to the following tools:

      {tools}

      Use the following format:

      Question: the input question you must answer
      Thought: you should always think about what to do
      Action: the action to take, should be one of [{tool_names}]
      Action Input: the input to the action
      Observation: the result of the action
      ... (this Thought/Action/Action Input/Observation can repeat N times)
      Thought: I now know the final answer
      Final Answer: the final answer to the original input question

      Begin!

      Question: {input}
      Thought: {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template=prompt_template).partial(
        tools=render_text_description(tools=tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0,
        stop=["\nObservation"],
    )

    intermediate_steps = []

    agent_inputs = {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
    }

    agent = agent_inputs | prompt | llm | ReActSingleInputOutputParser()

    agent_step: Union[AgentAction | AgentFinish] = agent.invoke(
        get_agent_input(intermediate_steps)
    )

    if isinstance(agent_step, AgentAction):
        # Get tool to call for next step
        tool_name = agent_step.tool
        tool_to_call = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input

        # get observation and add it to scratchpad for memory sakes
        observation = tool_to_call.func(tool_input)
        intermediate_steps.append((agent_step, str(observation)))

        # re-invoke the agent with the new observation and scratchpad
        agent_step = agent.invoke(get_agent_input(intermediate_steps))

        if isinstance(agent_step, AgentFinish):
            final_answer = agent_step.return_values
            print(final_answer)
