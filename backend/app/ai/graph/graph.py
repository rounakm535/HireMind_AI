from langgraph.graph import StateGraph, START, END
from app.ai.graph.state import ScreenResumeState
from app.ai.graph.nodes import (
    parse_resume_node,
    generate_embeddings_node,
    store_vector_node,
    retrieve_candidates_node,
    resume_matching_node,
    skill_gap_analysis_node,
    ranking_node,
    summary_generation_node,
    interview_questions_node,
)
from app.ai.graph.router import route_after_node

# Initialize the workflow graph
workflow = StateGraph(ScreenResumeState)

# 1. Register nodes
workflow.add_node("parse_resume", parse_resume_node)
workflow.add_node("generate_embeddings", generate_embeddings_node)
workflow.add_node("store_vector", store_vector_node)
workflow.add_node("retrieve_candidates", retrieve_candidates_node)
workflow.add_node("resume_matching", resume_matching_node)
workflow.add_node("skill_gap_analysis", skill_gap_analysis_node)
workflow.add_node("ranking", ranking_node)
workflow.add_node("summary_generation", summary_generation_node)
workflow.add_node("interview_questions", interview_questions_node)

# Helper node to handle retries and reset errors
async def retry_incrementer_node(state: ScreenResumeState) -> dict:
    return {
        "retry_count": state.get("retry_count", 0) + 1,
        "errors": [] # Clear errors to retry
    }
workflow.add_node("retry_incrementer", retry_incrementer_node)

# 2. Build graph routing logic with conditional edges (Retries & Branching)
# Flow starts at parse_resume
workflow.add_edge(START, "parse_resume")

# Node: parse_resume
workflow.add_conditional_edges(
    "parse_resume",
    route_after_node,
    {
        "continue": "generate_embeddings",
        "retry": "retry_incrementer",
        "error_end": END
    }
)

# Node: generate_embeddings
workflow.add_conditional_edges(
    "generate_embeddings",
    route_after_node,
    {
        "continue": "store_vector",
        "retry": "retry_incrementer",
        "error_end": END
    }
)

# Node: store_vector
workflow.add_conditional_edges(
    "store_vector",
    route_after_node,
    {
        "continue": "retrieve_candidates",
        "retry": "retry_incrementer",
        "error_end": END
    }
)

# Node: retrieve_candidates
workflow.add_conditional_edges(
    "retrieve_candidates",
    route_after_node,
    {
        "continue": "resume_matching",
        "retry": "retry_incrementer",
        "error_end": END
    }
)

# Node: resume_matching
workflow.add_conditional_edges(
    "resume_matching",
    route_after_node,
    {
        "continue": "skill_gap_analysis",
        "retry": "retry_incrementer",
        "error_end": END
    }
)

# Node: skill_gap_analysis
workflow.add_conditional_edges(
    "skill_gap_analysis",
    route_after_node,
    {
        "continue": "ranking",
        "retry": "retry_incrementer",
        "error_end": END
    }
)

# Node: ranking
workflow.add_conditional_edges(
    "ranking",
    route_after_node,
    {
        "continue": "summary_generation",
        "retry": "retry_incrementer",
        "error_end": END
    }
)

# Node: summary_generation
workflow.add_conditional_edges(
    "summary_generation",
    route_after_node,
    {
        "continue": "interview_questions",
        "retry": "retry_incrementer",
        "error_end": END
    }
)

# Node: interview_questions
workflow.add_conditional_edges(
    "interview_questions",
    route_after_node,
    {
        "continue": END,
        "retry": "retry_incrementer",
        "error_end": END
    }
)

# Retry Route target: Route back to the start or retry state
# For standard parsing retry loop, we route back to parse_resume
workflow.add_edge("retry_incrementer", "parse_resume")

# Compile graph
resume_screening_graph = workflow.compile()
