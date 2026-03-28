"""Tests for use case prompt builders — no OpenAI calls needed."""

from use_cases import market_research, competitor_analysis, meeting_summary


# ── Market Research ───────────────────────────────────────────────────────────

def test_market_research_prompt_returns_required_keys():
    """get_prompt returns a dict with both 'task' and 'context' keys."""
    result = market_research.get_prompt("AI SaaS for SMBs")
    assert isinstance(result, dict)
    assert "task" in result
    assert "context" in result


def test_market_research_prompt_contains_topic():
    """Prompt text includes the supplied topic string."""
    topic = "cloud ERP solutions"
    result = market_research.get_prompt(topic)
    assert topic in result["task"]
    assert topic in result["context"]


# ── Competitor Analysis ───────────────────────────────────────────────────────

def test_competitor_analysis_prompt_returns_required_keys():
    """get_prompt returns a dict with both 'task' and 'context' keys."""
    result = competitor_analysis.get_prompt("Notion, Confluence")
    assert isinstance(result, dict)
    assert "task" in result
    assert "context" in result


def test_competitor_analysis_prompt_contains_company_names():
    """Prompt text includes the supplied company names."""
    companies = "Salesforce, HubSpot, Pipedrive"
    result = competitor_analysis.get_prompt(companies)
    assert companies in result["task"]
    assert companies in result["context"]


# ── Meeting Summary ───────────────────────────────────────────────────────────

def test_meeting_summary_prompt_returns_required_keys():
    """get_prompt returns a dict with both 'task' and 'context' keys."""
    result = meeting_summary.get_prompt("Alice: Let's ship next Friday.")
    assert isinstance(result, dict)
    assert "task" in result
    assert "context" in result


def test_meeting_summary_prompt_contains_transcript():
    """Prompt task text includes the supplied transcript content."""
    transcript = "Bob: We decided to cut the beta feature. Alice: Agreed."
    result = meeting_summary.get_prompt(transcript)
    assert transcript in result["task"]


def test_meeting_summary_prompt_references_transcript_label():
    """Prompt contains the TRANSCRIPT section marker for clear context."""
    result = meeting_summary.get_prompt("Some meeting text.")
    assert "TRANSCRIPT" in result["task"]
