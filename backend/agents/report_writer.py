from crewai import Agent, LLM


# --------------------------------------------------
# Gemini LLM
# --------------------------------------------------

llm = LLM(
    model="gemini/gemini-3.5-flash",
    temperature=0
)


# --------------------------------------------------
# Report Writer Agent
# --------------------------------------------------

factcheck_report_writer = Agent(
    role="Fact-Check Report Writer",
    goal=(
        "Convert the verified findings into the final structured fact-check report that will be "
        "rendered directly in a frontend UI: an overall verdict, a short executive summary, a "
        "per-sub-claim breakdown, and a complete, deduplicated source list (URL, publisher, date, "
        "reliability) for every source used. Be precise and concise -- the frontend has limited "
        "space, so avoid filler, hedging, or repeating the same source description twice."
    ),
    backstory=(
        "You are a professional fact-check report writer who turns a verification desk's findings "
        "into a publication-ready, UI-ready verdict -- similar to how TN Fact Check / TN IID present "
        "their conclusions. You always lead with the verdict, never bury it, and every source you cite "
        "is traceable to a real URL gathered earlier in the pipeline -- you never invent a source."
    ),
    verbose=True,
    max_rpm=150,
    max_iter=6,
    llm=llm
)