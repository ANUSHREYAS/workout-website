from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import TavilySearchTool
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Configuration & LLM Setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # Updated to a valid model version
    google_api_key="AIzaSyCUAF2ewsSvxJOVxsECabVuKRaeL_sGWx0"
)
search_tool = TavilySearchTool(api_key="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")

# 2. Define Health & Wellness Agents
fitness_specialist = Agent(
    role='Fitness & Strength Coach',
    goal='Create a customized workout plan based on the user goal: {goal}',
    backstory="""You are an elite personal trainer. You specialize in designing 
    exercise routines that are safe, effective, and tailored to individual fitness levels.""",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

nutritionist = Agent(
    role='Registered Dietitian',
    goal='Design a comprehensive meal plan and nutritional strategy for: {goal}',
    backstory="""You are an expert in human nutrition. You focus on balanced macros, 
    micronutrients, and sustainable eating habits that complement physical activity.""",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

lifestyle_coach = Agent(
    role='Holistic Wellness Coordinator',
    goal='Synthesize fitness and diet into a cohesive lifestyle plan including sleep and stress management.',
    backstory="""You ensure that the workout and diet plans are realistic. You add 
    lifestyle advice like hydration, sleep hygiene, and recovery techniques.""",
    llm=llm,
    verbose=True
)

# 3. Define Tasks
workout_task = Task(
    description="""Analyze the user's fitness goal: '{goal}'. 
    Create a 7-day workout schedule. Include specific exercises, sets, and reps.""",
    expected_output="A structured weekly workout routine.",
    agent=fitness_specialist
)

diet_task = Task(
    description="""Based on the goal '{goal}', create a daily meal structure. 
    Include caloric targets (approximate) and specific food recommendations.""",
    expected_output="A detailed nutrition guide and sample daily menu.",
    agent=nutritionist
)

lifestyle_task = Task(
    description="""Review the workout and diet plans. Add a 'Lifestyle & Recovery' section.
    Include tips on sleep, hydration, and mental wellness to support the goal: '{goal}'.""",
    expected_output="A final, polished Health & Wellness Blueprint in markdown format.",
    agent=lifestyle_coach,
    context=[workout_task, diet_task]
)

# 4. Assemble the Fitness Crew
wellness_crew = Crew(
    agents=[fitness_specialist, nutritionist, lifestyle_coach],
    tasks=[workout_task, diet_task, lifestyle_task],
    verbose=True
)

# 5. Execution
if __name__ == "__main__":
    print("--- 🏋️ AI Personal Health & Wellness Crew ---")
    
    user_goal = input("\nWhat are your fitness and health goals? (e.g., lose 10lbs, build muscle, marathon training): ")
    
    if user_goal:
        inputs = {'goal': user_goal}
        
        print(f"\nGenerating your personalized blueprint for: {user_goal}...\n")
        result = wellness_crew.kickoff(inputs=inputs)
        
        print("\n\n########################")
        print("## YOUR PERSONALIZED PLAN")
        print("########################\n")
        print(result)