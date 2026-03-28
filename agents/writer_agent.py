"""Writer agent — synthesises research + analysis into a polished business report."""

from agents.base_agent import BaseAgent

_INSTRUCTIONS = """
You are a professional business report writer. Given research and analysis inputs:
- Synthesise all inputs into a cohesive, well-structured report.
- Use clear section headings: Executive Summary, Background, Key Findings,
  Strategic Implications, Recommendations, Conclusion.
- Write in a professional yet accessible tone suitable for C-suite readers.
- Open with a concise executive summary (3–5 sentences max).
- End with 3–5 concrete, actionable recommendations.
- Format in Markdown for clean rendering.
"""


class WriterAgent(BaseAgent):
    """Specialised for producing polished, structured Markdown business reports."""

    def __init__(self) -> None:
        super().__init__(
            name="WriterAgent",
            role="Professional Report Writer",
            instructions=_INSTRUCTIONS.strip(),
        )
