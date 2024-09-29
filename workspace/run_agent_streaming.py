import time
from typing import Optional, Union, Sequence
import agentscope
from agentscope.agents import AgentBase, UserAgent
from agentscope.message import Msg

# Init AgentScope
agentscope.init(
    model_configs="../config/qwen_model_config.json",
    project="A basic conversation demo",
    save_api_invoke=True,
)

class StreamingAgent(AgentBase):

    def __init__(
        self,
        name: str,
        sys_prompt: str,
        model_config_name: str,
    ) -> None:
        super().__init__(
            name=name,
            sys_prompt=sys_prompt,
            model_config_name=model_config_name,
        )
        self.memory.add(Msg(self.name, self.sys_prompt, "system"))

    def reply(self, x: Optional[Union[Msg, Sequence[Msg]]] = None) -> Msg:
        self.memory.add(x)
        prompt = self.model.format(self.memory.get_memory())
        res = self.model(prompt)

        if hasattr(res, 'stream') and res.stream is not None:
            self.speak(res.stream)
        else:
            self.simulate_stream(res.text)

        msg_returned = Msg(self.name, res.text, "assistant")
        self.memory.add(msg_returned)
        return msg_returned

    def simulate_stream(self, text: str):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.05) 
        print() 

agent = StreamingAgent(
    "assistant",
    sys_prompt="You're a helpful assistant",
    model_config_name="my_qwen_chat",
)

user = UserAgent("user")

msg = None
while True:
    msg = user(msg)
    if msg.content == "exit":
        break
    msg = agent(msg)

print("对话结束")