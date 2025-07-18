from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

information = """
Elon Reeve Musk (/ˈiːlɒn/ EE-lon; born June 28, 1971) is a businessman. He is known for his leadership of Tesla, SpaceX, X (formerly Twitter), and the Department of Government Efficiency (DOGE). Musk has been considered the wealthiest person in the world since 2021; as of May 2025, Forbes estimates his net worth to be US$424.7 billion.

Born to a wealthy family in Pretoria, South Africa, Musk emigrated in 1989 to Canada. He received bachelor's degrees from the University of Pennsylvania in 1997 before moving to California, United States, to pursue business ventures. In 1995, Musk co-founded the software company Zip2. Following its sale in 1999, he co-founded X.com, an online payment company that later merged to form PayPal, which was acquired by eBay in 2002. That year, Musk also became an American citizen.

In 2002, Musk founded the space technology company SpaceX, becoming its CEO and chief engineer; the company has since led innovations in reusable rockets and commercial spaceflight. Musk joined the automaker Tesla as an early investor in 2004 and became its CEO and product architect in 2008; it has since become a leader in electric vehicles. In 2015, he co-founded OpenAI to advance artificial intelligence research but later left; growing discontent with the organization's direction and their leadership in the AI boom in the 2020s led him to establish xAI. In 2022, he acquired the social network Twitter, implementing significant changes and rebranding it as X in 2023. His other businesses include the neurotechnology company Neuralink, which he co-founded in 2016, and the tunneling company the Boring Company, which he founded in 2017. He was named Time magazine's Person of the Year in 2021.

Musk's political activities, views, and statements have made him a polarizing figure, especially following the COVID-19 pandemic. He has been criticized for making unscientific and misleading statements, including COVID-19 misinformation and promoting conspiracy theories, and affirming antisemitic, racist, and transphobic comments. His acquisition of Twitter was controversial due to a subsequent increase in hate speech and the spread of misinformation on the service. Musk was the largest donor in the 2024 U.S. presidential election, and is a supporter of global far-right figures, causes, and political parties. In early 2025, he served as senior advisor to United States president Donald Trump and as the de facto head of DOGE. His role in the second Trump administration attracted public backlash, particularly in response to DOGE.
"""


def listen_and_respond():
    load_dotenv()
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
    print(res)


if __name__ == "__main__":
    print("loaded...")
    listen_and_respond()
