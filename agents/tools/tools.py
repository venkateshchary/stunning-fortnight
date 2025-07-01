"""
Purpose: get a name and find his linkedin url
"""

from langchain_community.tools.tavily_search import TavilySearchResults
"""
It is an search api. Tavily is an API. which is highly optimized for generative AI workloads
eg: LLM agents
    Building Rag application
    retrieval augmentation genration
"""

def get_profile_url_tavily(name:str):
    """
    Searches for LinkedIn or Twitter Profile Page.
    """
    search = TavilySearchResults()
    result = search.run(name)
    return result