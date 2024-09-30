import agentscope
from agentscope.agents import AgentBase, UserAgent
from agentscope.strategy import MixtureOfAgents
from agentscope.message import Msg

model_configs = "../../config/multi_moa_qwen_model_config copy.json"
agentscope.init(model_configs=model_configs, project="Mixture of Agents")

your_moa_module = MixtureOfAgents(
    main_model="my_qwen_chat1",
    reference_models=["my_qwen_chat1", "my_qwen_chat2"],
    show_internal=False,
    rounds=1
)

class DialogAgentWithMoA(AgentBase):
    def __init__(self, name: str, moa_module: MixtureOfAgents, use_memory: bool=True) -> None:
        super().__init__(name=name, sys_prompt="", use_memory=use_memory)
        self.moa_module = moa_module

    def reply(self, x: Msg=None) -> Msg:
        if self.memory and x:
            self.memory.add(x)
        response = self.moa_module(
            Msg("system", self.sys_prompt, role="system"),
            self.memory and self.memory.get_memory() or x
        )
        msg = Msg(self.name, response, role="assistant")
        self.speak(msg)
        if self.memory:
            self.memory.add(msg)
        return msg
    
if __name__ == "__main__":
    dialog_agent = DialogAgentWithMoA(name="Assistant", moa_module=your_moa_module, use_memory=True)
    user_agent = UserAgent()

    while True:
        q = user_agent(None)
        if q.content == "exit":
            break
        q = dialog_agent(q)