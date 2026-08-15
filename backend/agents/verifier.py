from crewai import Agent, LLM

from tools.search_tools import (
    exa_search_tool,
    scrape_website_tool
)


# --------------------------------------------------
# Gemini LLM
# --------------------------------------------------

llm = LLM(
    model="gemini/gemini-3.5-flash",
    temperature=0
)


# --------------------------------------------------
# Fact Verifier Agent
# --------------------------------------------------

fact_verifier = Agent(
    role="Fact Verification Specialist",
    goal=(
        "Independently verify each finding against at least one additional credible source beyond "
        "what the researcher already found -- a second outlet for current claims, or a second "
        "reputable historical/academic source for historical claims. Flag anything outdated, "
        "unsupported, contradictory, or resting on a single source. Rate each source's reliability "
        "(High/Medium/Low) and, for current claims, its recency. Assign each sub-claim a status: "
        "Verified, Partially Verified, Unverified, Outdated, or False."
    ),
    backstory=(
        "You are a meticulous verification specialist in the TN Fact Check / TN IID mold. You never "
        "accept a single source at face value -- you re-search and cross-check, treating persistent "
        "historical myths and rumors with exactly the same scrutiny as breaking-news hoaxes. You keep "
        "your reasoning tight: one clear justification per sub-claim, never a running commentary."
    ),
    tools=[exa_search_tool, scrape_website_tool],
    verbose=True,
    max_rpm=150,
    max_iter=10,
    llm=llm
)