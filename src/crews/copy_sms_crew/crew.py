import os
from crewai import Agent, Crew, Process, Task, LLM
from src.base.custom_crew_base import CustomCrewBase

from dotenv import load_dotenv

load_dotenv()

class CopySmsCrew(CustomCrewBase):
    """CopySms crew"""

    def __init__(self):
        super().__init__(agents_group_pool=["copy-sms"], tasks_group_pool=["copy-sms"])

    def promptBuilder(self) -> Agent:
        return Agent(
            config=self.agents_config["promptBuilder"],
            verbose=True,
            max_iter=1,
        )

    def variableSuggester(self) -> Agent:
        return Agent(
            config=self.agents_config["variableSuggester"],
            verbose=True,
            max_iter=1,
        )

    def copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config["copywriter"],
            verbose=True,
            max_iter=1,
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
            memory=True,
        )
