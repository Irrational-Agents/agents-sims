from prompt.llm_command_list import get_llm_responses_and_scores_and_outcome

def sunk_cost_bias_module(personality, emotion, conversation_history, response_candidates, score_lists):
    """
    Adjust scores based on Sunk Cost Bias, considering personality, emotion, and Prospect Theory.
    """
    # Step 1: Fetch responses, probabilities, and outcomes dynamically
    candidate_responses, probabilities, outcomes = get_llm_responses_and_scores_and_outcome(conversation_history)

    # Step 2: Set fallback for outcomes if necessary
    other_payoffs = outcomes if outcomes else [10, 20, 15]

    # Step 3: Determine parameters based on personality and emotion
    alpha, beta, gamma, lambda_ = determine_parameters(emotion, personality)

    # Step 4: Adjust based on sunk cost effect (greater investment increases perceived value)
    updated_scores = []
    for i, response in enumerate(response_candidates):
        agent_payoff = score_lists[i]  # Agent's payoff is the initial score

        # Sunk cost bias adjustment (higher score for higher investment)
        sunk_cost_score = sunk_cost_utility(agent_payoff)

        # Prospect theory adjustment
        value = prospect_theory_value(score_lists[i], alpha, beta, lambda_)
        probability = probability_weighting(probabilities[i] if probabilities else 0.8, gamma)

        # Final score combines sunk cost bias and prospect theory
        final_score = sunk_cost_score + value * probability
        updated_scores.append(final_score)

    return updated_scores


def sunk_cost_utility(agent_payoff):
    """
    Adjust score based on sunk cost bias. Higher investments result in higher perceived value.
    """
    return agent_payoff * 1.5  # Example: Increase score for greater investment in an action
