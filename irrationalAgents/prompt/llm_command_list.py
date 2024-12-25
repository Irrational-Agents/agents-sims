import os
from openai import OpenAI
import json
import logging
from langsmith import traceable
from langsmith.wrappers import wrap_openai

logger = logging.getLogger(__name__)
api_key = os.getenv('OPENAI_API_KEY')
client = wrap_openai(OpenAI(api_key=api_key))

@traceable(name="generative_agent")
def generative_agent(user_content):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {
                "role": "user",
                "content": user_content
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error in generative_agent: {e}")
        return None

@traceable(name="generate_plan")
def generate_plan(agent_name, agent_profile, current_emotion, recent_events, current_time, current_date, daily_plan=None):
    with open('irrationalAgents/prompt/prompt_templates/plan_prompt.txt', 'r') as file:
        prompt_template1 = file.read()
    with open('irrationalAgents/prompt/prompt_templates/action_prompt.txt', 'r') as file:
        prompt_template2 = file.read()

    prompt1 = prompt_template1.format(
        agent_name=agent_name,
        agent_profile=agent_profile,
        current_emotion=current_emotion,
        recent_events=recent_events,
        current_time=current_time,
        current_date=current_date,
        daily_plan=daily_plan
    )
    
    system_content = "You are an AI assistant tasked with creating plans based on recent events and current context."
    response = generative_agent(system_content, prompt1)
    prompt2 = prompt_template2.format(
        description_list=json.loads(response)
    ) 
    response = generative_agent(system_content, prompt2)

    print(response)
    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in response.")
        return None

@traceable(name="generate_daily_plan")
def generate_daily_plan(agent_name, agent_profile, current_emotion, previous, current_date):
    with open('irrationalAgents/prompt/prompt_templates/daily_plan_prompt.txt', 'r') as file:
        prompt_template = file.read()

    prompt = prompt_template.format(
        agent_name=agent_name,
        agent_profile=agent_profile,
        current_emotion=current_emotion,
        previous=previous,
        current_date=current_date
    )

    response = generative_agent(prompt)
    logger.info(f"daily plan response: {response}")
    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in response.")
        return None

@traceable(name="generate_conversation")
def generate_conversation(agent_name, agent_profile, current_emotion, plan, recent_events, current_time, current_date):
    with open('irrationalAgents/prompt/prompt_templates/conv_prompt.txt', 'r') as file:
        prompt_template = file.read()
    # here may stuck in infinite conversation loop
    prompt = prompt_template.format(
        agent_name=agent_name,
        agent_profile=agent_profile,
        current_emotion=current_emotion,
        plan=plan,
        recent_events=recent_events,
        current_time=current_time,
        current_date=current_date
    )

    response = generative_agent(prompt)
    print(response)
    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in response.")
        return None

@traceable(name="generate_personality")
def generate_personality(traits):    
        with open('irrationalAgents/prompt/prompt_templates/personality_prompt.txt', 'r') as file:
            prompt_template = file.read()
        
        traits_str = json.dumps(traits, indent=2)
        
        prompt = prompt_template.format(traits=traits_str)
        
        personality_profile = generative_agent(prompt)
        print(personality_profile)
        return personality_profile

@traceable(name="generate_short_memory")
def generate_short_memory(agent_name, current_emotion, personality_traits, relationships, past_memories, perceived_events):
    with open('irrationalAgents/prompt/prompt_templates/short_memory_prompt.txt', 'r') as file:
            prompt_template = file.read()
    prompt = prompt_template.format(
        agent_name=agent_name,
        current_emotion=current_emotion, 
        personality_traits=personality_traits,
        relationships=relationships,
        past_short_term_memories=past_memories,
        perceived_events=perceived_events
    )

    response = generative_agent(prompt)
    print(response)
    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in response.")
        return None
    
@traceable(name="extract_keywords")
def extract_keywords_for_long_term_memory(description):
    with open('irrationalAgents/prompt/prompt_templates/extract_keywords_prompt.txt', 'r') as file:
            prompt = file.read()
    prompt = prompt.format(
        description=description
    )

    response = generative_agent(prompt)
    print(response)
    try:
        parsed_response = json.loads(response)
        if isinstance(parsed_response, list):
            return parsed_response
        else:
            # If it's not a list, return empty or handle accordingly
            return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in response.")
        return []
    
def generate_short_memory(agent_name, current_emotion, personality_traits, relationships, past_memories, perceived_events):
    with open('irrationalAgents/prompt/prompt_templates/short_memory_prompt.txt', 'r') as file:
            prompt_template = file.read()
    prompt = prompt_template.format(
        agent_name=agent_name,
        current_emotion=current_emotion, 
        personality_traits=personality_traits,
        relationships=relationships,
        past_short_term_memories=past_memories,
        perceived_events=perceived_events
    )

    response = generative_agent(prompt)
    print(response)
    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in response.")
        return None
    
def get_llm_responses_and_scores_and_outcome(conversation):
    with open('irrationalAgents/prompt/prompt_templates/scores_and_outcome_prompt.txt', 'r') as file:
            prompt_template = file.read()
    prompt = prompt_template.format(conversation=conversation)

    for _ in 3:
        try:
            response = generative_agent(prompt)
            parsed_response = json.loads(response)
            
            # Validate structure and types
            if all(key in parsed_response for key in ["candidate_responses", "probabilities", "outcomes"]):
                candidate_responses = parsed_response["candidate_responses"]
                probabilities = parsed_response["probabilities"]
                outcomes = parsed_response["outcomes"]

                if isinstance(candidate_responses, list) and \
                   all(isinstance(p, (int, float)) for p in probabilities) and \
                   all(isinstance(o, (int, float)) for o in outcomes):
                    return candidate_responses, probabilities, outcomes
        except (json.JSONDecodeError, KeyError, TypeError):
            pass

    print("Error: Invalid JSON format in response.")
    return None
    
