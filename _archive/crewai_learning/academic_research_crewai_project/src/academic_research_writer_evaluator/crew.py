import os


from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	ExaSearchTool,
	ScrapeWebsiteTool,
	ArxivPaperTool,
	BraveSearchTool,
	SerplyScholarSearchTool
)
from academic_research_writer_evaluator.tools.semantic_scholar_search_tool import SemanticScholarSearchTool





@CrewBase
class AcademicResearchWriterEvaluatorCrew:
    """AcademicResearchWriterEvaluator crew"""

    
    @agent
    def academic_research_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["academic_research_specialist"],
            
            
            tools=[				ExaSearchTool(),
				ScrapeWebsiteTool(),
				SemanticScholarSearchTool(),
				ArxivPaperTool(),
				SerplyScholarSearchTool()],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def senior_content_writer(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["senior_content_writer"],
            
            
            tools=[				BraveSearchTool(),
				SerplyScholarSearchTool()],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def content_quality_evaluator(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["content_quality_evaluator"],
            
            
            tools=[				SerplyScholarSearchTool()],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def quality_gate(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["quality_gate"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def report_compiler(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["report_compiler"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def workflow_manager(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["workflow_manager"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def document_delivery_agent(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["document_delivery_agent"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    

    
    @task
    def research_mission(self) -> Task:
        return Task(
            config=self.tasks_config["research_mission"],
            markdown=False,
            
            
        )
    
    @task
    def write_article(self) -> Task:
        return Task(
            config=self.tasks_config["write_article"],
            markdown=False,
            
            
        )
    
    @task
    def evaluate_content(self) -> Task:
        return Task(
            config=self.tasks_config["evaluate_content"],
            markdown=False,
            
            
        )
    
    @task
    def quality_gate_check(self) -> Task:
        return Task(
            config=self.tasks_config["quality_gate_check"],
            markdown=False,
            
            
        )
    
    @task
    def manager_review_and_score(self) -> Task:
        return Task(
            config=self.tasks_config["manager_review_and_score"],
            markdown=False,
            
            
        )
    
    @task
    def compile_final_report(self) -> Task:
        return Task(
            config=self.tasks_config["compile_final_report"],
            markdown=False,
            
            
        )
    
    @task
    def deliver_clean_report(self) -> Task:
        return Task(
            config=self.tasks_config["deliver_clean_report"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the AcademicResearchWriterEvaluator crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,

            chat_llm=LLM(model="openai/gpt-4o-mini"),
        )


