from prompt.llm_command_list import *

def risk_preference_bias(agent_profile, current_emotion, conversation_history, response_candidates, score_lists):
    """
    Adjust scores based on Risk Preference Bias using risk aversion value.
    """
    # Step 1: Generate the risk aversion value dynamically using LLM command list
    risk_aversion_value = generate_risk_aversion()
    
    # Step 2: Apply risk aversion to adjust scores
    adjusted_scores = []
    for i, score in enumerate(score_lists):
        # Higher risk aversion means lower scores for riskier options
        adjusted_score = score * (1 - risk_aversion_value * 0.5)  # Example adjustment
        adjusted_scores.append(adjusted_score)
    
    return adjusted_scores
