import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


if __name__ == "__main__":
    print("Hello Langchain")

    president_profile = """
        Given the country name name {country_name}. I want you to create a short
        summary of their president profile.
    """

    president_profile_prompt = PromptTemplate(
        input_variables=["country_name"], template=president_profile
    )

    llm = ChatOpenAI(
        temperature=0, model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY")
    )

    chain = president_profile_prompt | llm
    res = chain.invoke(input={"country_name": "Nigeria"})

    print(res)
