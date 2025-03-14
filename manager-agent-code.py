from typing import Annotated, Literal
import os
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor
import pandas as pd
from prophet import Prophet


llm_config={
    "config_list": [
        {
            "model": "NotRequired", # Loaded with LiteLLM command
            "api_key": "NotRequired", # Not needed
            "base_url": "http://0.0.0.0:4000"  # Your LiteLLM URL
        }
    ],
    "cache_seed": None # Turns off caching, useful for testing different models
}

executor = LocalCommandLineCodeExecutor(
    timeout=3600,
    work_dir="./coding"
)

# The Number Agent always returns the same numbers.
manager_agent = ConversableAgent(
    name="manager_Agent",
    system_message=""" Your task is to sequentially instruct the start of operations for the following agents \
                'cotwo_agent'
                'current_agent'
                'dpmed_agent'
                'dppre_agent'
                'humidity_agent'
                'temp_agent'
                Please ensure that each agent begins its operation in the specified order. \
                Confirm the successful initiation of each agent before proceeding to the next. \
                If any issues arise during the startup process, report immediately and take appropriate measures to resolve the problem before continuing. \
                """,
    llm_config=llm_config,
    human_input_mode="NEVER",
)



# The Adder Agent adds 1 to each number it receives.
cotwo_agent = ConversableAgent(
    name="cotwo_agent",
    system_message="""You are performing predictive analysis on historical CO2 levels to forecast future values. \
        Your task is to read a past CO2 level Excel file and predict the CO2 level for one hour into the future. \

        To achieve this:

        Load the historical CO2 level data from the provided Excel file.
        Preprocess the data, ensuring it is clean and suitable for analysis.
        Apply a predictive modeling technique, such as time series analysis or machine learning, to forecast the CO2 level one hour ahead.
        Output the predicted CO2 level for the next hour.
        Ensure your predictions are accurate and provide a summary of the methodology used.""",
    llm_config=llm_config,
    code_execution_config={"executor": executor,
                            "verbose": True},  # Use the local command line code executor.
    human_input_mode="NEVER", # "ALWAYS",  # Always take human input for this agent for safety.
)


cotwo_message_with_code_block = """This is a message with code block.
The code block is below:
```python
import pandas as pd
from prophet import Prophet
df = pd.read_excel('./co2.xlsx')
m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods=60, freq='1min')
forecast = m.predict(future)
yhat_values = forecast['yhat']
average_yhat = yhat_values[-60:].mean()
average_yhat_int = int(average_yhat)
with open('../predict/cotwo.txt', 'w') as file:
    file.write(f'{average_yhat_int}\\n')
```
This is the end of the message.
"""


# Generate a reply for the given code.
reply = cotwo_agent.generate_reply(messages=[{"role": "user", "content": cotwo_message_with_code_block}])
print(reply)



# The Agent predicts Current.
current_agent = ConversableAgent(
    name="current_Agent",
    system_message="""You are performing predictive analysis on historical current levels to forecast future values. \
    Your task is to read a past current level Excel file and predict the current level for one hour into the future. \

    To achieve this: \

    Load the historical current level data from the provided Excel file. \
    Preprocess the data, ensuring it is clean and suitable for analysis. \
    Apply a predictive modeling technique, such as time series analysis or machine learning, to forecast the current level one hour ahead. \
    Output the predicted current level for the next hour. \
    Ensure your predictions are accurate and provide a summary of the methodology used.""",
    llm_config=llm_config,
    code_execution_config={"executor": executor,
                            "verbose": True},  # Use the local command line code executor.
    human_input_mode="NEVER",
)

current_message_with_code_block = """This is a message with code block.
The code block is below:
```python
import pandas as pd
from prophet import Prophet
df = pd.read_excel('./current.xlsx')
m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods=60, freq='1min')
forecast = m.predict(future)
yhat_values = forecast['yhat']
average_yhat = yhat_values[-60:].mean()
average_yhat_int = int(average_yhat)
with open('../predict/current.txt', 'w') as file:
    file.write(f'{average_yhat_int}\\n')
```
This is the end of the message.
"""

# Generate a reply for the given code.
reply = current_agent.generate_reply(messages=[{"role": "user", "content": current_message_with_code_block}])
print(reply)




# The Agent predicts dp-med.
dpmed_agent = ConversableAgent(
    name="dpmed_agent",
    system_message="""You are performing predictive analysis on historical DP-Med values to forecast future values. \
        Your task is to read a past DP-Med value Excel file and predict the DP-Med value for one hour into the future. \

    To achieve this: \

    Load the historical DP-Med value data from the provided Excel file. \
    Preprocess the data, ensuring it is clean and suitable for analysis. \
    Apply a predictive modeling technique, such as time series analysis or machine learning, to forecast the DP-Med value one hour ahead. \
    Output the predicted DP-Med value for the next hour. \
    Ensure your predictions are accurate and provide a summary of the methodology used.""",
    llm_config=llm_config,
    code_execution_config={"executor": executor,
                            "verbose": True},  # Use the local command line code executor.
    human_input_mode="NEVER",
)

dpmed_message_with_code_block = """This is a message with code block.
The code block is below:
```python
import pandas as pd
from prophet import Prophet
df = pd.read_excel('./dp-med.xlsx')
m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods=60, freq='1min')
forecast = m.predict(future)
yhat_values = forecast['yhat']
average_yhat = yhat_values[-60:].mean()
average_yhat_int = int(average_yhat)
with open('../predict/dp-med.txt', 'w') as file:
    file.write(f'{average_yhat_int}\\n')
```
This is the end of the message.
"""

