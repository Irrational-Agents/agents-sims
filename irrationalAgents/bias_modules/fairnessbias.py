from prospect_theory import prospect_theory_value, probability_weighting  # Assuming these are in your module

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
    Adjust scores based on FairnessBias, considering personality, emotion, and Prospect Theory.
    
    Arguments:
    - personality: A dictionary of Big Five traits (e.g., {"Openness": "high", "Neuroticism": "low"}).
    - emotion: Current emotional state of the agent (e.g., "happiness").
    - conversation_history: The context of prior interactions (e.g., a string or structured data).
    - response_candidates: A list of response options for the agent to choose from.
    - score_lists: Initial scores for each response option.

    Returns:
    - Updated scores list with FairnessBias adjustments applied.
    """
    # Step 1: Determine Prospect Theory parameters based on personality and emotion
    alpha, beta, gamma, lambda_ = determine_parameters(emotion, personality)

    # Step 2: Process each response candidate
    updated_scores = []
    for i, response in enumerate(response_candidates):
        # Extract relevant payoffs from conversation history (customize as per context)
        agent_payoff = score_lists[i]  # Use the initial score as the agent's payoff
        other_payoffs = [10, 20, 15]  # Example: Static or derived from conversation history
        
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

    # Call FairnessBias module
    updated_scores = fairness_bias_module(personality, emotion, conversation_history, response_candidates, score_lists)
    
    # Select the response with the highest score
    best_response_index = updated_scores.index(max(updated_scores))
    best_response = response_candidates[best_response_index]

    print("Updated Scores:", updated_scores)
    print("Selected Response:", best_response)
