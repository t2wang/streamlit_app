import streamlit as st
from langchain_groq import ChatGroq
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_tool_calling_agent
import requests

groqChat = ChatGroq(temperature=0.9, groq_api_key="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", model_name="llama-3.3-70b-versatile")
memory = ConversationBufferMemory()

class CityCurrentWeatherInput(BaseModel):
  city: str = Field(description="city")

class CityCurrentWeatherTool(BaseTool):
    name = "city_weather_current"
    description = "The tool provides an overview of the current weather of the city queried, including maximum and minimum temperature."
    args_schema: Type[BaseModel] = CityCurrentWeatherInput

    def _run(self, city: str) -> str:
        """Use the tool."""

        geo_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
        headers = {"Content-Type": "application/json"}
        
        try:
            geo_response = requests.get(geo_url, headers=headers)
            geo_data = geo_response.json()

            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]

            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m&daily=temperature_2m_max,temperature_2m_min&past_days=1&forecast_days=0"
            weather_response = requests.get(weather_url, headers=headers)
            return weather_response.text

        except Exception as e:
            return f"Error fetching weather data: {str(e)}"

current_weather_tool = CityCurrentWeatherTool()
tools = [current_weather_tool]
agent = create_tool_calling_agent(llm=groqChat, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Streamlit UI
st.title("XYZ Dealership Chatbot")
inquiry = st.text_input("Hi there! How can I help?")
if st.button("Submit"):
    if inquiry:
        response = agent_executor.invoke({"input": inquiry})
        st.write(response["output"])