"""
Prerequisite:
    scrapin url: https://app.scrapin.io/lookup/persons
    Coupon discount of 20%: EDENMARCO

"""

import os
from dotenv import load_dotenv
import requests

load_dotenv()


def extract_valid_data(response_data: dict):
    data = {
        k: v
        for k, v in response_data.items()
        if v not in ([], "", None) and k not in ["certifications"]
    }
    return data


def scrape_linkedin_profiles(linkedin_profile_url: str, mock: bool = True):
    """
    Scrape information from linkedin profiles,
    Manually scrape the information from the linkedin profile
    """
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json"
        response = requests.get(linkedin_profile_url, timeout=10)
        # print(response.text)
        return extract_valid_data(response.json())
    else:
        url = "https://api.scrapin.io/v1/enrichment/profile"
        params = {
            "apikey": os.getenv("SCRAPIN_API_KEY"),
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(url, params=params, timeout=10)
        """
          {"success":true,"credits_left":99,"rate_limit_left":99,
          "person":{"publicIdentifier":"eden-marco","linkedInIdentifier":"ACoAABx4394BeQhL15XiUqnQf7d9fobHXw13SMo","memberIdentifier":"477683678","linkedInUrl":"https://www.linkedin.com/in/eden-marco",
          "firstName":"Eden","lastName":"Marco",
          "headline":"LLMs @ Google Cloud | Best-selling Udemy Instructor | Backend & GenAI | Opinions stated here are my own, not those of my company",
          "location":{"country":"United States of America","countryCode":"US"},
          "photoUrl":"https://media.licdn.com/dms/image/v2/C4D03AQGlv35ItbkHBw/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1610187870291?e=1756339200&v=beta&t=GJHEpdYZg3i7Y-UbS_ykc2oTF1YFJh0JD6jpzTjk5D4",
          "backgroundUrl":"https://media.licdn.com/dms/image/v2/C4E16AQEMHegghll9tA/profile-displaybackgroundimage-shrink_350_1400/profile-displaybackgroundimage-shrink_350_1400/0/1641673555814?e=1756339200&v=beta&t=4TdBegpFnJWrM5XRUVWu_8lcWk6FJynHB8Hq013cheY",
          "openToWork":false,"premium":true,"showVerificationBadge":true
          }
          }"""
        return extract_valid_data(response.json())


if __name__ == "__main__":
    result = scrape_linkedin_profiles(
        linkedin_profile_url="https://www.linkedin.com/in/eden-marco", mock=True
    )
    print(result)
