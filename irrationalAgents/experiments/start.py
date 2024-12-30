import json
from datetime import datetime
import os
import pandas as pd
print(os.getcwd())
from irrationalAgents.prompt.llm_command_list import generate_experiment_llm

class Agent:
    """simple agent for experiment"""
    def __init__(self, name, traits, emotional_profile):
        self.name = name
        self.traits = traits  # dict with O,C,E,A,N scores
        self.emotional_profile = emotional_profile
        
        self.memory_path = "storage/experiments"
        os.makedirs(self.memory_path, exist_ok=True)

        self.memory_file = os.path.join(self.memory_path, f"{name}_memory.json")


    def save_memory(self, conv):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        memory_entry = {
            timestamp: {
                **conv
            }
        }
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                memories = json.load(f)
        else:
            memories = {}

        memories.update(memory_entry)

        with open(self.memory_file, 'w') as f:
            json.dump(memories, f, indent=4)

    def get_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                memories = json.load(f)
                
                memory_items = [(k, v) for k, v in memories.items()]
                
                memory_items.sort(key=lambda x: x[1], reverse=True)
                
                # 取最近3条
                recent_memories = dict(memory_items[:5])
                
                return recent_memories
        else:
            return {}
    
    def alter_emotion_base_weights(self):
        """todo: 可以根据上一次的会话情绪进行调整"""
        return self.emotional_profile


def load_agents_from_personas():
    columns = ['Name', 'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism', 'Dominance_emotion']
    
    categorical_map = {
        'low': 0.3,
        'medium': 0.6,
        'high': 0.9
    }

    agents = []
    with open('storage/experiments/personas.csv', 'r') as f:
        next(f)
        for line in f:
            parts = line.strip().split(',')
            name = parts[0]
            
            traits = {
                'Openness': categorical_map.get(parts[1].lower(), parts[1]),
                'Conscientiousness': categorical_map.get(parts[2].lower(),  parts[2]),
                'Extraversion': categorical_map.get(parts[3].lower(), parts[3]),
                'Agreeableness': categorical_map.get(parts[4].lower(), parts[4]),
                'Neuroticism': categorical_map.get(parts[5].lower(), parts[5])
            }
            emotions = parts[6]
            
            agents.append(Agent(name, traits, emotions))
            
    return agents

def load_economic_questions():
    """todo: load from file"""
    pass

def main():
    """simple start for test"""
    agents = load_agents_from_personas()
    agent = agents[0]
    
    #https://uowmailedu-my.sharepoint.com/:w:/r/personal/ka481_uowmail_edu_au/_layouts/15/doc2.aspx?sourcedoc=%7BF4ADC3A6-0D9E-4D07-95B8-4C44C42DFD55%7D&file=Write%20the%20plan.docx&action=default&mobileredirect=true&wdOrigin=OFFICE-OFFICE-METAOS.FILEBROWSER.FILES-FOLDER
    #questions = load_economic_questions()
    print(f"test agent: {agent.name}: {agent.traits}")
    while True:
        question = input("Q:  ")
        response = generate_experiment_llm(\
            agent.name, agent.emotional_profile, agent.traits, agent.get_memory(), question)
        
        agent.save_memory(response)


if __name__ == "__main__":
    main()
