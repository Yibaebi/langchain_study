import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from agents.linkedin_lookup_agent import lookup
from utils.linkedin_scrapper import scrape_linkedin_profile
from output_parsers import profile_summary_parser


class PresidentProfileIceBreaker:
    def __init__(self):
        self.president_profile_template = """
            Given the country name name {country_name}. I want you to create a short
            summary of their president profile.
        """

        self.president_profile_prompt = PromptTemplate(
            input_variables=["country_name"], template=self.president_profile_template
        )

        self.prompt_input = {"country_name": "Nigeria"}

    def icebreaker_chatgpt(self):
        llm = ChatOpenAI(
            temperature=0, model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY")
        )

        chain = self.president_profile_prompt | llm
        res = chain.invoke(input=self.prompt_input)

        return res

    def icebreaker_anthropic(self):
        llm = ChatAnthropic(model="claude-sonnet-4-20250514")
        chain = self.president_profile_prompt | llm | StrOutputParser()
        res = chain.invoke(input=self.prompt_input)

        return res


class LinkedInProfileSummaryIceBreaker:
    def get_linkedin_profile_info(self, name_with_unique_info):
        """
        Scrapes and Formats Scraped LinkedIn Info
        """
        linkedin_url = lookup(name_with_unique_info=name_with_unique_info)

        profile_info = scrape_linkedin_profile(
            linkedin_profile_url=linkedin_url, mock=True
        )

        return profile_info

    def create_linkedin_profile_summary(self, profile: dict):
        """
        Creates a linkedin profile summary
        """

        prompt_template = """
            Create the following for the Linkedin profile data {linkedin_profile}.
            1. A short professional summary of the profile.
            2. Two interesting facts about the linkedin profile.
            
            If the profile is unavailable you can respond that the profile is not found.
            \n{format_instructions}
        """

        linkedin_profile_prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["linkedin_profile"],
            partial_variables={
                "format_instructions": profile_summary_parser.get_format_instructions()
            },
        )

        llm = ChatAnthropic(model="claude-sonnet-4-20250514")
        chain = linkedin_profile_prompt | llm | profile_summary_parser
        res = chain.invoke(input={"linkedin_profile": profile})

        return res


pres_profile_IB = PresidentProfileIceBreaker()
linkedin_profile_IB = LinkedInProfileSummaryIceBreaker()
