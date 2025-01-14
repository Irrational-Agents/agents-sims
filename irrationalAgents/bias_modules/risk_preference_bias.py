from prompt.llm_command_list import get_llm_responses_and_scores_and_outcome

def risk_preference_bias_module(personality, emotion, conversation_history, response_candidates, score_lists):
    """
    Adjust scores based on Risk Preference Bias, considering personality, emotion, and Prospect Theory.
    """
    # Step 1: Fetch responses, probabilities, and outcomes dynamically
    candidate_responses, probabilities, outcomes = get_llm_responses_and_scores_and_outcome(conversation_history)

    # Step 2: Set fallback for outcomes if necessary
    other_payoffs = outcomes if outcomes else [10, 20, 15]

    # Step 3: Determine parameters based on personality and emotion
    alpha, beta, gamma, lambda_ = determine_parameters(emotion, personality)

    # Step 4: Adjust based on risk preference (Risk Averse vs. Risk Seeking)
    updated_scores = []
    for i, response in enumerate(response_candidates):
        agent_payoff = score_lists[i]  # Agent's payoff is the initial score

        # Risk preference adjustment
        risk_score = risk_preference_utility(agent_payoff)

        # Prospect theory adjustment
        value = prospect_theory_value(score_lists[i], alpha, beta, lambda_)
        probability = probability_weighting(probabilities[i] if probabilities else 0.8, gamma)

        # Final score combines risk preference and prospect theory
        final_score = risk_score + value * probability
        updated_scores.append(final_score)

    return updated_scores


def risk_preference_utility(agent_payoff):
    """
    Adjust score based on the agent's risk preference. Risk-seeking behaviors are encouraged if payoff 
    is higher, risk-averse if lower.
    """
    return agent_payoff * 0.8  # Example: Risk-averse behavior scales down the score
