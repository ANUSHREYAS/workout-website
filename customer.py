from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import TavilySearchTool
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Configuration & LLM Setup
# Gemini 1.5 Flash is highly recommended for speed and efficiency in CrewAI
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key="AIzaSyCUAF2ewsSvxJOVxsECabVuKRaeL_sGWx0"
)
search_tool = TavilySearchTool(api_key="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")

# 2. Define Problem-Solving Agents
researcher = Agent(
    role='Expert Solution Researcher',
    goal='Analyze the user problem: {problem} and find the most effective technical or product-based solutions.',
    backstory="""You are a world-class researcher. When given a problem, you look for 
    the root cause and find specific tools, products, or methods that solve it efficiently.""",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

writer = Agent(
    role='Solution Architect',
    goal='Transform research data into a clear, actionable solution plan for the user.',
    backstory="""You excel at communication. You take complex research and turn it into 
    a step-by-step guide that any user can follow to solve their specific issue.""",
    llm=llm,
    verbose=True
)

# 3. Define Tasks (Modified for Problem/Solution)
research_task = Task(
    description="""Carefully analyze the following user problem: '{problem}'. 
    Search for the best ways to solve this, including specific products or software if applicable. 
    Provide at least 3 distinct approaches or tools.""",
    expected_output="A detailed breakdown of 3 viable solutions with evidence of why they work.",
    agent=researcher
)

writing_task = Task(
    description="""Review the solutions found. Write a personalized response to the user.
    Explain WHY these solutions fix their specific problem: '{problem}'.
    Structure it as a 'Recommended Action Plan'.""",
    expected_output="A professional, empathetic, and actionable markdown report.",
    agent=writer,
    context=[research_task]
)

# 4. Assemble the Crew
solution_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

# 5. Interactive Execution
if __name__ == "__main__":
    print("--- 🤖 AI Problem-Solving Assistant ---")
    
    # Get dynamic input from the user
    user_problem = input("\nDescribe the problem you are facing: ")
    
    if user_problem:
        inputs = {
            'problem': user_problem
        }
        
        print(f"\nWorking on a solution for: {user_problem}...\n")
        result = solution_crew.kickoff(inputs=inputs)
        
        print("\n\n########################")
        print("## PROPOSED SOLUTION")
        print("########################\n")
        print(result)