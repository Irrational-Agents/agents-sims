from parameter_tuner import determine_parameters
from value_function import compute_value
from probability_weighting import compute_weight
from prompt.llm_command_list import get_llm_responses_and_scores_and_outcome
from utils import *
"""
Get candidates of answers
"""
def generate_candidates_responses(conversation):

    candidate_responses, probabilities, outcomes = get_llm_responses_and_scores_and_outcome(conversation)
    total_prob = sum(probabilities)
    if total_prob == 0:
        normalized_probabilities = [0 for _ in probabilities]
    else:
        normalized_probabilities = [p / total_prob for p in probabilities]
    return candidate_responses, normalized_probabilities, outcomes

"""
*******************Bias Framework*********************
"""
def prospect_theory_evaluation(conversation, emotion, personality):
    # Step 1: Get candidate responses, normalized probabilities, and outcomes
    candidate_responses, probabilities, outcomes = generate_candidates_responses(conversation)

    # Step 2: Determine parameters (alpha, beta, gamma, lambda)
    alpha, beta, gamma, lambda_ = determine_parameters(emotion, personality)

    # Step 3: Calculate scores using Prospect Theory
    scores = []
    for i in range(len(candidate_responses)):
        # Value function
        value = compute_value(outcomes[i], alpha, beta, lambda_)
        # Probability weighting
        weighted_prob = compute_weight(probabilities[i], gamma)
        # Final prospect theory score
        score = value * weighted_prob
        scores.append(score)

    return candidate_responses, scores
