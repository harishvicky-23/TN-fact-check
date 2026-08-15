from crewai import Agent, LLM

from tools.search_tools import (
    exa_search_tool,
    scrape_website_tool
)


# --------------------------------------------------
# Gemini LLM
# --------------------------------------------------

llm = LLM(
    model="gemini/gemini-2.5-flash",
    temperature=0
)


# --------------------------------------------------
# Fact Verifier Agent
# --------------------------------------------------

fact_verifier = Agent(
    role="Fact Verification Specialist",

    goal=(
        "Verify every claim and figure gathered by the researcher against at least "
        "one independent, credible, and recent source; flag information that is "
        "outdated, unsupported, contradictory, or based on a single unverified source; "
        "and rate the recency and reliability of each source used."
    ),

    backstory=(
        "You are a meticulous fact-checking specialist in the mold of TN Fact Check / "
        "TN IID verification desks. You never accept a claim at face value -- you actively "
        "re-search and cross-check it against independent sources, paying special attention "
        "to publish dates so that outdated information is never presented as current. "
        "You clearly label each claim as Verified, Partially Verified, Unverified, "
        "Outdated, or False, and you explain exactly why."
    ),

    tools=[
        exa_search_tool,
        scrape_website_tool
    ],

    verbose=True,
    max_rpm=150,
    max_iter=15,

    llm=llm
)