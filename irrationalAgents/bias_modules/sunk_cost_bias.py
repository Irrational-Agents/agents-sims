from prompt.llm_command_list import *

def sunk_cost_bias(agent_profile, current_emotion, conversation_history, response_candidates, score_lists):
    """
    Adjust scores based on Sunk Cost Bias using previous investments.
    """
    # Step 1: Generate previous investments using LLM command list
    num_candidates = len(response_candidates)
    previous_investments = generate_previous_investments(num_candidates)
    
    # Step 2: Apply sunk cost bias: higher investments should lead to higher scores
    adjusted_scores = []
    for i, score in enumerate(score_lists):
        investment = previous_investments[i]
        adjusted_score = score + (investment * 0.1)  # Example: larger investment increases score
        adjusted_scores.append(adjusted_score)
    
    return adjusted_scores
