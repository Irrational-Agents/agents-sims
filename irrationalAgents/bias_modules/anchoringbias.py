# anchoring_bias.py
def anchoring_bias_module(personality, emotion, conversation_history, response_candidates, initial_scores, response_values, beta=0.5):
    """
    Adjust decision scores using Anchoring Bias, integrated with Prospect Theory and Fairness.
    
    Arguments:
    - personality: A dictionary of Big Five traits.
    - emotion: Current emotional state of the agent.
    - conversation_history: Context of prior interactions.
    - response_candidates: List of response options.
    - initial_scores: Initial scores for the responses.
    - response_values: Estimated values of the responses.
    - beta: Sensitivity to anchoring (default=0.5).
    
    Returns:
    - Updated scores list with Anchoring Bias applied.
    """
    # Step 1: Calculate anchor dynamically from response values (e.g., mean or median)
    anchor = sum(response_values) / len(response_values)

    # Step 2: Adjust scores based on Anchoring Bias
    adjusted_scores = []
    for i, response in enumerate(response_candidates):
        distance_from_anchor = abs(response_values[i] - anchor)
        anchoring_penalty = beta * distance_from_anchor
        adjusted_score = initial_scores[i] - anchoring_penalty  # Apply penalty based on distance from anchor
        adjusted_scores.append(adjusted_score)

    return adjusted_scores, anchor
