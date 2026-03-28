"""Analyst agent — interprets research findings and surfaces quantified insights."""

from agents.base_agent import BaseAgent

_INSTRUCTIONS = """
You are a sharp business intelligence analyst. Given research findings:
- Identify patterns, correlations, and anomalies in the data.
- Create structured comparisons (tables or lists) where relevant.
- Quantify insights wherever possible (percentages, growth rates, rankings).
- Highlight the top 3–5 strategic opportunities and risks.
- Structure output with headings: Key Patterns, Comparative Analysis,
  Quantified Insights, Opportunities, Risks.
- Be data-driven and precise — avoid vague generalisations.
"""


class AnalystAgent(BaseAgent):
    """Specialised for pattern recognition, comparison, and quantified insights."""

    def __init__(self) -> None:
        super().__init__(
            name="AnalystAgent",
            role="Business Intelligence Analyst",
            instructions=_INSTRUCTIONS.strip(),
        )
