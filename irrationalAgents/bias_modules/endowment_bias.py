# endowment_bias.py
def endowment_bias_module(response_candidates, score_lists, ownership_status):
    """
    Adjust decision scores based on endowment bias, considering whether the agent owns the item.
    
    Arguments:
    - response_candidates: List of response options for the agent to choose from.
    - score_lists: Initial scores for each response option.
    - ownership_status: A list indicating whether the agent owns the item (1 = owns, 0 = does not own).
    
    Returns:
    - Updated scores list with Endowment Bias adjustments applied.
    """
    updated_scores = []
    for i, response in enumerate(response_candidates):
        # Apply endowment bias: if the agent owns the item, they value it more highly
        endowment_adjustment = score_lists[i] * (1 + ownership_status[i] * 0.2)  # 20% boost for owned items
        updated_scores.append(endowment_adjustment)
    
    return updated_scores
