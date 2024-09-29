# -*- coding: utf-8 -*-
"""AgentScope Multi-Agent Group Conversation Demo"""

import re
from typing import Sequence
import agentscope
from agentscope.agents import UserAgent
from agentscope.message import Msg
from agentscope.msghub import msghub

# Group chat utils
def select_next_one(agents: Sequence, rnd: int) -> Sequence:
    """Select next agent."""
    return agents[rnd % len(agents)]

def filter_agents(string: str, agents: Sequence) -> Sequence:
    """Filter agents mentioned in the input string."""
    if len(agents) == 0:
        return []
    
    pattern = (
        r"@(" + "|".join(re.escape(agent.name) for agent in agents) + r")\b"
    )
    matches = re.findall(pattern, string)
    
    agent_dict = {agent.name: agent for agent in agents}
    ordered_agents = [
        agent_dict[name] for name in matches if name in agent_dict
    ]
    return ordered_agents

# Constants
DEFAULT_TOPIC = """
This is a chat room and you can speak freely and briefly.
"""

SYS_PROMPT = """
You can designate a member to reply to your message, you can use the @ symbol.
This means including the @ symbol in your message, followed by
that person's name, and leaving a space after the name.

All participants are: {agent_names}
"""

USER_TIME_TO_SPEAK = 100  # User's response timeout

def main() -> None:
    """Group chat main function."""
    # Initialize AgentScope
    npc_agents = agentscope.init(
        model_configs="../config/multi_qwen_model_config.json",
        agent_configs="../config/multi_qwen_agent_config.json",
        project="Conversation with Mentions",
    )

    user = UserAgent()
    agents = list(npc_agents) + [user]

    hint = Msg(
        name="Host",
        content=DEFAULT_TOPIC
        + SYS_PROMPT.format(
            agent_names=[agent.name for agent in agents],
        ),
        role="assistant",
    )

    rnd = 0
    speak_list = []
    with msghub(agents, announcement=hint):
        while True:
            x = user(timeout=USER_TIME_TO_SPEAK)
            if x.content == "exit":
                break

            speak_list += filter_agents(x.content, npc_agents)

            if len(speak_list) > 0:
                next_agent = speak_list.pop(0)
                x = next_agent()
            else:
                next_agent = select_next_one(npc_agents, rnd)
                x = next_agent()

            speak_list += filter_agents(x.content, npc_agents)
            rnd += 1

if __name__ == "__main__":
    main()