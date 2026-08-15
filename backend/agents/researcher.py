from crewai import Agent, LLM

from tools.search_tools import (
    exa_search_tool,
    scrape_website_tool
)


# Gemini LLM

llm = LLM(
    model="gemini/gemini-2.5-flash",
    temperature=0
)



# News Researcher Agent

news_researcher = Agent(
    role="Real-Time News Researcher",

    goal=(
        "Retrieve the most recent, relevant information available for each research "
        "topic -- prioritizing breaking news, official statements, recent actions, "
        "and reports published within the requested (or most recent possible) time "
        "window -- and record the exact publish date and source URL for everything found."
    ),

    backstory=(
        "You are an investigative wire-service researcher who specializes in real-time "
        "news retrieval. You know that yesterday's article is more useful than last year's, "
        "so you always search with recency-biased terms ('latest', 'today', 'this week', "
        "specific months/years) and sort mentally for the newest credible coverage first. "
        "You cross-reference multiple outlets (news sites, official government/organization "
        "pages, press releases) rather than relying on a single source, and you scrape pages "
        "when a snippet is not enough to confirm a date, figure, or direct quote."
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