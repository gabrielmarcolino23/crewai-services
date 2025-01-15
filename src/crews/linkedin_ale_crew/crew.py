from crewai import Agent, Crew, Process, Task
from src.base.custom_crew_base import CustomCrewBase

class LinkedinPostAle(CustomCrewBase):
	"""SegmentAi crew"""

	def __init__(self):
		super().__init__(
			agents_group_pool=["linkedin-post-ale"], tasks_group_pool=["linkedin-post-ale"]
		)

	def researcher(self) -> Agent:
		return Agent(config=self.agents_config["researcher"], verbose=True)
	
	def linkedin_writer(self) -> Agent:
		return Agent(config=self.agents_config["linkedin_writer"], verbose=True)

	def linkedin_reviwer(self) -> Agent:
		return Agent(config=self.agents_config["linkedin_reviwer"], verbose=True)

	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config["research_task"],
			agent=self.researcher(),
		)
	
	def linkdin_writing_task(self) -> Task:
		return Task(
			config=self.tasks_config["linkdin_writing_task"],
			agent=self.linkedin_writer(),
		)

	def linkedin_reviwer_task(self) -> Task:
		return Task(
			config=self.tasks_config["linkedin_reviwer_task"],
			agent=self.linkedin_reviwer(),
		)

	def crew(self) -> Crew:
		"""Creates the Linkedin Ale crew"""
		return Crew(
			agents=[self.researcher(), self.linkedin_writer(), self.linkedin_reviwer()],
			tasks=[self.research_task(), self.linkdin_writing_task(), self.linkedin_reviwer_task()],
			process=Process.sequential,
			verbose=True,
		)