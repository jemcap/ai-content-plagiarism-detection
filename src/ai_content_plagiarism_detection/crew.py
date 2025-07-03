from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class AiContentPlagiarismDetection():
    """AiContentPlagiarismDetection crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    @agent
    def text_analyzer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['text_analyzer_agent'], # type: ignore[index]
            verbose=True
        )

    @agent
    def similarity_checker_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['similarity_checker_agent'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],  # Using SerperDevTool for web search capabilities
        )
        
    @agent
    def content_improvement_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['content_improvement_agent'], # type: ignore[index]
            verbose=True
        )
        
    @agent
    def plagiarism_report_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['plagiarism_report_agent'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def text_analyzer(self) -> Task:
        return Task(
            config=self.tasks_config['text_analyzer'], # type: ignore[index]
        )

    @task
    def similarity_checker(self) -> Task:
        return Task(
            config=self.tasks_config['similarity_checker'], # type: ignore[index]
        )
        
    @task
    def content_improvement(self) -> Task:
        return Task(
            config=self.tasks_config['content_improvement'], # type: ignore[index]
        )
    
    @task
    def plagiarism_report(self) -> Task:
        return Task(
            config=self.tasks_config['plagiarism_report'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AiContentPlagiarismDetection crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
        
    def update_output_paths(self, output_dir: str):
        """Update all task output paths to use the provided output directory"""
        if not output_dir or not os.path.exists(output_dir):
            print(f"Warning: Output directory '{output_dir}' does not exist.")
            os.makedirs(output_dir, exist_ok=True)
            
        for task in self.tasks:
            if hasattr(task, 'output_file') and task.output_file:
                # Replace placeholder or extract filename from existing path
                if "__DYNAMIC_PATH__" in task.output_file:
                    task.output_file = task.output_file.replace("__DYNAMIC_PATH__", output_dir)
                else:
                    filename = os.path.basename(task.output_file)
                    task.output_file = os.path.join(output_dir, filename)
                    
                print(f"Updated task '{task.name}' output path: {task.output_file}")
