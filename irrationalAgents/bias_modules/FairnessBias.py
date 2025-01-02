import numpy as np
from prospect_theory import prospect_theory_module  # Import the existing module

# Define the Fairness Utility Function
def fairness_utility(agent_payoff, other_payoffs, alpha=0.8, beta=0.6):
    """
    Calculate fairness utility for an agent based on inequality aversion.
    """
    envy_term = sum([max(other - agent_payoff, 0) for other in other_payoffs]) * alpha
    guilt_term = sum([max(agent_payoff - other, 0) for other in other_payoffs]) * beta
    utility = agent_payoff - envy_term - guilt_term
    return utility

# Define the FairnessBias Decision Module
def fairness_bias_decision(conversation, agent_payoff, other_payoffs, emotion, personality):
    """
    Combine fairness utility with prospect theory for scoring decisions.
    """
    # Step 1: Use Prospect Theory to calculate scores
    candidate_responses, prospect_scores = prospect_theory_module(conversation, emotion, personality)

    # Step 2: Adjust scores based on fairness utility
    alpha, beta, _, _ = determine_parameters(emotion, personality)  # Use the same parameter function
    final_scores = []

    for i in range(len(candidate_responses)):
        fairness_score = fairness_utility(agent_payoff, other_payoffs, alpha, beta)
        final_score = fairness_score + prospect_scores[i]  # Combine fairness and prospect theory
        final_scores.append(final_score)

    return candidate_responses, final_scores

# Example Usage
if __name__ == "__main__":
    # Example conversation context
    conversation = "How should the resources be distributed fairly among a group?"

    # Example payoffs
    agent_payoff = 50
    other_payoffs = [30, 70, 45]

    # Emotion and personality
    emotion = "happiness"  # Example emotion
    personality = {"Openness": "high", "Neuroticism": "low"}  # Example personality traits

    # Call FairnessBias
    responses, scores = fairness_bias_decision(conversation, agent_payoff, other_payoffs, emotion, personality)
    print("Candidate Responses:", responses)
    print("Final Scores:", scores)