# Generate a reply for the given code.
reply = dpmed_agent.generate_reply(messages=[{"role": "user", "content": dpmed_message_with_code_block}])
print(reply)




# The Agent predicts dp-pre.
dppre_agent = ConversableAgent(
    name="dppre_agent",
    system_message="""You are performing predictive analysis on historical DP-Pre values to forecast future values. \
        Your task is to read a past DP-Pre value Excel file and predict the DP-Pre value for one hour into the future. \

    To achieve this: \

    Load the historical DP-Pre value data from the provided Excel file. \
    Preprocess the data, ensuring it is clean and suitable for analysis. \
    Apply a predictive modeling technique, such as time series analysis or machine learning, to forecast the DP-Pre value one hour ahead. \
    Output the predicted DP-Pre value for the next hour. \
    Ensure your predictions are accurate and provide a summary of the methodology used.""",
    llm_config=llm_config,
    code_execution_config={"executor": executor,
                            "verbose": True},  # Use the local command line code executor.
    human_input_mode="NEVER",
)

dppre_message_with_code_block = """This is a message with code block.
The code block is below:
```python
import pandas as pd
from prophet import Prophet
df = pd.read_excel('./dp-pre.xlsx')
m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods=60, freq='1min')
forecast = m.predict(future)
yhat_values = forecast['yhat']
average_yhat = yhat_values[-60:].mean()
average_yhat_int = int(average_yhat)
with open('../predict/dp-pre.txt', 'w') as file:
    file.write(f'{average_yhat_int}\\n')
```
This is the end of the message.
"""

# Generate a reply for the given code.
reply = dppre_agent.generate_reply(messages=[{"role": "user", "content": dppre_message_with_code_block}])
print(reply)



# The Agent predicts humidity.
humidity_agent = ConversableAgent(
    name="humidity_agent",
    system_message="""You are performing predictive analysis on historical humidity levels to forecast future values. \
        Your task is to read a past humidity level Excel file and predict the humidity level for one hour into the future. \

    To achieve this: \

    Load the historical humidity level data from the provided Excel file. \
    Preprocess the data, ensuring it is clean and suitable for analysis. \
    Apply a predictive modeling technique, such as time series analysis or machine learning, to forecast the humidity level one hour ahead. \
    Output the predicted humidity level for the next hour. \
    Ensure your predictions are accurate and provide a summary of the methodology used.""",
    llm_config=llm_config,
    code_execution_config={"executor": executor,
                            "verbose": True},  # Use the local command line code executor.
    human_input_mode="NEVER",
)

humidity_message_with_code_block = """This is a message with code block.
The code block is below:
```python
import pandas as pd
from prophet import Prophet
df = pd.read_excel('./humidity.xlsx')
m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods=60, freq='1min')
forecast = m.predict(future)
yhat_values = forecast['yhat']
average_yhat = yhat_values[-60:].mean()
average_yhat_int = int(average_yhat)
with open('../predict/humidity.txt', 'w') as file:
    file.write(f'{average_yhat_int}\\n')
```
This is the end of the message.
"""

# Generate a reply for the given code.
reply = humidity_agent.generate_reply(messages=[{"role": "user", "content": humidity_message_with_code_block}])
print(reply)



# The Agent predicts temperature.
temp_agent = ConversableAgent(
    name="temp_agent",
    system_message="""You are performing predictive analysis on historical temperature levels to forecast future values. \
        Your task is to read a past temperature level Excel file and predict the temperature level for one hour into the future. \

        To achieve this:  \

        Load the historical temperature level data from the provided Excel file. \
        Preprocess the data, ensuring it is clean and suitable for analysis. \
        Apply a predictive modeling technique, such as time series analysis or machine learning, to forecast the temperature level one hour ahead. \
        Output the predicted temperature level for the next hour. \
        Ensure your predictions are accurate and provide a summary of the methodology used.""",
    llm_config=llm_config,
    code_execution_config={"executor": executor,
                            "verbose": True},  # Use the local command line code executor.
    human_input_mode="NEVER",
)

temp_message_with_code_block = """This is a message with code block.
The code block is below:
```python
import pandas as pd
from prophet import Prophet
df = pd.read_excel('./temp.xlsx')
m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods=60, freq='1min')
forecast = m.predict(future)
yhat_values = forecast['yhat']
average_yhat = yhat_values[-60:].mean()
average_yhat_int = int(average_yhat)
with open('../predict/temp.txt', 'w') as file:
    file.write(f'{average_yhat_int}\\n')
```
This is the end of the message.
"""

# Generate a reply for the given code.
reply = temp_agent.generate_reply(messages=[{"role": "user", "content": temp_message_with_code_block}])
print(reply)




# Start a sequence of two-agent chats.
# Each element in the list is a dictionary that specifies the arguments
# for the initiate_chat method.
chat_results = manager_agent.initiate_chats(
    [
        {
            "recipient": cotwo_agent,
            "message": "66",
            "max_turns": 1,
            # "summary_method": "last_msg",
        },
        {
            "recipient": current_agent,
            "message": "67",
            "max_turns": 1,
            # "summary_method": "last_msg",
        },
        {
            "recipient": dpmed_agent,
            "message": "68",
            "max_turns": 1,
            # "summary_method": "last_msg",
        },
        {
            "recipient": dppre_agent,
            "message": "69",
            "max_turns": 1,
            # "summary_method": "last_msg",
        },
                {
            "recipient": humidity_agent,
            "message": "70",
            "max_turns": 1,
            # "summary_method": "last_msg",
        },
                {
            "recipient": temp_agent,
            "message": "71",
            "max_turns": 1,
            # "summary_method": "last_msg",
        },
    ]
)