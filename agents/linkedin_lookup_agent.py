"""
Point 1: We take user name as an input
Point 2: We will search in online and get the linkedIn profile URL
Point 3: Using the scrapi api get the information by using the above generated profile url
"""

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from tools.tools import get_profile_url_tavily

load_dotenv()


def look_up(name: str) -> str:

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    template = """ given the full name {name_of_person} I want you to get it me a link to their linkedIn profile page.
            Your answer should contain only a URL. """

    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )  # name_of_person we are going to plugin dynamically

    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedIn profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the LinkedIn page URL",
        )
    ]

    react_prompt = hub.pull(
        "hwchase17/react"
    )  # harrison Chase 17 is the user name of Harrison Chase in the prompt tab
    """
    react prompt is going to be our reasoning Engine of our agent
    React prompt is sent to the LLM, It will include our tool names and description and what we want our agent to do
    """
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, prompt=react_prompt
    )
    result = agent_executor.invoke(
        input={"input": prompt_template.format(name_of_person=name)}
    )
    linkedin_profile_url = result["output"]
    return linkedin_profile_url


if __name__ == "__main__":
    look_up(name="venkatesh vadla zelis")
