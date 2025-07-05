"""
Prerequisite:
    1. scrapin url: https://app.scrapin.io/lookup/persons
       Coupon discount of 20%: EDENMARCO
       free tier will give 100 credits
    2. https://nubela.co/proxycurl/linkedin
       Free tier will get 10 credits
"""

import os

import requests
from utils import extract_valid_data
from agents.linkedin_lookup_agent import look_up as linkedin_lookup_agent
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()


def provide_short_description(information: str):
    summary_template = """
    given the information {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables="information", template=summary_template
    )
    llm = ChatOpenAI(
        temperature=0, model_name="gpt-4o-mini"
    )  # 0 means it won't be creative
    chain = (
        summary_prompt_template | llm
    )  # chaining will be acieved by using the pipe | operator
    res = chain.invoke(input={"information": information})
    return res.content

def scrape_linkedin_profiles(name: str):
    """
    Scrape information from linkedin profiles,
    steps:
        1. take the input as user name findthe best match in the linkedin profiles
        2. return the linkedin profile url from the agent
        3. ingest linkedIn profile url to scrapin to get the profile information
        4. pass the information to chatopenAI to pull the short information
    """
    linkendin_profile_url = linkedin_lookup_agent(name=name)
    url = "https://api.scrapin.io/v1/enrichment/profile"
    params = {
            "apikey": os.getenv("SCRAPIN_API_KEY"),
            "linkedInUrl": linkendin_profile_url,
        }
    response = requests.get(url, params=params, timeout=10)
    user_information = extract_valid_data(response.json())
    short_discription = provide_short_description(user_information)
    return short_discription

if __name__ == "__main__":
    result = scrape_linkedin_profiles(name="carl pei nothing")
    print(result)
