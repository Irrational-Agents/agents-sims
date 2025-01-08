from parameter_tuner import determine_parameters
from value_function import compute_value
from probability_weighting import compute_weight

def fairness_utility(agent_payoff, other_payoffs, alpha=0.8, beta=0.6):
    """
    Calculate fairness utility for an agent based on inequality aversion.
    """
    envy_term = sum([max(other - agent_payoff, 0) for other in other_payoffs]) * alpha
    guilt_term = sum([max(agent_payoff - other, 0) for other in other_payoffs]) * beta
    utility = agent_payoff - envy_term - guilt_term
    return utility



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