# tools.py
# -*- coding: utf-8 -*-
"""some utils of agent_builder example"""
import re

def load_txt(instruction_file: str) -> str:
    """
    load .txt file
    Arguments:
        instruction_file: str type, which is the .txt file path
    Returns:
        instruction: str type, which is the str in the instruction_file
    """
    with open(instruction_file, "r", encoding="utf-8") as f:
        instruction = f.read()
    return instruction

def extract_scenario_and_participants(content: str) -> dict:
    """
    extract the scenario and participants from agent builder's response
    Arguments:
        content: the agent builders response
    Returns:
        result: dict
    """
    result = {}
    # 定义正则表达式
    scenario_pattern = r"#场景#:(.*)"
    participants_pattern = r"\*(.*?):(.*)"

    # 查找并提取场景信息
    scenario_match = re.search(scenario_pattern, content)
    if scenario_match:
        result["Scenario"] = scenario_match.group(1).strip()

    # 查找并提取参与者信息
    participants_dict = {}
    participants_matches = re.findall(participants_pattern, content)
    for match in participants_matches:
        participants_dict[match[0].strip()] = match[1].strip()
    
    result["Participants"] = participants_dict

    return result