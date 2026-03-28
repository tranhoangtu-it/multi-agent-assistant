"""Tests for BaseAgent and Orchestrator — all OpenAI calls are mocked."""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from agents.base_agent import BaseAgent
from agents.orchestrator import Orchestrator


def _make_mock_client() -> MagicMock:
    """Return a MagicMock that stands in for AsyncOpenAI without a real API key."""
    return MagicMock()


# ── BaseAgent init ────────────────────────────────────────────────────────────

def test_base_agent_init():
    """Constructor stores name, role, and instructions correctly."""
    agent = BaseAgent(
        name="TestAgent",
        role="Test Role",
        instructions="Do the thing.",
        client=_make_mock_client(),
    )
    assert agent.name == "TestAgent"
    assert agent.role == "Test Role"
    assert agent.instructions == "Do the thing."


# ── BaseAgent.run with mocked OpenAI ─────────────────────────────────────────

async def test_base_agent_run_mocked():
    """run() passes the correct messages to the OpenAI client and returns content."""
    mock_client = _make_mock_client()

    agent = BaseAgent(
        name="TestAgent",
        role="Tester",
        instructions="Test instructions.",
        client=mock_client,
    )

    # Build a fake response object matching openai SDK shape
    fake_message = MagicMock()
    fake_message.content = "Mocked response"
    fake_choice = MagicMock()
    fake_choice.message = fake_message
    fake_response = MagicMock()
    fake_response.choices = [fake_choice]

    mock_create = AsyncMock(return_value=fake_response)
    mock_client.chat.completions.create = mock_create

    result = await agent.run(task="Summarise the market.", context="Some prior context.")

    assert result == "Mocked response"

    # Verify the call included both system and user messages
    call_kwargs = mock_create.call_args.kwargs
    messages = call_kwargs["messages"]
    assert messages[0]["role"] == "system"
    assert "Tester" in messages[0]["content"]
    assert messages[1]["role"] == "user"
    assert "Summarise the market." in messages[1]["content"]
    assert "Some prior context." in messages[1]["content"]


# ── Orchestrator pipeline with mocked agents ─────────────────────────────────

async def test_orchestrator_pipeline_mocked():
    """Pipeline runs agents sequentially and returns correct output structure."""
    # Patch AsyncOpenAI so Orchestrator.__init__ never needs a real API key
    with patch("agents.base_agent.AsyncOpenAI", return_value=_make_mock_client()):
        orchestrator = Orchestrator()

    orchestrator.research_agent.run = AsyncMock(return_value="Research output")
    orchestrator.analyst_agent.run = AsyncMock(return_value="Analysis output")
    orchestrator.writer_agent.run = AsyncMock(return_value="Report output")

    progress_calls: list[tuple] = []

    def capture_progress(agent_name: str, status: str, output: str) -> None:
        progress_calls.append((agent_name, status))

    results = await orchestrator.run_pipeline(
        use_case="Market Research",
        input_data="AI SaaS tools",
        on_progress=capture_progress,
    )

    # Verify output dict structure
    assert results["research"] == "Research output"
    assert results["analysis"] == "Analysis output"
    assert results["report"] == "Report output"
    assert results["agents_used"] == ["ResearchAgent", "AnalystAgent", "WriterAgent"]

    # Verify sequential execution (running → done for each agent in order)
    expected = [
        ("ResearchAgent", "running"),
        ("ResearchAgent", "done"),
        ("AnalystAgent", "running"),
        ("AnalystAgent", "done"),
        ("WriterAgent", "running"),
        ("WriterAgent", "done"),
    ]
    assert progress_calls == expected

    # Verify analyst received research output as context
    analyst_call_kwargs = orchestrator.analyst_agent.run.call_args.kwargs
    assert "Research output" in analyst_call_kwargs.get("context", "")

    # Verify writer received both research and analysis as context
    writer_call_kwargs = orchestrator.writer_agent.run.call_args.kwargs
    assert "Research output" in writer_call_kwargs.get("context", "")
    assert "Analysis output" in writer_call_kwargs.get("context", "")
