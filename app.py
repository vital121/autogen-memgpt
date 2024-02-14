# Import necessary modules
import autogen
from autogen import AssistantAgent, UserProxyAgent
import memgpt.agent as agent
import memgpt.autogen.interface as autogen_interface
import memgpt.autogen.memgpt_agent as memgpt_autogen
import memgpt.constants as constants
import memgpt.humans.humans as humans
import memgpt.personas.personas as personas
import memgpt.presets as presets
import memgpt.system as system
import memgpt.utils as utils
from memgpt.persistence_manager import InMemoryStateManager
import openai

# Set up OpenAI API key
openai.api_key = 'API KEY HERE'

# Define model configurations
config_list = [{
    'model': 'gpt-4'
}]
llm_config = {"config_list": config_list, "seed": 42}

# Define user proxy
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "output"},
    llm_config=llm_config,
    system_message="""
   Reply TERMINATE if the task is completed, reply CONTINUE otherwise, or the reason why the task is not solved yet."""
)

# Set up Autogen interface
interface = autogen_interface.AutoGenInterface()

# Set up In-Memory state manager
persistence_manager = InMemoryStateManager()

# Define personalities
persona = "I'm a create writer."
human = "I am an Editor."

# Set up MemGPT agent
memgpt_agent = presets.use_preset(presets.DEFAULT_PRESET,None, 'gpt-4', persona, human, interface, persistence_manager)

# Define the Creative Writer into Autogen
writer = memgpt_autogen.MemGPTAgent(
    name="MemGPT_Writer",
    agent=memgpt_agent,
)

user_proxy.initiate_chat(
    writer,
    message="Create a 200 word story for kids that like racing."
)
