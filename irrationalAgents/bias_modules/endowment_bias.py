from prompt.llm_command_list import *

def endowment_bias(agent_profile, current_emotion, conversation_history, response_candidates, score_lists):
    """
    Adjust scores based on Endowment Bias using ownership status.
    """
    # Step 1: Generate ownership status using LLM command list
    num_candidates = len(response_candidates)
    ownership_status = generate_ownership_status(num_candidates)
    
    # Step 2: Apply the endowment effect: Items owned tend to get higher scores
    adjusted_scores = []
    for i, score in enumerate(score_lists):
        if ownership_status[i] == 1:  # If the item is owned, increase its score
            adjusted_score = score * 1.2  # Example: boost owned options
        else:
            adjusted_score = score  # No change for non-owned items
        adjusted_scores.append(adjusted_score)
    
    return adjusted_scores
