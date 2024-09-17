import os
from openai import OpenAI
import json

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def generative_agent(system_content, user_content, max_retries=3):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {
                "role": "system",
                "content": system_content
                },
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

def generate_plan(agent_name, agent_profile, current_emotion, recent_events, current_time, current_date):
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
        current_date=current_date
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


def generate_conversation(agent_name, agent_profile, current_emotion, plan, recent_events, current_time, current_date):
    with open('irrationalAgents/prompt/prompt_templates/conv_prompt.txt', 'r') as file:
        prompt_template = file.read()
    
    prompt = prompt_template.format(
        agent_name=agent_name,
        agent_profile=agent_profile,
        current_emotion=current_emotion,
        plan=plan,
        recent_events=recent_events,
        current_time=current_time,
        current_date=current_date
    )
    
    system_content = "You are an AI assistant tasked with generating brief, context-appropriate actions or conversations based on given plans and events."
    response = generative_agent(system_content, prompt)
    print(response)
    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in response.")
        return None

def generate_personality(traits):
        with open('irrationalAgents/prompt/prompt_templates/personality_prompt.txt', 'r') as file:
            prompt_template = file.read()
        
        traits_str = json.dumps(traits, indent=2)
        
        prompt = prompt_template.format(traits=traits_str)
        
        system_content = "You are an AI assistant specialized in creating concise and insightful personality profiles based on given personality traits."
        personality_profile = generative_agent(system_content, prompt)
        print(personality_profile)
        return personality_profile

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
    
    system_content = "You are an AI assistant tasked with updating an agent's short-term memory and emotional state based on perceived events and context."
    response = generative_agent(system_content, prompt)
    print(response)
    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in response.")
        return None