'''import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import TavilySearchResults


load_dotenv()'''
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import TavilySearchTool
import os
from crewai.llm import LLM
from dotenv import load_dotenv
load_dotenv()

# 1. Configuration & LLM Setup
# Note: Ensure GOOGLE_API_KEY and TAVILY_API_KEY are in your .env file
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # Use 1.5-flash for speed or 1.5-pro for complex reasoning
    google_api_key="AIzaSyBsH0g9LETLCpSwwzdKKZ-OMdL4ynowHEs"
)

search_tool = TavilySearchTool(api_key="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")

# 3. Define Agents
researcher = Agent(
    role='Product Researcher',
    goal='Find the top 3 products for {topic} based on {requirements}',
    backstory="""You are an expert at scouring the internet for the best tech and lifestyle products. 
    You focus on technical specs, user reviews, and value for money.""",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

writer = Agent(
    role='Shopping Consultant',
    goal='Create a persuasive and clear comparison of the products found.',
    backstory="""You take technical data and turn it into easy-to-read shopping advice. 
    You highlight why each option is a good fit for the user's specific use case.""",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role='Quality Assurance Specialist',
    goal='Review the final recommendations for accuracy and budget alignment.',
    backstory="""You are picky and detail-oriented. You ensure that the products actually 
    meet the user's budget and technical requirements before giving the final green light.""",
    llm=llm,
    verbose=True
)

# 4. Define Tasks
research_task = Task(
    description="""Search for the best {topic} that meet these requirements: {requirements}. 
    Find exactly 3 options with prices and key specs.""",
    expected_output="A summary of 3 distinct products with their pros, cons, and current pricing.",
    agent=researcher
)

writing_task = Task(
    description="""Take the research results and write a structured recommendation report. 
    Include a 'Best Overall', 'Best Value', and 'Premium Choice' label.""",
    expected_output="A professionally formatted markdown report comparing the 3 products.",
    agent=writer,
    context=[research_task]
)

review_task = Task(
    description="""Review the report. Check if the products are within the user's budget and 
    if the specs match the 'Primary Use Case'. If anything is wrong, ask for a revision.""",
    expected_output="A finalized, verified shopping guide ready for the customer.",
    agent=reviewer,
    context=[writing_task]
)

## 5. Assemble the Crew
shopping_crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, writing_task, review_task],
    # process=Process.sequential,  <-- REMOVE THIS LINE
    verbose=True
)

# 6. Execute
if __name__ == "__main__":
    print("--- 🛒 Multi-Agent Shopping Crew Started ---")
    
    # Example inputs
    inputs = {
        'topic': 'Gaming Laptops',
        'requirements': 'Budget under $1500, must have at least an RTX 4060, and good thermal cooling.'
    }
    
    result = shopping_crew.kickoff(inputs=inputs)
    
    print("\n\n########################")
    print("## FINAL RECOMMENDATION")
    print("########################\n")
    print(result)