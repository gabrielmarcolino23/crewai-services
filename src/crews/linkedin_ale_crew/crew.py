from crewai import Agent, Crew, Process, Task
from src.base.custom_crew_base import CustomCrewBase
from src.tools.tavily_search import TavilySearchTool

class LinkedinPostAle(CustomCrewBase):
	"""Linkedin crew"""

	def __init__(self):
		super().__init__(
			agents_group_pool=["linkedin-post-ale"], tasks_group_pool=["linkedin-post-ale"],
		)
		self.tavily_tool = TavilySearchTool()

	def researcher(self) -> Agent:
		return Agent(config=self.agents_config["researcher"], verbose=True, tools=[self.tavily_tool])
	
	def linkedin_writer(self) -> Agent:
		return Agent(config=self.agents_config["linkedin_writer"], verbose=True)

	def linkedin_reviewer(self) -> Agent:
		return Agent(config=self.agents_config["linkedin_reviewer"], verbose=True)

	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config["research_task"],
			agent=self.researcher(),
		)
	
	def linkedin_writing_task(self) -> Task:
		return Task(
			config=self.tasks_config["linkedin_writing_task"],
			agent=self.linkedin_writer(),
		)

	def linkedin_reviewer_task(self) -> Task:
		return Task(
			config=self.tasks_config["linkedin_reviewer_task"],
			agent=self.linkedin_reviewer(),
		)

	def crew(self) -> Crew:
		"""Creates the Linkedin Ale crew"""
		return Crew(
			agents=[self.researcher(), self.linkedin_writer()],
			tasks=[self.research_task(), self.linkedin_writing_task()],
			process=Process.sequential,
			verbose=True,
		)