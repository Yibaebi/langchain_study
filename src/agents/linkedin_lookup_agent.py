from langchain_anthropic import ChatAnthropic
from langchain import hub
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, Tool, AgentExecutor
from tools.tools import find_linkedin_profile


def lookup(name_with_unique_info: str):
    llm = ChatAnthropic(model="claude-sonnet-4-20250514")

    lookup_template = """
      You are given the following person's name and unique info - {name_with_unique_info}.
      Your goal will be to return only the URL to the person's profile.
    """

    lookup_prompt_template = PromptTemplate(
        template=lookup_template,
        input_variables=["name_with_unique_info"],
    )

    lookup_tools = [
        Tool(
            description="Crawl Google for user's linkedin profile",
            func=find_linkedin_profile,
            name="Useful for looking up a person's linkedin profile URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        prompt=react_prompt,
        tools=lookup_tools,
    )

    agent_executor = AgentExecutor(agent=agent, tools=lookup_tools, verbose=True)

    response = agent_executor.invoke(
        input={
            "input": lookup_prompt_template.format_prompt(
                name_with_unique_info=name_with_unique_info
            )
        }
    )

    profile_url: str = response["output"]
    return profile_url
