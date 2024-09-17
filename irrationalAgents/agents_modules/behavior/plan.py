from datetime import datetime, timedelta
import math
from irrationalAgents.prompt.llm_command_list import *
from irrationalAgents.agents_modules.personality.emotion import *

def plan(agent, new_day):
    
    if new_day:
        _dayly_planning(agent, new_day)
    
    plan_list = create_plan(agent)
    return plan_list

def _dayly_planning(agent, new_day):
    # 起床時間から、1日の1時間ごとのスケジュールを組む
    # この関数の実装は現状のままです
    pass

def create_plan(agent):
    # GPTを使用してプランを生成
    return generate_plan(agent.name, agent.formed_profile, get_complex_mood(agent.short_memory.emotion_memory[-1]), agent.short_memory.recent_events, agent.short_memory.curr_time, agent.short_memory.curr_date)

