import yaml
import os


class CustomCrewBase:
    def __init__(self, agents_group_pool: list, tasks_group_pool: list):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self._generateAgentsConfig(agents_group_pool)
        self._generateTasksConfig(tasks_group_pool)

    def _generateAgentsConfig(self, agents_group_pool: list):
        agents_config = {}

        for agent_group in agents_group_pool:
            group_config_path = os.path.join(
                self.base_dir, f"../config/{agent_group}/agents.yaml"
            )
            group_config: dict = self.generateConfig(group_config_path)
            if not isinstance(group_config, dict):
                raise ValueError(
                    f"Invalid configuration in {group_config_path}. "
                    f"Expected a dictionary but got {type(group_config).__name__}"
                )
            for agent_name, agent_config in group_config.items():
                if agents_config.get(agent_name) is not None:
                    raise ValueError(f"Agent {agent_name} already exists in the config")
                agents_config[agent_name] = agent_config
        self.agents_config = agents_config

    def _generateTasksConfig(self, tasks_group_pool: list):
        tasks_config = {}
        for task_group in tasks_group_pool:
            group_config_path = os.path.join(
                self.base_dir, f"../config/{task_group}/tasks.yaml"
            )
            group_config: dict = self.generateConfig(group_config_path)
            if not isinstance(group_config, dict):
                raise ValueError(
                    f"Invalid configuration in {group_config_path}. "
                    f"Expected a dictionary but got {type(group_config).__name__}"
                )
            for task_name, task_config in group_config.items():
                if tasks_config.get(task_name) is not None:
                    raise ValueError(f"Task {task_name} already exists in the config")
                tasks_config[task_name] = task_config
        self.tasks_config = tasks_config

    def generateConfig(self, name: str) -> dict:
        with open(name, "r") as file:
            config = yaml.safe_load(file)
        return config
