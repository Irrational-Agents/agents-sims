def calculate_probabilities_and_outcomes(conversation):

    candidate_responses, probabilities, outcomes = get_llm_responses_and_scores_and_outcome(conversation)
    total_prob = sum(probabilities)
    if total_prob == 0:
        normalized_probabilities = [0 for _ in probabilities]
    else:
        normalized_probabilities = [p / total_prob for p in probabilities]
    return candidate_responses, normalized_probabilities, outcomes