from langchain.agents import tool
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.tools.render import render_text_description
from langchain import hub


@tool
def get_string_length(text: str):
    """Returns the length of a string."""
    return len(text.strip("\n").strip('"'))


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
      Thought:
    """

    prompt = PromptTemplate.from_template(template=prompt_template).partial(
        tools=render_text_description(tools=tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)
    agent = (
        {"input": lambda x: x["input"]} | prompt | llm | ReActSingleInputOutputParser()
    )

    res = agent.invoke({"input": "What is the length of this text 'Elliot'"})

    print(res)
