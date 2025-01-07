# sunk_cost_bias.py
def sunk_cost_bias_module(response_candidates, score_lists, previous_investment):
    """
    Adjust decision scores based on the sunk cost fallacy, considering previous investments.
    
    Arguments:
    - response_candidates: List of response options for the agent to choose from.
    - score_lists: Initial scores for each response option.
    - previous_investment: A list of previous investments in the options (e.g., time, money).
    
    Returns:
    - Updated scores list with Sunk Cost Bias adjustments applied.
    """
    updated_scores = []
    for i, response in enumerate(response_candidates):
        # Apply sunk cost bias: the more investment, the higher the score
        sunk_cost_adjustment = score_lists[i] + previous_investment[i] * 0.1  # 10% increase for previous investment
        updated_scores.append(sunk_cost_adjustment)
    
    return updated_scores
