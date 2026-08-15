import os

from dotenv import load_dotenv
from crewai_tools import EXASearchTool, ScrapeWebsiteTool


load_dotenv()

EXA_API_KEY = os.getenv("EXA_API_KEY")


if not EXA_API_KEY:
    raise ValueError(
        "EXA_API_KEY is not set. Please add it to your .env file."
    )


# Exa search tool

exa_search_tool = EXASearchTool()


# Website scraper

scrape_website_tool = ScrapeWebsiteTool()