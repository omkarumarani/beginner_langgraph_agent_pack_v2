"""A small LangGraph workflow for a beginner domain agent pack.

This is intentionally deterministic: it teaches safe workflow structure before
introducing an LLM. A future platform may replace the reasoning inside nodes
with a governed model call without changing the pack's YAML boundaries.
"""
from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict, total=False):
    trigger: dict
    evidence: dict
    observation: str
    hypothesis: str
    diagnosis: str
    confidence: float
    recommendation: str
    verified: bool
    notes: list[str]


def observe(state: AgentState) -> AgentState:
    trigger = state["trigger"]
    return {"observation": f"Investigating {trigger['symptom']} on {trigger['application']}.", "notes": []}


def hypothesize(state: AgentState) -> AgentState:
    evidence = state["evidence"]
    if evidence["recent_deployment"]:
        hypothesis = "A recent deployment introduced a regression."
    elif evidence["database_p99_ms"] > 1000:
        hypothesis = "Database latency is contributing to application failure."
    else:
        hypothesis = "The available evidence is insufficient for a safe conclusion."
    return {"hypothesis": hypothesis}


def gather_evidence(state: AgentState) -> AgentState:
    # In a real platform this node requests named, approved capabilities.
    # The starter pack receives scenario evidence to stay runnable with no credentials.
    return {"notes": state.get("notes", []) + ["Evidence gathered from approved scenario inputs."]}


def reason(state: AgentState) -> AgentState:
    evidence = state["evidence"]
    if evidence["recent_deployment"] and evidence["traffic_change"] == "flat":
        return {"diagnosis": "Deployment regression is the likely cause.", "confidence": 0.85}
    if evidence["database_p99_ms"] > 1000:
        return {"diagnosis": "Database latency is likely contributing to the 503 errors.", "confidence": 0.82}
    return {"diagnosis": "Cause is unresolved with current evidence.", "confidence": 0.35}


def recommend(state: AgentState) -> AgentState:
    diagnosis = state["diagnosis"].lower()
    if "deployment" in diagnosis:
        return {"recommendation": "application.rollback_deployment"}
    # Database is deliberately escalated: it is outside this starter agent's ownership.
    return {"recommendation": "incident.escalate"}


def verify(state: AgentState) -> AgentState:
    # An execution success is not proof of incident resolution.
    # In real use, post-action platform evidence would decide this value.
    return {"verified": state["recommendation"] == "application.rollback_deployment"}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("observe", observe)
    graph.add_node("hypothesize", hypothesize)
    graph.add_node("gather_evidence", gather_evidence)
    graph.add_node("reason", reason)
    graph.add_node("recommend", recommend)
    graph.add_node("verify", verify)
    graph.add_edge(START, "observe")
    graph.add_edge("observe", "hypothesize")
    graph.add_edge("hypothesize", "gather_evidence")
    graph.add_edge("gather_evidence", "reason")
    graph.add_edge("reason", "recommend")
    graph.add_edge("recommend", "verify")
    graph.add_edge("verify", END)
    return graph.compile()


def run_scenario(scenario: dict) -> AgentState:
    return build_graph().invoke({"trigger": scenario["trigger"], "evidence": scenario["evidence"]})
