from crewai import Task

from agents.query_analyzer import query_analyzer
from agents.researcher import news_researcher
from agents.verifier import fact_verifier
from agents.report_writer import factcheck_report_writer


# --------------------------------------------------
# Task 1: Analyze query
# --------------------------------------------------

analyze_query_task = Task(
    description=(
        "Analyze the user's query and break it down into specific, checkable "
        "sub-claims and key questions. Identify all entities, events, organizations, "
        "and dates involved. Determine the correct time window for research: if the "
        "user specified a date or period, use exactly that; otherwise, target the "
        "most recent information available as of {current_date}. Produce a focused "
        "research plan with concrete, recency-biased search queries.\n\n"

        "The user's query is: {user_query}\n"
        "The user-specified time period (if any) is: {time_period}\n"
        "Today's date is: {current_date}"
    ),

    expected_output=(
        "A research plan listing: "
        "(1) the specific sub-claims/questions to verify, "
        "(2) the exact entities/events/dates involved, "
        "(3) the determined time window to search within, and "
        "(4) concrete, recency-biased search queries for each sub-claim."
    ),

    agent=query_analyzer
)


# --------------------------------------------------
# Task 2: Retrieve recent information
# --------------------------------------------------

retrieve_recent_info_task = Task(
    description=(
        "Using the research plan, search the web and news sources for the most recent, "
        "relevant information on every identified sub-claim and topic. Prioritize sources "
        "published within the determined time window. Use recency-biased search terms and, "
        "when the user gave no specific period, actively seek the latest available news, "
        "actions, or developments rather than older background material. For every piece "
        "of information gathered, record the source URL and its publish date, and scrape "
        "the page when needed to confirm exact dates, figures, or quotes."
    ),

    expected_output=(
        "A detailed collection of research findings covering every sub-claim, each entry "
        "including the finding itself, the source URL, and the source's publish date, "
        "clearly separating the most recent findings from older/background context."
    ),

    agent=news_researcher
)


# --------------------------------------------------
# Task 3: Verify facts
# --------------------------------------------------

verify_facts_task = Task(
    description=(
        "Review all gathered research. For each claim or finding, verify it against "
        "at least one independent, credible source. Identify conflicting information, "
        "outdated claims, potential misinformation, or gaps that still need addressing. "
        "Explicitly check whether each source's publish date falls within the required "
        "time window; if a source is stale, search for a more recent update and note "
        "whether the situation has changed."
    ),

    expected_output=(
        "A fact-verification summary that, for each sub-claim, states a status "
        "(Verified / Partially Verified / Unverified / Outdated / False), the supporting "
        "evidence, any conflicting claims found, a note on source recency and reliability, "
        "and recommended corrections or additional research needed."
    ),

    agent=fact_verifier
)


# --------------------------------------------------
# Task 4: Write final report
# --------------------------------------------------

write_factcheck_report_task = Task(
    description=(
        "Create a final fact-check report that directly answers the user's original query "
        "using only the verified, up-to-date research. Lead with a clear overall verdict "
        "(True / False / Misleading / Unverified / Needs More Context). Summarize the "
        "supporting evidence in plain language, explicitly state how recent the underlying "
        "information is using specific dates, and list every source used with its link "
        "and publish date."
    ),

    expected_output=(
        "A comprehensive, clearly structured fact-check report containing: "
        "an overall verdict, an executive summary, a detailed evidence breakdown "
        "per sub-claim, an explicit note on recency of information, and a complete "
        "list of source citations with publish dates."
    ),

    agent=factcheck_report_writer
)