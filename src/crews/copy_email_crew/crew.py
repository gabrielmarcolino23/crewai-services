from crewai import Agent, Crew, Process, Task, LLM
from src.base.custom_crew_base import CustomCrewBase
from src.outputs.email_output import EmailOutput
from src.LLMs.open_ai import faster_4o_mini_model, creative_4o_mini_model

from dotenv import load_dotenv

load_dotenv()

debug = False


class CopyEmailCrew(CustomCrewBase):
    """CopyEmail crew"""

    def __init__(self):
        super().__init__(
            agents_group_pool=["copy-email"], tasks_group_pool=["copy-email"]
        )

    def variableSuggester(self) -> Agent:
        return Agent(
            config=self.agents_config["variableSuggester"],
            verbose=debug,
            cache=False,
            max_iter=1,
            llm=faster_4o_mini_model,
        )

    def estrategista_de_marketing(self) -> Agent:
        return Agent(
            config=self.agents_config["estrategista_de_marketing"],
            verbose=debug,
            cache=False,
            max_iter=1,
            llm=faster_4o_mini_model,
        )

    def redator_de_conteudo(self) -> Agent:
        return Agent(
            config=self.agents_config["redator_de_conteudo"],
            verbose=debug,
            cache=False,
            max_iter=1,
            llm=creative_4o_mini_model,
        )

    def estilista_html(self) -> Agent:
        return Agent(
            config=self.agents_config["estilista_html"],
            verbose=debug,
            cache=False,
            max_iter=1,
            llm=creative_4o_mini_model,
        )

    def variableSuggester_task(self) -> Task:
        return Task(
            config=self.tasks_config["variableSuggester_task"],
            agent=self.variableSuggester(),
        )

    def tarefa_extrair_inputs(self) -> Task:
        return Task(
            config=self.tasks_config["tarefa_extrair_inputs"],
            agent=self.estrategista_de_marketing(),
        )

    def tarefa_gerar_conteudo_email(self) -> Task:
        return Task(
            config=self.tasks_config["tarefa_gerar_conteudo_email"],
            agent=self.redator_de_conteudo(),
        )

    def tarefa_estilizar_email(self) -> Task:
        return Task(
            config=self.tasks_config["tarefa_estilizar_email"],
            agent=self.estilista_html(),
            output_pydantic=EmailOutput,
        )

    def crew(self) -> Crew:
        """Creates the CopyEmail crew"""
        return Crew(
            agents=[
                self.estrategista_de_marketing(),
                self.variableSuggester(),
                self.redator_de_conteudo(),
                self.estilista_html(),
            ],
            tasks=[
                self.tarefa_extrair_inputs(),
                self.variableSuggester_task(),
                self.tarefa_gerar_conteudo_email(),
                self.tarefa_estilizar_email(),
            ],
            process=Process.sequential,
            verbose=debug,
        )
