import os
import requests
from sqlalchemy import null


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    Scrape information from linkedin profiles
    """

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/Yibaebi/f8253d41b59da5d65737085612d698ae/raw/04d9abc78ea3d230df7b0108ad968be96e4e7159/.json"
        response = requests.get(linkedin_profile_url, timeout=10)

    else:
        api_key = os.getenv("PROXYCURL_API_KEY")
        headers = {"Authorization": "Bearer " + api_key}
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"

        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=headers,
            timeout=10,
        )

    data: dict = response.json()

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None)
        and k
        not in [
            "accomplishment_patents",
            "accomplishment_projects",
            "volunteer_work",
            "activities",
        ]
    }

    return data
