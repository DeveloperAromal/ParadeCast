from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.agents import AgentAction, AgentFinish
import os
import json
from dotenv import load_dotenv

load_dotenv()

def do_collect_wind_info(input: str):
    return f"Wind data collected (placeholder) based on input: {input}"

def do_collect_weather_info(input: str):
    return f"Weather data collected (placeholder) based on input: {input}"

def do_collect_temperature_info(input: str):
    return f"Temperature data collected (placeholder) based on input: {input}"

def do_collect_environment_info(input: str):
    return f"Environment data collected (placeholder) based on input: {input}"

def agent_prompt(historic_dates, location_name, latitude, longitude, target_date):
    return f"Analyze the historical data for the dates {historic_dates} at {location_name} (Lat: {latitude}, Lon: {longitude}) and predict the most likely conditions for {target_date}. Use your tools to gather all required information."

class ToolOutputLogger(BaseCallbackHandler):
    def __init__(self):
        self.tool_outputs = []

    def on_tool_end(self, tool_output: str, **kwargs):
        self.tool_outputs.append(tool_output)

    def get_tool_outputs(self):
        return self.tool_outputs

class ReasoningCaptureCallback(BaseCallbackHandler):
    def __init__(self):
        self.logs = []

    def on_llm_new_token(self, token: str, **kwargs):
        self.logs.append(token)

    def on_agent_action(self, action: AgentAction, **kwargs):
        self.logs.append(
            f"\nAgent Action: Tool='{action.tool}', Input='{action.tool_input}', Log='{action.log}'"
        )

    def on_tool_end(self, output: str, **kwargs):
        self.logs.append(f"\nTool Result: {output}")

    def on_agent_finish(self, finish: AgentFinish, **kwargs):
        self.logs.append(
            f"\nAgent Final Answer: {finish.return_values.get('output', 'No final output')}"
        )

    def get_logs(self):
        return "".join(self.logs)


def main_agent(historic_dates, latitude, longitude, target_date):
    log_file = os.path.join("src/db/raw", "agent_full_log.txt")

    llm = ChatOpenAI(
        model="deepseek/deepseek-chat-v3.1:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    tools = [
        Tool(name="collect_wind_info", func=do_collect_wind_info, description="Collect historical wind data."),
        Tool(name="collect_weather_info", func=do_collect_weather_info, description="Collect historical general weather data."),
        Tool(name="collect_temperature_info", func=do_collect_temperature_info, description="Collect historical temperature data."),
        Tool(name="collect_environment_info", func=do_collect_environment_info, description="Collect environmental data like humidity and pressure."),
    ]

    reasoning_logger = ReasoningCaptureCallback()
    tool_logger = ToolOutputLogger()

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        callbacks=[reasoning_logger, tool_logger],
        handle_parsing_errors=True,
    )

    result = agent.run(agent_prompt(historic_dates, latitude, longitude, target_date))

    if isinstance(result, (dict, list)):
        result_str = json.dumps(result, indent=2)
    else:
        result_str = str(result)

    full_reasoning_log = reasoning_logger.get_logs()
    raw_tool_outputs = tool_logger.get_tool_outputs()

    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))

    with open(log_file, "a", encoding="utf-8") as f:
        f.write("=== AGENT LOGIC & INTERLEAVED TOOL RESULTS ===\n\n")
        f.write(full_reasoning_log)
        
        f.write("\n\n" + "="*80 + "\n\n")
        f.write("=== RAW TOOL OUTPUTS (Unprocessed for Debugging) ===\n\n")
        for output in raw_tool_outputs:
            f.write(output + "\n\n")
        
        f.write("\n\n" + "="*80 + "\n\n")
        f.write("=== FINAL AGENT RETURN VALUE ===\n\n")
        f.write(result_str)

        print(f"This is the content ===> {result_str}")
    return result_str