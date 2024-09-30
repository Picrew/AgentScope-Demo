import time
from typing import Optional, Union, Sequence
import agentscope
from agentscope.agents import AgentBase, UserAgent
from agentscope.strategy import MixtureOfAgents
from agentscope.message import Msg

# 初始化 model config
model_configs = "../../config/multi_moa_qwen_model_config copy.json"
agentscope.init(model_configs=model_configs, project="Mixture of Agents Streaming")

# 初始化 MoA 模块
your_moa_module = MixtureOfAgents(
    main_model="my_qwen_chat1",
    reference_models=["my_qwen_chat1", "my_qwen_chat2"],
    show_internal=False,
    rounds=1
)

class StreamingDialogAgentWithMoA(AgentBase):
    def __init__(self, name: str, moa_module: MixtureOfAgents, use_memory: bool=True) -> None:
        super().__init__(name=name, sys_prompt="", use_memory=use_memory)
        self.moa_module = moa_module

    def reply(self, x: Optional[Union[Msg, Sequence[Msg]]] = None) -> Msg:
        if self.memory and x:
            self.memory.add(x)
        
        response = self.moa_module(
            Msg("system", self.sys_prompt, role="system"),
            self.memory and self.memory.get_memory() or x
        )

        if hasattr(response, 'stream') and response.stream is not None:
            self.stream_output(response.stream)
        else:
            self.simulate_stream(response)

        msg = Msg(self.name, response, role="assistant")
        if self.memory:
            self.memory.add(msg)
        return msg

    def stream_output(self, stream):
        for chunk in stream:
            print(chunk, end='', flush=True)
        print()

    def simulate_stream(self, text: str):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.05)
        print()

# 设置聊天
if __name__ == "__main__":
    # 初始化两个代理
    dialog_agent = StreamingDialogAgentWithMoA(name="Assistant", moa_module=your_moa_module, use_memory=True)
    user_agent = UserAgent()

    # 开始用户和助手之间的对话
    msg = None
    while True:
        msg = user_agent(msg)
        if msg.content == "exit":
            break
        msg = dialog_agent(msg)

    print("对话结束")