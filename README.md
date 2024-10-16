# AgentScope Demo
## Introduction
This README provides a concise overview of setting up and running a simple demo using the [AgentScope](https://github.com/modelscope/agentscope) framework. 

## News
* [2024/09/29] I have released **Sample example, Streaming output, Multi-agent discussions, Auto-multi-agent** at the floder ``workspace``.
* [2024/09/30] I have released **MOA-agent** at the floder ``workspace/moa_agent``.
* [2024/10/13] I have released a Gomoku Game using **Gomoku_agent** at the floder ``workspace/gomoku_agent``.

## Prerequisites
* Python version: 3.9 or higher
* Clone the repository:
```bash
git clone -b v0.1.0 https://github.com/modelscope/agentscope.git
cd agentscope
```
* Install the package:
```bash
pip install agentscope
# or
pip install -e .
```

## Quick Start

```bash
git clone https://github.com/Picrew/AgentScope-Demo.git
```

### Sample example
Please **run agent.ipynb**

### Streaming output
```bash
cd AgentScope-Demo
python run_agent_streaming.py
```

### Multi-agent discussions
```bash
python run_multi_agent_streaming.py
```
And use @ who.

### Auto-multi-agent
```bash
cd auto_multi_agent
python auto_discussion.py
```

### Moa_agent
```bash
cd moa_agent
python run_moa_agent_streaming.py 
# or 
python run_moa_agent.py
```

### Gomoku_agent
```bash
cd gomoku_agent
python run_game.py
```

#### :game_die: This is a sample game begin 

<p align="center">
  <img src="./assets/gomoku_agent_output.jpg" width="80%">
</p>

#### :trophy: This is a game over  

<p align="center">
  <img src="./assets/gomoku_agent_win.jpg" width="80%">
</p>