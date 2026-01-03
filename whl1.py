from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import TavilySearchTool
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Configuration
# Note: Use gemini-1.5-flash or gemini-2.0-flash (2.5 is not yet a standard release)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key="YOUR_KEY")
search_tool = TavilySearchTool(api_key="YOUR_KEY")

# 2. Define specialized Agents
# NEW: The Discovery Agent finds out what we need to know about YOU
discovery_agent = Agent(
    role='Health Intake Specialist',
    goal='Identify the essential medical, physical, and lifestyle questions needed for goal: {goal}',
    backstory="""You are a professional health consultant. You use search tools to find 
    standard medical and fitness intake requirements (like BMI needs, equipment access, 
    and health contraindications) specific to a user's goal.""",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

fitness_specialist = Agent(
    role='Fitness Coach',
    goal='Create a workout plan based on user goal and their personal data.',
    backstory="You design routines based on available equipment and physical limits.",
    llm=llm,
    verbose=True
)

nutritionist = Agent(
    role='Nutritionist',
    goal='Design a meal plan based on user biometrics and lifestyle.',
    backstory="You calculate macros and meal timing based on the user's specific daily schedule.",
    llm=llm,
    verbose=True
)
lifestyle_agent = Agent(
    role='Lifestyle Coach',
    goal='Provide actionable lifestyle modifications based on health conditions and goal: {goal}',
    backstory="""You are an expert in behavioral science and wellness. You look at 
    the user's health conditions and personal details to recommend changes in sleep, 
    stress management, and daily habits to help them reach their goal safely.""",
    llm=llm,
    verbose=True
)

# 3. Task for Discovery (This happens first)
discovery_task = Task(
    description="""Search Google to find out what personal details (height, weight, 
    medical history, equipment, lifestyle habits) are required to safely and 
    accurately plan for the goal: '{goal}'. Output these as a clear list of questions.""",
    expected_output="A list of 5-10 specific discovery questions.",
    agent=discovery_agent
)

# 4. Main Execution Logic
if __name__ == "__main__":
    print("--- 🏋️ AI Personal Health Discovery ---")
    user_goal = input("\nWhat is your fitness goal? ")

    # Step A: Identify what we need to ask
    discovery_crew = Crew(agents=[discovery_agent], tasks=[discovery_task])
    questions_result = discovery_crew.kickoff(inputs={'goal': user_goal})

    print("\n--- 📋 TO PROVIDE AN ACCURATE PLAN, PLEASE ANSWER THE FOLLOWING ---")
    print(questions_result)
    
    # Step B: User provides their specific details
    user_answers = input("\nPlease provide your answers (you can type them all at once): ")

    # Step C: Run the full planning crew with the new personal data
    combined_inputs = {
        'goal': user_goal,
        'personal_details': user_answers
    }

    # Redefine tasks to include 'personal_details'
    workout_task = Task(
        description="Create a workout for {goal} using these details: {personal_details}",
        expected_output="7-day workout plan.",
        agent=fitness_specialist
    )

    diet_task = Task(
        description="Create a diet for {goal} using these details: {personal_details}",
        expected_output="Nutritional plan with calories/macros.",
        agent=nutritionist
    )
    lifestyle_task = Task(
    description="""Analyze the {personal_details} and {goal}. Identify specific 
    lifestyle habits (like sleep hygiene, stress reduction, or daily movement) 
    that need adjustment to support their health condition and fitness progress.""",
    expected_output="A list of 3-5 specific lifestyle changes and habit recommendations.",
    agent=lifestyle_agent
)

    final_crew = Crew(
    agents=[fitness_specialist, nutritionist, lifestyle_agent], # Added lifestyle_agent
    tasks=[workout_task, diet_task, lifestyle_task],            # Added lifestyle_task
    verbose=True
)

    print(f"\nProcessing your custom plan...\n")
    final_plan = final_crew.kickoff(inputs=combined_inputs)

    print("\n\n########################")
    print("## YOUR CUSTOM BLUEPRINT")
    print("########################\n")
    print(final_plan)