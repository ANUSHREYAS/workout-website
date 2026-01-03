from crewai import Agent, Task, Crew
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
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
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