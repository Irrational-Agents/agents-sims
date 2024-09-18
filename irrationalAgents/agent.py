import json

import logging

from irrationalAgents.memory_modules.long_term_memory import *
from irrationalAgents.memory_modules.short_term_memory import *
from irrationalAgents.common_method import *
from irrationalAgents.stimulus import *
from irrationalAgents.agents_modules.behavior.plan import *
from irrationalAgents.agents_modules.behavior.plan_evaluation import *
from irrationalAgents.agents_modules.behavior.action import *
from irrationalAgents.agents_modules.personality.cognition import *
from irrationalAgents.agents_modules.personality.emotion import *
from irrationalAgents.agents_modules.personality.personality import *

logger = logging.getLogger(__name__)
class Agent:
    def __init__(self, basic_info, memory_folder_path=False):
        self.basic_info = basic_info

        self.name = basic_info['name']


        long_memory_path = f"{memory_folder_path}/long_term"
        self.long_memory = LongTermMemory(long_memory_path)

        short_memory_path = f"{memory_folder_path}/short_term.json"
        self.short_memory = ShortTermMemory(short_memory_path)

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



    def move(self, agents_list, curr_time, event):
        
        #eventは後で修正する。(多分マップの方で取り扱いそう)testチャットよう。
        #[event] will be removed after connecting Unity
        events = []
        events.append(event)

        new_day = False
        if not self.short_memory.curr_datetime: 
            new_day = "First day"
        elif (self.short_memory.curr_datetime.strftime('%A %B %d')
            != self.short_memory.curr_datetime.strftime('%A %B %d')):
            new_day = "New day"
        self.short_memory.curr_datetime = curr_time
        self.short_memory.curr_time = self.short_memory.curr_datetime.strftime('%H:%M')
        self.short_memory.curr_date = self.short_memory.curr_datetime.strftime('%Y-%m-%d')
            
        stimulus = self.stimulus(events)

        if stimulus == "sys2":
            return
        elif stimulus == "sys1":
            plan_list = self.plan(new_day)
            best_plan = self.plan_evaluation(plan_list)
            self.action(best_plan)

        






