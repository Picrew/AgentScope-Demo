# auto_discussion.py
# -*- coding: utf-8 -*-
"""AgentScope Multi-Agent Group Conversation Demo"""

import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
from agentscope.msghub import msghub
from tools import load_txt, extract_scenario_and_participants

def main(query: str, max_rounds: int = 5):
    # Initialize AgentScope
    agentscope.init(
        model_configs="../../config/multi_qwen_model_config.json",
        project="Auto Discussion Demo",
    )

    # Get the discussion scenario and participant agents
    agent_builder_content = load_txt("agent_builder_instruct.txt").format(question=query)
    agent_builder = DialogAgent(
        name="agent_builder",
        sys_prompt="You are an AI assistant that helps organize group discussions by creating scenarios and defining participant roles. Please create 3 roles for this discussion.",
        model_config_name="my_qwen_chat1"
    )
    settings = agent_builder(Msg("user", agent_builder_content, role="user"))

    scenario_participants = extract_scenario_and_participants(settings.content)

    # Set the agents that participate in the discussion
    agents = []
    model_configs = ["my_qwen_chat1", "my_qwen_chat2", "my_qwen_chat3"]
    
    for i, (key, val) in enumerate(scenario_participants["Participants"].items()):
        agents.append(
            DialogAgent(
                name=key,
                sys_prompt=val,
                model_config_name=model_configs[i % 3],  
            )
        )

    # Begin discussion
    hint = Msg(
        name="Host",
        content=f"Scenario: {scenario_participants['Scenario']}\nQuestion: {query}",
        role="assistant",
    )

    with msghub(agents, announcement=hint):
        msg = Msg("user", f"Let's discuss to solve the question: {query}", role="user")
        for _ in range(max_rounds):
            for agent in agents:
                msg = agent(msg)
                print(f"{agent.name}: {msg.content}")
                import time
                time.sleep(0.5)

if __name__ == "__main__":
    question = ""
    main(question, max_rounds=3)