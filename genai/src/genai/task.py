'''
from crewai import Task

def create_tasks(researcher, writer, reviewer):
    # Task 1: Research
    task1 = Task(
        description='Analyze the latest 2024-2025 trends in {topic}.',
        expected_output='A detailed report with 5 key bullet points.',
        agent=researcher
    )

    # Task 2: Writing
    task2 = Task(
        description='Using the research, write a 3-paragraph blog post about {topic}.',
        expected_output='A markdown formatted blog post.',
        agent=writer
    )

    # Task 3: Review
    task3 = Task(
        description='Review the blog post for clarity, grammar, and alignment with research.',
        expected_output='A polished final version of the blog post.',
        agent=reviewer,
        output_file='final_article.md' # Optional: saves the final result to a file
    )

    return [task1, task2, task3]'''