import os
from crewai import Agent, Crew, Process, Task, LLM
from src.base.custom_crew_base import CustomCrewBase
from src.LLMs.open_ai import faster_4o_mini_model, creative_4o_mini_model

from dotenv import load_dotenv

load_dotenv()

class CopywhatsappCrew(CustomCrewBase):
    """Copywhatsapp crew"""

    def __init__(self):
        super().__init__(agents_group_pool=["copy-wpp"], tasks_group_pool=["copy-wpp"])

    def promptBuilder(self) -> Agent:
        return Agent(
            config=self.agents_config["promptBuilder"],
            verbose=True,
            cache=False,
            max_iter=1,
            llm=faster_4o_mini_model,
        )

    def variableSuggester(self) -> Agent:
        return Agent(
            config=self.agents_config["variableSuggester"],
            verbose=True,
            cache=False,
            max_iter=1,
            llm=faster_4o_mini_model,
        )

    def copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config["copywriter"],
            verbose=True,
            cache=False,
            max_iter=1,
            llm=faster_4o_mini_model,
        )

    def promptBuilder_task(self) -> Task:
        return Task(
            config=self.tasks_config["promptBuilder_task"],
            async_execution=True,
            agent=self.promptBuilder(),
        )

    def variableSuggester_task(self) -> Task:
        return Task(
            config=self.tasks_config["variableSuggester_task"],
            async_execution=True,
            agent=self.variableSuggester(),
        )

    def copywriter_task(self) -> Task:
        return Task(
            config=self.tasks_config["copywriter_task"],
            agent=self.copywriter(),
        )

    def crew(self) -> Crew:
        """Creates the Copywhatsapp crew"""
        return Crew(
            agents=[self.promptBuilder(), self.variableSuggester(), self.copywriter()],
            tasks=[
                self.promptBuilder_task(),
                self.variableSuggester_task(),
                self.copywriter_task(),
            ],
            process=Process.sequential,
            verbose=True,
        )
