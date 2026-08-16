from crewai import Agent, LLM
from config.agents import agents_config


# --------------------------------------------------
# Report Writer Agent
# --------------------------------------------------

config = agents_config["report_writer"]

# Dynamic LLM
llm = LLM(
    model=config.get("model", "gemini/gemini-3.5-flash"),
    temperature=config.get("temperature", 0)
)

factcheck_report_writer = Agent(
    role=config["role"],
    goal=config["goal"],
    backstory=config["backstory"],
    verbose=True,
    max_rpm=150,
    max_iter=6,
    llm=llm
)