from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from third_parties.linkedin import scrape_linkedin_profiles


load_dotenv()


def listen_and_respond():

    information = scrape_linkedin_profiles(
        linkedin_profile_url="https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json"
    )
    summary_template = """
    given the information {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables="information", template=summary_template
    )
    llm = ChatOpenAI(
        temperature=0, model_name="gpt-3.5-turbo"
    )  # 0 means it won't be creative
    chain = (
        summary_prompt_template | llm
    )  # chaining will be acieved by using the pipe | operator
    res = chain.invoke(input={"information": information})
    print(res.content)


if __name__ == "__main__":
    print("loaded...")
    listen_and_respond()
