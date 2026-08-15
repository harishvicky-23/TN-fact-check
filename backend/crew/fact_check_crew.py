from crewai import Crew, Process
from typing import Callable, Any

from agents.query_analyzer import query_analyzer
from agents.researcher import researcher
from agents.verifier import fact_verifier
from agents.report_writer import factcheck_report_writer

from tasks.fact_check_tasks import (
    analyze_query_task,
    gather_evidence_task,
    verify_facts_task,
    write_factcheck_report_task
)

# create the crew with the defined agents and tasks
fact_check_crew = Crew(
    agents=[
        query_analyzer,
        researcher,
        fact_verifier,
        factcheck_report_writer
    ],
    tasks=[
        analyze_query_task,
        gather_evidence_task,
        verify_facts_task,
        write_factcheck_report_task
    ],
    process=Process.sequential,
    verbose=True
)

def run_fact_check(
    user_query: str,
    time_period: str,
    current_date: str,
    on_task_completed: Callable[[str, Any], None] = None
):
    # Set up task callbacks dynamically for this run
    if on_task_completed:
        def callback_1(output):
            on_task_completed("analyzing_done", output)
        
        def callback_2(output):
            on_task_completed("gathering_done", output)
            
        def callback_3(output):
            on_task_completed("verifying_done", output)
            
        analyze_query_task.callback = callback_1
        gather_evidence_task.callback = callback_2
        verify_facts_task.callback = callback_3
    else:
        analyze_query_task.callback = None
        gather_evidence_task.callback = None
        verify_facts_task.callback = None

    result = fact_check_crew.kickoff(
        inputs={
            "user_query": user_query,
            "time_period": time_period,
            "current_date": current_date
        }
    )

    return result