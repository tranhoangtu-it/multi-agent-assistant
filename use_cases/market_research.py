"""Market research use case — prompt builder for researching a market or industry."""


def get_prompt(topic: str) -> dict:
    """
    Build the task + context dict for a market research request.

    Args:
        topic: The market or industry to research (e.g. "AI SaaS for SMBs").

    Returns:
        Dict with 'task' and 'context' keys ready for the orchestrator.
    """
    task = (
        f"Conduct a comprehensive market research report on: {topic}\n\n"
        "Cover the following dimensions:\n"
        "1. Market size and growth rate (current and projected)\n"
        "2. Key market segments and target demographics\n"
        "3. Major players and their market share\n"
        "4. Emerging trends and technological drivers\n"
        "5. Regulatory or macro-economic factors\n"
        "6. Barriers to entry and competitive dynamics\n"
        "7. Key opportunities and unmet needs\n"
        "8. Potential risks and threats"
    )

    context = (
        f"Topic: {topic}\n"
        "Use case: Market Research\n"
        "Audience: Business strategists and investors seeking actionable intelligence."
    )

    return {"task": task, "context": context}
