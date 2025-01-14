from prompt.llm_command_list import get_llm_responses_and_scores_and_outcome

def anchoring_bias_module(personality, emotion, conversation_history, response_candidates, score_lists):
    """
    Adjust scores based on Anchoring Bias, considering personality, emotion, and Prospect Theory.
    """
    # Step 1: Fetch responses, probabilities, and outcomes dynamically
    candidate_responses, probabilities, outcomes = get_llm_responses_and_scores_and_outcome(conversation_history)

    # Step 2: Set fallback for outcomes if necessary
    other_payoffs = outcomes if outcomes else [10, 20, 15]

    # Step 3: Determine parameters based on personality and emotion
    alpha, beta, gamma, lambda_ = determine_parameters(emotion, personality)

    # Step 4: Get the first response (anchor) and adjust other responses based on it
    anchor_value = score_lists[0]  # Assume the first response is the anchor
    updated_scores = []

    for i, response in enumerate(response_candidates):
        agent_payoff = score_lists[i]  # Agent's payoff is the initial score

        # Anchoring utility adjustment
        anchor_score = anchor_utility(agent_payoff, anchor_value)

        # Prospect theory adjustment
        value = prospect_theory_value(score_lists[i], alpha, beta, lambda_)
        probability = probability_weighting(probabilities[i] if probabilities else 0.8, gamma)

        # Final score combines anchoring and prospect theory
        final_score = anchor_score + value * probability
        updated_scores.append(final_score)

    return updated_scores


def anchor_utility(agent_payoff, anchor_value):
    """
    Adjust score based on the anchoring effect. The closer the agent's payoff is to the anchor, 
    the higher the score.
    """
    return abs(agent_payoff - anchor_value)  # Example: smaller difference means higher score
