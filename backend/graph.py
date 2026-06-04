from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import END

from compliance_agent import compliance_node
from negotiation_agent import negotiation_node
from planner import create_plan
from executive_summary_agent import executive_summary_node
from playbook_agent import playbook_node
from retrieval import analyze_contract_risk


class ContractState(TypedDict):

    contract_text: str
    contract_type: str
    industry: str

    persona: str
    custom_knowledge: str

    plan: dict

    risks: list

    compliance: list

    playbook_conflicts: list

    negotiations: list

    executive_summary: str

    final_output: dict

def planner_node(state):

    plan = create_plan(
        contract_text=state["contract_text"],
        contract_type=state["contract_type"],
        industry=state["industry"],
        persona=state["persona"],
        custom_knowledge=state["custom_knowledge"]
    )

    return {
        "plan": plan
    }


def risk_node(state):

    risks = analyze_contract_risk(
        state["contract_text"],
        state["contract_type"],
        state["industry"],
        state["persona"],
        state["custom_knowledge"]
    )

    return {
        "risks": risks
    }



def judge_node(state):

    high = 0
    medium = 0
    low = 0

    for risk in state["risks"]:

        level = risk.get(
            "risk_level",
            ""
        ).lower()

        if level == "high":
            high += 1

        elif level == "medium":
            medium += 1

        else:
            low += 1

    score = 100

    score -= high * 12
    score -= medium * 6
    score -= low * 2

    score = max(score, 0)

    return {
        "final_output": {
            "health_score": score,
            "executive_summary": state["executive_summary"],
            "plan": state["plan"],
            "risks": state["risks"],
            "compliance": state["compliance"],
            "negotiations": state["negotiations"],
            "playbook_conflicts": state["playbook_conflicts"]
        }
    }
workflow = StateGraph(ContractState)

workflow.add_node(
    "planner",
    planner_node
)

workflow.add_node(
    "risk",
    risk_node
)

workflow.add_node(
    "judge",
    judge_node
)
workflow.add_node(
    "compliance",
    compliance_node
)

workflow.add_node(
    "playbook",
    playbook_node
)
workflow.add_node(
    "negotiation",
    negotiation_node
)
workflow.add_node(
    "summary",
    executive_summary_node
)

workflow.set_entry_point("planner")
workflow.add_edge(
    "planner",
    "risk"
)

workflow.add_edge(
    "risk",
    "playbook"
)

workflow.add_edge(
    "playbook",
    "compliance"
)

workflow.add_edge(
    "compliance",
    "negotiation"
)

workflow.add_edge(
    "negotiation",
    "summary"
)

workflow.add_edge(
    "summary",
    "judge"
)
workflow.add_edge(
    "judge",
    END
)

graph = workflow.compile()