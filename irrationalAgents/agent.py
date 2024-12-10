import json


from memory_modules.long_term_memory import *
from memory_modules.short_term_memory import *
from common_method import *
from stimulus import *
from agents_modules.behavior.plan import *
from agents_modules.behavior.plan_evaluation import *
from agents_modules.behavior.action import *
from agents_modules.personality.cognition import *
from agents_modules.personality.emotion import *
from agents_modules.personality.personality import *

from logger_config import setup_logger

logger = setup_logger('Agent')

def gen_agent_by_name(name):
    # todo: load from meta.json
    root_dir = f"storage/sample_data/agents/{name}"
    if not os.path.exists(root_dir):
        logger.error(f"agent {name} not exists!")
        return None
    
    with open(os.path.join(root_dir, "basic_info.json"), 'r', encoding='utf-8') as f:
        basic_info = json.load(f)
    memory_folder_path = os.path.join(root_dir, "memory")
    return Agent(basic_info, memory_folder_path)

class Agent:
    def __init__(self, basic_info, memory_folder_path=False):
        
        self.basic_info = basic_info

        self.name = basic_info['name']


        long_memory_path = f"{memory_folder_path}/long_term"
        self.long_memory = LongTermMemory(long_memory_path)

        short_memory_path = f"{memory_folder_path}/short_term.json"
        self.short_memory = ShortTermMemory(short_memory_path)

        if basic_info.get('personality'):
            self.short_memory.personality_text = basic_info.get('personality')
        else:
            self.short_memory.personality_text = generate_personality(basic_info['personality_traits'])

        self.basic_profile = profile_to_narrative(basic_info) 
        self.formed_profile = self.basic_profile + self.short_memory.personality_text
        self.relationships = basic_info['social_relationships']
        self.short_memory.emotion_memory.append(self.short_memory.emotion)


    def stimulus(self, event):
        return stimulus(self, event)
    
    def plan(self, new_day):
        return plan(self, new_day)
    
    def plan_evaluation(self, plan_list):
        return plan_evaluation(self, plan_list)
    
    def action(self, best_plan):
        return action(self, best_plan)

    def emotion(self):
        return emotion(self)
    
    def cognition(self):
        return cognition(self)

    def growth(self):
        growth(self)



    def move(self, agents_list,curr_time, event):
        
        #eventは後で修正する。(多分マップの方で取り扱いそう)testチャットよう。
        #[event] will be removed after connecting Unity
        events = []
        events.append(event)

        new_day = False
        if not self.short_memory.curr_datetime: 
            new_day = "First day"
            self.short_memory.short_memory = []
        elif (self.short_memory.curr_datetime.strftime('%A %B %d')
            != self.short_memory.curr_datetime.strftime('%A %B %d')):
            new_day = "New day"
        self.short_memory.curr_datetime = curr_time
        self.short_memory.curr_time = self.short_memory.curr_datetime.strftime('%H:%M')
        self.short_memory.curr_date = self.short_memory.curr_datetime.strftime('%Y-%m-%d')

        if new_day == "New day":
            self.long_memory.update_all_freshness(self.short_memory.curr_datetime)
            
        stimulus = self.stimulus(events)

        if stimulus == "sys2":
            return
        elif stimulus == "sys1":
            plan_list = self.plan(new_day)
            best_plan = self.plan_evaluation(plan_list)
            self.short_memory.save(self.short_memory)
            #self.action(best_plan)

        






