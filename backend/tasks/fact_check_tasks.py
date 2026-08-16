from crewai import Task
from config.tasks import tasks_config

from agents.query_analyzer import query_analyzer
from agents.researcher import researcher
from agents.verifier import fact_verifier
from agents.report_writer import factcheck_report_writer

from Models.models import FactCheckReport

# --------------------------------------------------
# Task 1: Analyze query
# --------------------------------------------------

config_aq = tasks_config["analyze_query"]

analyze_query_task = Task(
    description=config_aq["description"],
    expected_output=config_aq["expected_output"],
    agent=query_analyzer,
)


# --------------------------------------------------
# Task 2: Gather evidence
# --------------------------------------------------

config_ge = tasks_config["gather_evidence"]

gather_evidence_task = Task(
    description=config_ge["description"],
    expected_output=config_ge["expected_output"],
    agent=researcher,
)


# --------------------------------------------------
# Task 3: Verify facts
# --------------------------------------------------

config_vf = tasks_config["verify_facts"]

verify_facts_task = Task(
    description=config_vf["description"],
    expected_output=config_vf["expected_output"],
    agent=fact_verifier,
)


# --------------------------------------------------
# Task 4: Write final report
# --------------------------------------------------

config_wr = tasks_config["write_factcheck_report"]

write_factcheck_report_task = Task(
    description=config_wr["description"],
    expected_output=config_wr["expected_output"],
    agent=factcheck_report_writer,
    output_pydantic=FactCheckReport,
)