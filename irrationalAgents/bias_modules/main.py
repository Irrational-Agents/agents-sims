# main.py
from anchoring_bias import anchoring_bias_module
from fairness_bias import fairness_bias_module
from risk_preference_bias import risk_preference_bias_module
from endowment_bias import endowment_bias_module
from sunk_cost_bias import sunk_cost_bias_module

# Assuming the `determine_parameters`, `prospect_theory_value`, and `probability_weighting` functions are defined elsewhere

if __name__ == "__main__":
    # Agent's personality and emotion
    personality = {"Openness": "high", "Conscientiousness": "neutral", "Neuroticism": "low"}
    emotion = "happiness"
    
    # Conversation history (can be structured or simple context)
    conversation_history = "What would you like to do today?"
    
    # Response candidates and their initial scores
    response_candidates = ["Go for a walk", "Watch a movie", "Read a book"]
    score_lists = [50, 60, 55]  # Initial scores for each response
    
    # Apply Anchoring Bias first
    response_values = [40, 55, 70]  # Example values for each response
    adjusted_scores, anchor = anchoring_bias_module(personality, emotion, conversation_history, response_candidates, score_lists, response_values, beta=0.8)
    
    # Apply Fairness Bias on the adjusted scores
    fairness_scores = fairness_bias_module(personality, emotion, conversation_history, response_candidates, adjusted_scores)
    
    # Apply Risk Preference Bias on the fairness-adjusted scores
    risk_aversion = 0.7  # Example risk aversion value
    risk_scores = risk_preference_bias_module(personality, response_candidates, fairness_scores, risk_aversion)
    
    # Apply Endowment Bias on the risk-adjusted scores
    ownership_status = [1, 0, 0]  # Assume agent owns the first option
    endowment_scores = endowment_bias_module(response_candidates, risk_scores, ownership_status)
    
    # Apply Sunk Cost Bias on the endowment-adjusted scores
    previous_investment = [10, 20, 15]  # Example previous investments in options
    final_scores = sunk_cost_bias_module(response_candidates, endowment_scores, previous_investment)
    
    # Select the best response based on the final adjusted scores
    best_response_index = final_scores.index(max(final_scores))
    best_response = response_candidates[best_response_index]
    
    print("Final Adjusted Scores:", final_scores)
    print("Selected Response:", best_response)
