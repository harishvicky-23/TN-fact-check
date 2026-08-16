from crewai import Agent, LLM
from config.agents import agents_config


# Query Analyzer Agent

config = agents_config["query_analyzer"]

# Dynamic LLM
llm = LLM(
    model=config.get("model", "gemini/gemini-3.5-flash"),
    temperature=config.get("temperature", 0)
)

query_analyzer = Agent(
    role=config["role"],
    goal=config["goal"],
    backstory=config["backstory"],
    verbose=True,
    max_rpm=150,
    max_iter=8,
    llm=llm
)