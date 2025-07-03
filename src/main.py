from dotenv import load_dotenv
from ice_breaker import linkedin_profile_IB

load_dotenv()

if __name__ == "__main__":
    # LinkedIn Profile Summary Ice Breaker
    search_query = "Elliot Yibaebi Yibalua"

    profile = linkedin_profile_IB.get_linkedin_profile_info(
        name_with_unique_info=search_query
    )

    res = linkedin_profile_IB.create_linkedin_profile_summary(profile=profile)

    print(res)
