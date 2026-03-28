"""Meeting summary use case — prompt builder for summarising meeting transcripts."""


def get_prompt(transcript: str) -> dict:
    """
    Build the task + context dict for a meeting summary request.

    Args:
        transcript: Raw meeting transcript text.

    Returns:
        Dict with 'task' and 'context' keys ready for the orchestrator.
    """
    task = (
        "Analyse and summarise the following meeting transcript.\n\n"
        "Extract and structure:\n"
        "1. Meeting purpose and attendees (if mentioned)\n"
        "2. Key decisions made (with context)\n"
        "3. Action items — each with: owner, task description, deadline\n"
        "4. Open questions or unresolved issues\n"
        "5. Key discussion points and their outcomes\n"
        "6. Risks or blockers identified\n\n"
        "Finally, draft a professional follow-up email summarising decisions "
        "and action items for all attendees.\n\n"
        f"--- TRANSCRIPT ---\n{transcript}"
    )

    context = (
        "Use case: Meeting Summary\n"
        "Audience: Meeting participants and stakeholders needing a clear record "
        "of decisions and next steps."
    )

    return {"task": task, "context": context}
