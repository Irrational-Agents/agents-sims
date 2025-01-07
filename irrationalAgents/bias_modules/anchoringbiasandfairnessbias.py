from prospect_theory import prospect_theory_value, probability_weighting  # Assuming these are in your module

# Anchoring Bias module (as in your previous example)
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

# Fairness Bias module (as in your code)
def fairness_utility(agent_payoff, other_payoffs, alpha=0.8, beta=0.6):
    """
    Calculate fairness utility for an agent based on inequality aversion.
    """
    envy_term = sum([max(other - agent_payoff, 0) for other in other_payoffs]) * alpha
    guilt_term = sum([max(agent_payoff - other, 0) for other in other_payoffs]) * beta
    utility = agent_payoff - envy_term - guilt_term
    return utility

def fairness_bias_module(personality, emotion, conversation_history, response_candidates, score_lists):
    """
    Adjust scores based on Fairness Bias, considering personality, emotion, and Prospect Theory.
    Arguments:
    - personality: A dictionary of Big Five traits.
    - emotion: Current emotional state of the agent.
    - conversation_history: The context of prior interactions.
    - response_candidates: List of response options for the agent to choose from.
    - score_lists: Initial scores for each response option.
    Returns:
    - Updated scores list with Fairness Bias adjustments applied.
    """
    # Step 1: Determine Prospect Theory parameters based on personality and emotion
    alpha, beta, gamma, lambda_ = determine_parameters(emotion, personality)
    
    # Step 2: Process each response candidate
    updated_scores = []
    for i, response in enumerate(response_candidates):
        agent_payoff = score_lists[i]  # Agent's payoff is the score after anchoring bias adjustment
        other_payoffs = [10, 20, 15]  # Static or context-driven payoffs
        
        # Fairness utility adjustment
        fairness_score = fairness_utility(agent_payoff, other_payoffs, alpha, beta)
        
        # Prospect theory adjustment (value and probability weighting)
        value = prospect_theory_value(score_lists[i], alpha, beta, lambda_)
        probability = probability_weighting(0.8, gamma)  # Example probability, can be dynamic
        
        # Final score combines fairness and prospect theory
        final_score = fairness_score + value * probability
        updated_scores.append(final_score)

    return updated_scores

# Example Usage
if __name__ == "__main__":
    # Agent's personality and emotion
    personality = {"Openness": "high", "Conscientiousness": "neutral", "Neuroticism": "low"}
    emotion = "happiness"
    
    # Conversation history (can be structured or simple context)
    conversation_history = "What would you like to do today?"
    
    # Response candidates and their initial scores
    response_candidates = ["Go for a walk", "Watch a movie", "Read a book"]
    score_lists = [50, 60, 55]  # Initial scores for each response
    
    # Apply Anchoring Bias first
    response_values = [40, 55, 70]  # Example values for each response
    adjusted_scores, anchor = anchoring_bias_module(personality, emotion, conversation_history, response_candidates, score_lists, response_values, beta=0.8)
    
    # Apply Fairness Bias on the adjusted scores
    final_scores = fairness_bias_module(personality, emotion, conversation_history, response_candidates, adjusted_scores)
    
    # Select the best response based on the final adjusted scores
    best_response_index = final_scores.index(max(final_scores))
    best_response = response_candidates[best_response_index]
    
    print("Anchor Value:", anchor)
    print("Final Adjusted Scores:", final_scores)
    print("Selected Response:", best_response)
