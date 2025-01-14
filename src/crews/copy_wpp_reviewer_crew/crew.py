from crewai import Agent, Crew, Process, Task
from src.base.custom_crew_base import CustomCrewBase

class ReviewerwppCrew(CustomCrewBase):
    """Reviewerwpp crew"""

    def __init__(self):
        super().__init__(
            agents_group_pool=["reviewer-wpp"], tasks_group_pool=["reviewer-wpp"]
        )

    def reviewerwpp(self) -> Agent:
        return Agent(config=self.agents_config["reviewerwpp"], verbose=True)

    def reviewerwpp_task(self) -> Task:
        return Task(
            config=self.tasks_config["reviewerwpp_task"],
            agent=self.reviewerwpp(),
        )

    def crew(self) -> Crew:
        """Creates the Reviewerwpp crew"""
        return Crew(
            agents=[self.reviewerwpp()],
            tasks=[self.reviewerwpp_task()],
            process=Process.sequential,
            verbose=True,
        )
