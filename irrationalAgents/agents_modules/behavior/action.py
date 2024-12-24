from irrationalAgents.prompt.llm_command_list import *
from irrationalAgents.common_method import *
from irrationalAgents.agents_modules.personality.emotion import *

def action(agent, next_action):
    action_type = next_action['action']
    description = next_action['description']
    
    if action_type == "think":
        return handle_think(agent, description)
    elif action_type == "chat":
        return handle_chat(agent, description, agent.short_memory.recent_events)
    elif action_type == "interact":
        return handle_interact(agent, description)
    elif action_type == "move":
        return handle_move(agent, description)
    else:
        return handle_unknown_action(agent, action_type, description)

def handle_think(agent, description):
    new_entry = {
        "time": agent.short_memory.curr_date,
        "date": agent.short_memory.curr_date,
        "moccupying": 1,
        "description": f"{agent.name} thought about: {description}",
        "emotion": {
            "type": "contemplative",
            "intensity": 4
        }
    }
    
    agent.short_memory.add_short_memory(new_entry)
    print(new_entry)
    return f"Thought about: {description}"

def handle_chat(agent, description, recent_events_text):
    advance_time, advance_date = advance_time_by_15_minutes(agent.short_memory.curr_time, agent.short_memory.curr_date)
    
    conv = generate_conversation(agent.name, agent.formed_profile, get_complex_mood(agent.short_memory.emotion_memory[-1]), description, recent_events_text, advance_time, advance_date)

    
    new_entry = {
        "time": advance_time,
        "date": advance_date,
        "moccupying": 1,
        "description": f"{conv[0]} chatted with {conv[1]}: {conv[2]}",
        "emotion": agent.short_memory.emotion_memory[-1]
    }
    print(get_complex_mood(agent.short_memory.emotion_memory[-1]))
    agent.short_memory.add_short_memory([new_entry])
    return conv

def handle_interact(agent, description):
    '''
    new_entry = {
        "time": agent.short_memory.curr_date,
        "date": agent.short_memory.curr_date,
        "moccupying": 1,
        "description": f"{agent.name} interacted with {description}",
        "emotion": {
            "type": "engaged",
            "intensity": 5
        }
    }
    '''
    new_entry = {
        "time": agent.short_memory.curr_date,
        "date": agent.short_memory.curr_date,
        "moccupying": 1,
        "description": f"{agent.name} interacted with other: {description}",
        "emotion": {
            "type": "engaged",
            "intensity": 5
        }
    }
    
    agent.short_memory.add_short_memory([new_entry])
    print(new_entry)
    return f"Interacted with {description}"

def handle_move(agent, description):
    '''
    new_entry = {
        "time": agent.short_memory.curr_date,
        "date": agent.short_memory.curr_date,
        "moccupying": 1,
        "description": f"{agent.name} moved to {description}",
        "emotion": {
            "type": "neutral",
            "intensity": 3
        }
    }
    '''
    new_entry = {
        "time": agent.short_memory.curr_date,
        "date": agent.short_memory.curr_date,
        "moccupying": 1,
        "description": f"{agent.name} moved: {description}",
        "emotion": {
            "type": "neutral",
            "intensity": 3
        }
    }
    
    agent.short_memory.add_short_memory([new_entry])
    print(new_entry)
    return f"Moved to {description}"

def handle_unknown_action(agent, action_type, description):
    new_entry = {
        "time": agent.short_memory.curr_date,
        "date": agent.short_memory.curr_date,
        "moccupying": 1,
        "description": f"{agent.name} did: {action_type} - {description}",
        "emotion": {
            "type": "confused",
            "intensity": 4
        }
    }
    
    agent.short_memory.add_short_memory([new_entry])
    print(new_entry)
    return f"Attempted unknown action: {action_type} - {description}"

