from crewai import Agent, Crew, Process, Task
from src.base.custom_crew_base import CustomCrewBase

class SegmentAiCrew(CustomCrewBase):
	"""SegmentAi crew"""

	def __init__(self):
		super().__init__(
			agents_group_pool=["segment-builder"], tasks_group_pool=["segment-builder"]
		)

	def segment_builder(self) -> Agent:
		return Agent(config=self.agents_config["segment_builder"], verbose=True)

	def build_segment_task(self) -> Task:
		return Task(
			config=self.tasks_config["segment_builder_task"],
			agent=self.segment_builder(),
		)

	def crew(self) -> Crew:
		"""Creates the SegmentAi crew"""
		return Crew(
			agents=[self.segment_builder()],
			tasks=[self.build_segment_task()],
			process=Process.sequential,
			verbose=True,
		)