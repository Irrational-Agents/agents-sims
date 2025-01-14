from llm_command_list import generate_fairness_parameters, generate_other_payoffs
import random

def fairness_bias(agent_profile, current_emotion, conversation_history, response_candidates, score_lists):
    """
    Adjust scores based on Fairness Bias, considering personality, emotion, and fairness utility.
    """
    # Step 1: Use LLM to generate fairness parameters (alpha, beta) dynamically based on profile and emotion
    fairness_params = generate_fairness_parameters(agent_profile, current_emotion)  # Prompt to generate alpha, beta
    other_payoffs = generate_other_payoffs(conversation_history, len(response_candidates))  # Prompt to generate other payoffs

    # Extract alpha and beta values from the generated parameters
    alpha = fairness_params['alpha']
    beta = fairness_params['beta']
    
    # Step 2: Fairness Utility Calculation (can be customized for each agent's payoff)
    adjusted_scores = []
    for i, score in enumerate(score_lists):
        agent_payoff = score
        fairness_score = fairness_utility(agent_payoff, other_payoffs, alpha, beta)
        adjusted_scores.append(fairness_score)
    
    return adjusted_scores
