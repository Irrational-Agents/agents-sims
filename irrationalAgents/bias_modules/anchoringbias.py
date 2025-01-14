from prompt.llm_command_list import *
import random

def anchoring_bias(agent_profile, current_emotion, conversation_history, response_candidates, score_lists, beta=0.5):
    """
    Adjust scores based on Anchoring Bias, dynamically generating anchor value using LLM.
    """
    # Step 1: Use LLM to generate a dynamic anchor based on the conversation history
    anchor = generate_dynamic_anchor(conversation_history)  # Prompt to generate anchor
    
    # Step 2: Anchoring Bias Calculation (calculate score adjustments based on anchor)
    adjusted_scores = []
    for i, score in enumerate(score_lists):
        distance_from_anchor = abs(score - anchor)  # Calculate the distance from the anchor
        
        # Apply the anchoring bias penalty
        anchoring_penalty = beta * distance_from_anchor
        final_score = score - anchoring_penalty  # Adjust score based on the anchor
        
        adjusted_scores.append(final_score)
    
    return adjusted_scores
