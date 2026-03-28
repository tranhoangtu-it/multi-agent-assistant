"""Streamlit UI for the Multi-Agent Business Assistant."""

import asyncio
import streamlit as st
from agents.orchestrator import Orchestrator
from use_cases import market_research, competitor_analysis, meeting_summary

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Business Assistant",
    page_icon="🤖",
    layout="wide",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Multi-Agent Business Assistant")
    st.markdown("Powered by **3 specialised AI agents** working in sequence.")
    st.divider()

    use_case = st.selectbox(
        "Select Use Case",
        ["Market Research", "Competitor Analysis", "Meeting Summary"],
    )

    st.divider()
    st.markdown("**Agent Pipeline**")
    st.markdown("1. ResearchAgent — gathers facts")
    st.markdown("2. AnalystAgent — finds patterns")
    st.markdown("3. WriterAgent — drafts the report")

# ── Main area ─────────────────────────────────────────────────────────────────
st.header(f"{use_case}")

# Dynamic input label per use case
_labels = {
    "Market Research": ("Market or industry to research", "e.g. AI SaaS for small businesses"),
    "Competitor Analysis": ("Companies to compare (comma-separated)", "e.g. Notion, Confluence, Coda"),
    "Meeting Summary": ("Paste your meeting transcript", "Paste the full transcript here..."),
}
label, placeholder = _labels[use_case]

if use_case == "Meeting Summary":
    user_input = st.text_area(label, placeholder=placeholder, height=200)
else:
    user_input = st.text_input(label, placeholder=placeholder)

run_btn = st.button("Run Analysis", type="primary", disabled=not user_input)

# ── Pipeline execution ────────────────────────────────────────────────────────
if run_btn and user_input:
    # Build prompt dict from the selected use case module
    prompt_builders = {
        "Market Research": market_research.get_prompt,
        "Competitor Analysis": competitor_analysis.get_prompt,
        "Meeting Summary": meeting_summary.get_prompt,
    }
    prompt = prompt_builders[use_case](user_input)

    # Placeholders for live progress
    st.divider()
    st.subheader("Agent Progress")
    progress_slots = {
        "ResearchAgent": st.empty(),
        "AnalystAgent": st.empty(),
        "WriterAgent": st.empty(),
    }
    output_slots: dict = {}

    def on_progress(agent_name: str, status: str, output: str) -> None:
        """Update UI with agent status in real time."""
        icon = "⏳" if status == "running" else "✅"
        progress_slots[agent_name].markdown(f"{icon} **{agent_name}** — {status}")
        if status == "done" and output:
            output_slots[agent_name] = output

    orchestrator = Orchestrator()

    with st.spinner("Running multi-agent pipeline…"):
        results = asyncio.run(
            orchestrator.run_pipeline(
                use_case=use_case,
                input_data=prompt["task"],
                on_progress=on_progress,
            )
        )

    # ── Agent outputs (expandable) ─────────────────────────────────────────
    st.divider()
    st.subheader("Agent Outputs")

    with st.expander("ResearchAgent output", expanded=False):
        st.markdown(results["research"])

    with st.expander("AnalystAgent output", expanded=False):
        st.markdown(results["analysis"])

    # ── Final report ───────────────────────────────────────────────────────
    st.divider()
    st.subheader("Final Report")
    st.markdown(results["report"])

    # Download button
    st.download_button(
        label="Download report as Markdown",
        data=results["report"],
        file_name=f"{use_case.lower().replace(' ', '_')}_report.md",
        mime="text/markdown",
    )
