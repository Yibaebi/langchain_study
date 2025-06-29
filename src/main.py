from ice_breaker import linkedin_profile_IB


if __name__ == "__main__":
    # LinkedIn Profile Summary Ice Breaker
    profile = linkedin_profile_IB.get_linkedin_profile_info()
    res = linkedin_profile_IB.create_linkedin_profile_summary(profile=profile)

    print(res)
