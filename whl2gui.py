import os
import streamlit as st
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import TavilySearchTool


# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Health Coach", page_icon="🏋️")



# --- CORE LOGIC SETUP ---
# --- CORE LOGIC SETUP ---
# Paste your actual keys inside the quotes below
os.environ["GOOGLE_API_KEY"] = "AIzaSyDauEIMD0AUmjOXq0iWjbKWC7vPJ9ZrEYk"
os.environ["TAVILY_API_KEY"] = "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"

# Now define your LLM and Tools using those environment variables
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
search_tool = TavilySearchTool()

# Agent Definitions
discovery_agent = Agent(
    role='Health Intake Specialist',
    goal='Identify essential medical and lifestyle questions for {goal}',
    backstory="Expert health consultant finding required personal data points.",
    tools=[search_tool], 
    llm=llm, 
    verbose=True
    )

    # ... (rest of your fitness_agent, nutrition_agent, etc.)

fitness_agent = Agent(
        role='Fitness Coach',
        goal='Create workout plan based on {goal} and {personal_details}',
        backstory="Elite trainer designing routines for specific equipment/limits.",
        llm=llm, verbose=True
    )

nutrition_agent = Agent(
        role='Nutritionist',
        goal='Design meal plan based on {goal} and {personal_details}',
        backstory="Dietitian calculating macros and meal timing.",
        llm=llm, verbose=True
    )

lifestyle_agent = Agent(
        role='Lifestyle Coach',
        goal='Provide lifestyle and recovery advice for {goal} based on {personal_details}',
        backstory="Expert in sleep, stress management, and habit formation.",
        llm=llm, verbose=True
    )

    # --- UI LAYOUT ---
st.title("🏋️ AI Personal Health & Wellness Coach")
st.write("Get a custom workout, diet, and lifestyle plan researched specifically for your goals.")

    # STEP 1: Goal Input
user_goal = st.text_input("What is your fitness goal?", placeholder="e.g., Lose 5kg and start meditating")

if user_goal:
        # We use session_state to remember if we've already run the discovery
        if 'questions' not in st.session_state:
            if st.button("Step 1: Generate Discovery Questions"):
                with st.spinner("Searching Google for required intake details..."):
                    discovery_task = Task(
                        description=f"Identify 5-8 vital questions (height, weight, medical, equipment, lifestyle) needed for the goal: {user_goal}",
                        expected_output="A bulleted list of questions.",
                        agent=discovery_agent
                    )
                    crew = Crew(agents=[discovery_agent], tasks=[discovery_task])
                    result = crew.kickoff(inputs={'goal': user_goal})
                    st.session_state.questions = result.raw # Store in session
                    st.rerun()

        # STEP 2: Answer Questions
        if 'questions' in st.session_state:
            st.info("### 📋 Please provide your details:")
            st.markdown(st.session_state.questions)
            
            user_answers = st.text_area("Type your answers here:", placeholder="Height: 180cm, Weight: 80kg, Equipment: Dumbbells...")

            if st.button("Step 2: Generate My Full Plan"):
                with st.spinner("Analyzing your data and crafting your 7-day blueprint..."):
                    
                    # --- UPDATED TASKS FOR DAY-BY-DAY PLAN ---
                    w_task = Task(
                        description=f"Create a detailed 7-day workout schedule for: {user_goal}. Data: {user_answers}", 
                        expected_output="A day-by-day workout routine (Day 1 to Day 7) with specific exercises, sets, and reps.", 
                        agent=fitness_agent
                    )
                    n_task = Task(
                        description=f"Create a 7-day meal plan for: {user_goal}. Data: {user_answers}", 
                        expected_output="A daily meal plan (Day 1 to Day 7) including Breakfast, Lunch, Dinner, and Snacks.", 
                        agent=nutrition_agent
                    )
                    l_task = Task(
                        description=f"Provide 7 days of lifestyle habits for: {user_goal}. Data: {user_answers}", 
                        expected_output="A 7-day checklist for sleep, hydration, and stress management.", 
                        agent=lifestyle_agent
                    )

                    final_crew = Crew(
                        agents=[fitness_agent, nutrition_agent, lifestyle_agent],
                        tasks=[w_task, n_task, l_task],
                        verbose=True
                    )
                    
                    # Execute the crew
                    final_crew.kickoff()
                    
                    st.success("✅ Your 7-Day Plan is Ready!")
                    st.markdown("---")
                    
                    # --- UI TABS FOR BETTER VIEWING ---
                    tab1, tab2, tab3 = st.tabs(["🏋️ Workout", "🥗 Nutrition", "🛌 Lifestyle"])

                    with tab1:
                        st.markdown(w_task.output.raw)
                    
                    with tab2:
                        st.markdown(n_task.output.raw)

                    with tab3:
                        st.markdown(l_task.output.raw)
                    
                    # Download button for the full combined plan
                    full_plan = f"# Workout Plan\n{w_task.output.raw}\n\n# Nutrition Plan\n{n_task.output.raw}"
                    st.download_button("Download Full Plan", full_plan, file_name="7_day_health_plan.md")