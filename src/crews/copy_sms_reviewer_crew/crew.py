from crewai import Agent, Crew, Process, Task
from src.base.custom_crew_base import CustomCrewBase


class ReviewersmsCrew(CustomCrewBase):
    """Reviewersms crew"""

    def __init__(self):
        super().__init__(
            agents_group_pool=["reviewer-sms"], tasks_group_pool=["reviewer-sms"]
        )

    def reviewersms(self) -> Agent:
        return Agent(config=self.agents_config["reviewersms"], verbose=True)

    def reviewersms_task(self) -> Task:
        return Task(
            config=self.tasks_config["reviewersms_task"],
            agent=self.reviewersms(),
        )

    def crew(self) -> Crew:
        """Creates the Reviewersms crew"""
        return Crew(
            agents=[self.reviewersms()],
            tasks=[self.reviewersms_task()],
            process=Process.sequential,
            verbose=True,
        )
