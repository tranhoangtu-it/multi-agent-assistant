"""Orchestrator — coordinates Research → Analyst → Writer pipeline."""

from typing import Callable, Optional
from agents.research_agent import ResearchAgent
from agents.analyst_agent import AnalystAgent
from agents.writer_agent import WriterAgent


class Orchestrator:
    """
    Runs the three-agent pipeline sequentially.
    Each agent receives the previous agent's output as context.
    """

    def __init__(self) -> None:
        self.research_agent = ResearchAgent()
        self.analyst_agent = AnalystAgent()
        self.writer_agent = WriterAgent()

    async def run_pipeline(
        self,
        use_case: str,
        input_data: str,
        on_progress: Optional[Callable[[str, str, str], None]] = None,
    ) -> dict:
        """
        Execute the full Research → Analysis → Report pipeline.

        Args:
            use_case:    Short label describing the type of task (e.g. "Market Research").
            input_data:  The raw user input (topic, company names, transcript, etc.).
            on_progress: Optional callback(agent_name, status, output) for UI updates.

        Returns:
            Dict with keys: research, analysis, report, agents_used.
        """
        results: dict = {"research": "", "analysis": "", "report": "", "agents_used": []}

        # --- Step 1: Research ---
        _notify(on_progress, "ResearchAgent", "running", "")
        research_out = await self.research_agent.run(
            task=f"[{use_case}] {input_data}",
        )
        results["research"] = research_out
        results["agents_used"].append("ResearchAgent")
        _notify(on_progress, "ResearchAgent", "done", research_out)

        # --- Step 2: Analysis ---
        _notify(on_progress, "AnalystAgent", "running", "")
        analysis_out = await self.analyst_agent.run(
            task=f"Analyse the following research for: {use_case}\nInput: {input_data}",
            context=research_out,
        )
        results["analysis"] = analysis_out
        results["agents_used"].append("AnalystAgent")
        _notify(on_progress, "AnalystAgent", "done", analysis_out)

        # --- Step 3: Write Report ---
        _notify(on_progress, "WriterAgent", "running", "")
        combined_context = f"RESEARCH:\n{research_out}\n\nANALYSIS:\n{analysis_out}"
        report_out = await self.writer_agent.run(
            task=f"Write a comprehensive business report for: {use_case}\nSubject: {input_data}",
            context=combined_context,
        )
        results["report"] = report_out
        results["agents_used"].append("WriterAgent")
        _notify(on_progress, "WriterAgent", "done", report_out)

        return results


def _notify(
    callback: Optional[Callable[[str, str, str], None]],
    agent_name: str,
    status: str,
    output: str,
) -> None:
    """Fire the progress callback if one was provided."""
    if callback:
        callback(agent_name, status, output)
