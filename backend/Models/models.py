from pydantic import BaseModel, Field
from typing import List, Optional


class SourceCitation(BaseModel):
    title: str = Field(description="Title of the source article/page")
    url: str = Field(description="Direct URL of the source")
    publisher: str = Field(description="Publication, organization, or site name")
    published_date: Optional[str] = Field(
        default=None,
        description="Publish or last-updated date (YYYY-MM-DD if known, else 'unknown')"
    )
    reliability: str = Field(description="High, Medium, or Low")
    supports: str = Field(description="Confirms, Contradicts, or Partially confirms the sub-claim")


class SubClaimResult(BaseModel):
    sub_claim: str = Field(description="The specific sub-claim being checked")
    status: str = Field(description="Verified, Partially Verified, Unverified, Outdated, or False")
    explanation: str = Field(description="1-3 sentence plain-language explanation of the status")
    sources: List[SourceCitation] = Field(description="Sources supporting this sub-claim's status")


class FactCheckReport(BaseModel):
    user_query: str = Field(description="The original user query/claim")
    is_historical: bool = Field(
        description="True if the claim is about a settled past event/figure, False if current/ongoing"
    )
    time_window_used: str = Field(description="The time window/period the research was grounded in")
    overall_verdict: str = Field(
        description="True, False, Misleading, Unverified, or Needs More Context"
    )
    confidence: str = Field(description="High, Medium, or Low confidence in the verdict")
    executive_summary: str = Field(description="A 2-4 sentence plain-language summary of the verdict and why")
    sub_claims: List[SubClaimResult] = Field(description="Per sub-claim verification breakdown")
    all_sources: List[SourceCitation] = Field(
        description="Deduplicated list of every source used across the whole investigation"
    )
    report_generated_on: str = Field(description="Date the report was generated")