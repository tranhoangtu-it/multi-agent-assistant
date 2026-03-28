"""Competitor analysis use case — prompt builder for comparing companies."""


def get_prompt(companies: str) -> dict:
    """
    Build the task + context dict for a competitor analysis request.

    Args:
        companies: Comma-separated company names (e.g. "Notion, Confluence, Coda").

    Returns:
        Dict with 'task' and 'context' keys ready for the orchestrator.
    """
    task = (
        f"Conduct a detailed competitor analysis for the following companies: {companies}\n\n"
        "For each company, cover:\n"
        "1. Company overview and core product/service\n"
        "2. Target market and customer segments\n"
        "3. Key features and differentiators\n"
        "4. Pricing model and tiers\n"
        "5. Market position and estimated market share\n"
        "6. Strengths and competitive advantages\n"
        "7. Weaknesses and known pain points\n"
        "8. Recent strategic moves (funding, partnerships, product launches)\n\n"
        "Then provide a comparative summary table and identify the clear winner in each dimension."
    )

    context = (
        f"Companies to analyse: {companies}\n"
        "Use case: Competitor Analysis\n"
        "Audience: Product managers and business strategists evaluating the competitive landscape."
    )

    return {"task": task, "context": context}
