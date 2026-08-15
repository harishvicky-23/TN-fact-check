from crewai import Crew, Process

from agents.query_analyzer import query_analyzer
from agents.researcher import news_researcher
from agents.verifier import fact_verifier
from agents.report_writer import factcheck_report_writer

from tasks.fact_check_tasks import (
    analyze_query_task,
    retrieve_recent_info_task,
    verify_facts_task,
    write_factcheck_report_task
)


# --------------------------------------------------
# Create Crew
# --------------------------------------------------

fact_check_crew = Crew(

    agents=[
        query_analyzer,
        news_researcher,
        fact_verifier,
        factcheck_report_writer
    ],

    tasks=[
        analyze_query_task,
        retrieve_recent_info_task,
        verify_facts_task,
        write_factcheck_report_task
    ],

    process=Process.sequential,

    verbose=True
)


# --------------------------------------------------
# Run fact check
# --------------------------------------------------

def run_fact_check(
    user_query: str,
    time_period: str,
    current_date: str
):

    result = fact_check_crew.kickoff(
        inputs={
            "user_query": user_query,
            "time_period": time_period,
            "current_date": current_date
        }
    )

    return result