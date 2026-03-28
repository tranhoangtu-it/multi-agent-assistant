"""Research agent — gathers and structures information on a given topic."""

from agents.base_agent import BaseAgent

_INSTRUCTIONS = """
You are a meticulous researcher. For every topic you are given:
- Provide a comprehensive overview with key facts and figures.
- Identify major trends and recent developments (simulate based on your knowledge).
- List credible source types that would be consulted (e.g., industry reports, news, papers).
- Structure your findings with clear headings: Overview, Key Facts, Trends, Sources.
- Be concise but thorough — aim for depth over brevity.
"""


class ResearchAgent(BaseAgent):
    """Specialised for information gathering and source-structured findings."""

    def __init__(self) -> None:
        super().__init__(
            name="ResearchAgent",
            role="Senior Research Analyst",
            instructions=_INSTRUCTIONS.strip(),
        )
