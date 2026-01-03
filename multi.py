import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool # You can also use DuckDuckGoSearchRun
from dotenv import load_dotenv

load_dotenv()

# Set up your LLM and Tools
# Ensure you have OPENAI_API_KEY or GOOGLE_API_KEY in your .env
search_tool = SerperDevTool()

# 1. Research Agent
researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in {topic}',
    backstory="""You are an expert at identifying emerging trends. 
    You excel at finding the most relevant and recent information from multiple sources.""",
    tools=[search_tool],
    verbose=True
)

# 2. Writing Agent
writer = Agent(
    role='Content Strategist',
    goal='Craft a compelling and easy-to-read article about {topic}',
    backstory="""You turn complex technical data into engaging narratives. 
    Your writing is clear, professional, and optimized for a general audience.""",
    verbose=True
)

# 3. Review Agent
reviewer = Agent(
    role='Editorial Lead',
    goal='Proofread and refine the article for quality and accuracy',
    backstory="""You have a keen eye for detail. You ensure the tone is consistent, 
    the facts are checked, and the final output is ready for publication.""",
    verbose=True
)

# Define Tasks
task1 = Task(
    description='Analyze the latest 2024-2025 trends in {topic}.',
    expected_output='A detailed report with 5 key bullet points.',
    agent=researcher
)

task2 = Task(
    description='Using the research, write a 3-paragraph blog post about {topic}.',
    expected_output='A markdown formatted blog post.',
    agent=writer
)

task3 = Task(
    description='Review the blog post for clarity, grammar, and alignment with research.',
    expected_output='A polished final version of the blog post.',
    agent=reviewer
)

# Assemble the Crew
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[task1, task2, task3],
    process=Process.sequential
)

# Start the work
result = crew.kickoff(inputs={'topic': 'AI Agents in 2026'})
print(result)