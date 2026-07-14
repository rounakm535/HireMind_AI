import logging
from typing import Literal
from app.ai.graph.state import ScreenResumeState

logger = logging.getLogger(__name__)

def route_after_node(state: ScreenResumeState) -> Literal["continue", "retry", "error_end"]:
    """Determine the next step in the workflow based on the presence of errors and retry limits."""
    errors = state.get("errors")
    
    if not errors:
        return "continue"
        
    retry_count = state.get("retry_count", 0)
    if retry_count < 3:
        logger.warning(f"Error detected in graph execution: {errors[-1]}. Retrying (Attempt {retry_count + 1}/3)...")
        return "retry"
        
    logger.error(f"Max retries exceeded. Error terminating graph pipeline: {errors[-1]}")
    return "error_end"
