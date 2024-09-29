# AgentScope Demo
## Introduction
This README provides a concise overview of setting up and running a simple demo using the [AgentScope](https://github.com/modelscope/agentscope) framework. 

## News
* [2024/09/29] I have released **Sample example, Streaming output, Multi-agent discussions, Auto-multi-agent** at this repositories.


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

### Sample example
Please **run agent.ipynb**

### Streaming output
```bash
python run_agent_streaming.py
```

### Multi-agent discussions
```bash
python run_multi_agent_streaming.py
```
And use @ who.

### Auto-multi-agent
```bash
python auto_discussion.py
```

