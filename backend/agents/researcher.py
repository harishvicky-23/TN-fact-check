from crewai import Agent, LLM
from config.agents import agents_config

from tools.search_tools import (
    exa_search_tool,
    scrape_website_tool
)


# News Researcher Agent

config = agents_config["researcher"]

# Dynamic LLM
llm = LLM(
    model=config.get("model", "gemini/gemini-3.5-flash"),
    temperature=config.get("temperature", 0)
)

researcher = Agent(
    role=config["role"],
    goal=config["goal"],
    backstory=config["backstory"],
    tools=[
        exa_search_tool,
        scrape_website_tool
    ],
    verbose=True,
    max_rpm=150,
    max_iter=10,
    llm=llm
)