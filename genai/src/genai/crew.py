'''
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Genai():
    """Genai crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Genai crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
        '''
''' chat gpt code
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class Genai():
    """Genai crew defined without external YAML files"""

    # Define configurations directly as dictionaries
    agents_config = {
        'researcher': {
            'role': 'Senior Research Analyst',
            'goal': 'Uncover cutting-edge developments in {topic}',
            'backstory': 'You are an expert at identifying emerging trends and gathering deep insights.'
        },
        'reporting_analyst': {
            'role': 'Reporting Analyst',
            'goal': 'Create detailed reports based on {topic} research findings',
            'backstory': 'You excel at turning complex research into clear, actionable markdown reports.'
        }
    }

    tasks_config = {
        'research_task': {
            'description': 'Conduct a thorough research about {topic} in 2026.',
            'expected_output': 'A list with 10 bullet points of the most relevant information.'
        },
        'reporting_task': {
            'description': 'Review the research and expand it into a full markdown report.',
            'expected_output': 'A fully fledged markdown report.'
        }
    }

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )'''
'''
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import TavilySearchTool
import os
from crewai.llm import LLM
from dotenv import load_dotenv
load_dotenv()
# -----------------------------
# LLM (EXPLICIT)
# -----------------------------

llm = LLM(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)

# -----------------------------
# TAVILY SEARCH TOOL
# -----------------------------

 

search_tool = TavilySearchTool(
    tavily_api_key=os.getenv('TAVILY_API_KEY'),
    max_results=5
)

# -----------------------------
# AGENTS (STATIC)
# -----------------------------

researcher = Agent(
    role="Research Agent",
    goal="Collect accurate factual information",
    backstory="Expert researcher who gathers verified facts only",
    tools=[search_tool],        # ✅ ONLY researcher gets tools
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Writer Agent",
    goal="Write clear content from provided research",
    backstory="Professional writer who does not invent facts",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Review Agent",
    goal="Improve clarity and correctness of written content",
    backstory="Strict editor who does not add new information",
    llm=llm,
    verbose=True
)

# -----------------------------
# LOOP
# -----------------------------

print("\n🧠 Multi-Agent Pipeline (type 'exit' to quit)\n")

while True:
    user_input = input("Enter a topic: ").strip()

    if user_input.lower() in ("exit", "quit"):
        print("Exiting...")
        break

    if not user_input:
        print("⚠ Enter a valid topic.\n")
        continue

    # -----------------------------
    # TASKS (PIPELINE-DRIVEN)
    # -----------------------------

    research_task = Task(
        description=f"""
Research the topic: "{user_input}"

Rules:
- Use search when required
- Only factual information
- Bullet points
- No opinions
""",
        expected_output="Bullet list of researched facts",
        agent=researcher
    )

    write_task = Task(
        description="""
Write a clear, structured article
using ONLY the research provided above.
""",
        expected_output="Well-structured article",
        agent=writer
    )

    review_task = Task(
        description="""
Review the article for:
- Clarity
- Logical flow
- Grammar

Do NOT add new facts.
""",
        expected_output="Final polished article",
        agent=reviewer
    )

    # -----------------------------
    # CREW EXECUTION
    # -----------------------------

    crew = Crew(
        agents=[researcher, writer, reviewer],
        tasks=[research_task, write_task, review_task],
        verbose=False
    )

    result = crew.kickoff()

    print("\n📄 FINAL OUTPUT:\n")
    print(result)
    print("\n" + "-" * 50 + "\n")
''