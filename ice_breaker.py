"""
Prerequisite:
    1. scrapin url: https://app.scrapin.io/lookup/persons
       Coupon discount of 20%: EDENMARCO
       free tier will give 100 credits
    2. https://nubela.co/proxycurl/linkedin
       Free tier will get 10 credits
"""

import os
from typing import Tuple
import requests
from utils import extract_valid_data
from agents.linkedin_lookup_agent import look_up as linkedin_lookup_agent
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from output_parsers import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profiles

load_dotenv()

def get_linkedin_profile_photo_url(linkedin_data: str) -> str:
    person_obj = linkedin_data.get("person", {"person": ""})
    photo_url = person_obj.get("photoUrl", "")
    return photo_url



def provide_short_description(linkedin_data: str) -> Tuple[Summary, str]:
    summary_template = """
    given the information about a person from linkedin {information} from I want you to create:
    1. a short summary
    2. two interesting facts about them

    Use information from LinkedIn \n
    {format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_data"], template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )
    llm = ChatOpenAI(
        temperature=0, model_name="gpt-4o-mini"
    )  # 0 means it won't be creative
    chain = summary_prompt_template | llm | summary_parser # chaining will be acieved by using the pipe | operator
    res: Summary = chain.invoke(input={"information": linkedin_data})
    photo_url = get_linkedin_profile_photo_url(linkedin_data=linkedin_data)
    return res, photo_url

def ice_breaker_with(name: str, mock=False) -> Tuple[Summary, str]:
    """
    Scrape information from linkedin profiles,
    steps:
        1. take the input as user name findthe best match in the linkedin profiles
        2. return the linkedin profile url from the agent
        3. ingest linkedIn profile url to scrapin to get the profile information
        4. pass the information to chatopenAI to pull the short information
    """
    linkendin_profile_url = linkedin_lookup_agent(name=name, mock=mock)
    print(linkendin_profile_url)
    linkedin_data = scrape_linkedin_profiles(linkedin_profile_url=linkendin_profile_url,
                                              mock=mock)
    short_discription = provide_short_description(linkedin_data)
    print(f"short description: {short_discription}")
    return short_discription

if __name__ == "__main__":
    result = ice_breaker_with(name="carl pei nothing")
    print(result)
