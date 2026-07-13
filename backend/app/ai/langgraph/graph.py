from langgraph.graph import StateGraph, START, END
from app.ai.langgraph.state import ScreenResumeState
from app.ai.langgraph.nodes import (
    resume_parsing_node,
    embedding_generation_node,
    resume_matching_node,
    skill_gap_analysis_node,
    candidate_ranking_node,
    interview_question_generation_node,
    summary_generation_node,
)

# Initialize the state graph
workflow = StateGraph(ScreenResumeState)

# Register nodes
workflow.add_node("parse_resume", resume_parsing_node)
workflow.add_node("generate_embeddings", embedding_generation_node)
workflow.add_node("match_resume", resume_matching_node)
workflow.add_node("analyze_skill_gaps", skill_gap_analysis_node)
workflow.add_node("generate_interview_questions", interview_question_generation_node)
workflow.add_node("generate_summary", summary_generation_node)
workflow.add_node("rank_candidates", candidate_ranking_node)

# Link nodes with sequential edges
workflow.add_edge(START, "parse_resume")
workflow.add_edge("parse_resume", "generate_embeddings")
workflow.add_edge("generate_embeddings", "match_resume")
workflow.add_edge("match_resume", "analyze_skill_gaps")
workflow.add_edge("analyze_skill_gaps", "generate_interview_questions")
workflow.add_edge("generate_interview_questions", "generate_summary")
workflow.add_edge("generate_summary", "rank_candidates")
workflow.add_edge("rank_candidates", END)

# Compile graph
resume_screening_graph = workflow.compile()
