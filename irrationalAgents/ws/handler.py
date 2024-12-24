from irrationalAgents.agent import gen_agent_by_name
from irrationalAgents.agents_modules.behavior.action import handle_chat

AGENT_DICT = {
    "Zhang San": 1
}


def handle_active(agents):
    for agent_name in agents:
        agent = gen_agent_by_name(agent_name)
        AGENT_DICT[agent_name] = agent


def handle_chat(agent, content):
    agent = AGENT_DICT[agent]
    return handle_chat(agent, content, agent.short_memory.recent_events)