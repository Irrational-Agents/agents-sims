from prompt.llm_command_list import *

def calculate_probabilities_and_outcomes(conversation):
    candidate_responses, probabilities, outcomes = get_llm_responses_and_scores_and_outcome(conversation)

    total_prob = sum(probabilities)
    normalized_probabilities = [p / total_prob for p in probabilities]

    return candidate_responses, normalized_probabilities, outcomes


def determine_parameters(emotion, personality):
    # Default parameters
    alpha, beta, gamma, lambda_ = 0.8, 0.8, 0.9, 1.5

    # Adjust parameters based on emotion
    if emotion == "anger":
        alpha, beta, gamma, lambda_ = 0.9, 0.7, 0.7, 1.2
    elif emotion == "disgust":
        alpha, beta, gamma, lambda_ = 0.8, 0.6, 0.9, 2.0
    elif emotion == "fear":
        alpha, beta, gamma, lambda_ = 0.7, 0.5, 0.8, 1.8
    elif emotion == "happiness":
        alpha, beta, gamma, lambda_ = 1.0, 0.9, 1.0, 1.0
    elif emotion == "sadness":
        alpha, beta, gamma, lambda_ = 0.7, 0.6, 0.8, 1.5
    elif emotion == "surprise":
        alpha, beta, gamma, lambda_ = 0.8, 0.7, 0.6, 1.3
    elif emotion == "neutral":
        alpha, beta, gamma, lambda_ = 0.8, 0.8, 0.9, 1.5
    
    # Big Five
    personality_influence = {
        "Openness": {"high": 0.1, "neutral": 0.0, "low": -0.1},
        "Conscientiousness": {"high": 0.0, "neutral": 0.0, "low": 0.0},
        "Extraversion": {"high": 0.1, "neutral": 0.0, "low": -0.1},
        "Agreeableness": {"high": 0.0, "neutral": 0.0, "low": 0.0},
        "Neuroticism": {"high": -0.1, "neutral": 0.0, "low": 0.1},
    }

    for trait, level in personality.items():
        if trait == "Openness":
            alpha += personality_influence[trait][level]
            gamma += personality_influence[trait][level]
        elif trait == "Conscientiousness":
            beta += personality_influence[trait][level]
            lambda_ += personality_influence[trait][level]
        elif trait == "Extraversion":
            alpha += personality_influence[trait][level]
            gamma += personality_influence[trait][level]
            lambda_ -= 0.1 if level == "high" else (-0.1 if level == "low" else 0.0)
        elif trait == "Agreeableness":
            beta += personality_influence[trait][level]
            lambda_ += personality_influence[trait][level]
        elif trait == "Neuroticism":
            alpha += personality_influence[trait][level]
            beta += personality_influence[trait][level]
            lambda_ += 0.2 if level == "high" else (-0.2 if level == "low" else 0.0)

    return alpha, beta, gamma, lambda_

def prospect_theory_module(conversation, emotion, personality):
    # Step 1: Get candidate responses, normalized probabilities, and outcomes
    candidate_responses, probabilities, outcomes = calculate_probabilities_and_outcomes(conversation)

    # Step 2: Determine parameters
    alpha, beta, gamma, lambda_ = determine_parameters(emotion, personality)

    # Step 3: Calculate scores using Prospect Theory
    scores = []
    for i in range(len(candidate_responses)):
        if outcomes[i] >= 0:
            value = outcomes[i] ** alpha
        else:
            value = -lambda_ * ((-outcomes[i]) ** beta)

        weighted_prob = (probabilities[i] ** gamma) / (
            (probabilities[i] ** gamma + (1 - probabilities[i]) ** gamma) ** (1 / gamma)
        )

        score = value * weighted_prob
        scores.append(score)

    return candidate_responses, scores
