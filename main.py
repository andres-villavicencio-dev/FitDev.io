from crewai import Crew, Process
from agents import CodeReviewAgents
from tasks import CodeReviewTasks
from crewai_tools import DirectoryReadTool, FileReadTool
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from dotenv import load_dotenv
_ = load_dotenv()

directory = "/home/andus/Documents/Fitbank/Projects/fit-base/fuentes/negocio/electronic-money/src/"

"""directory_read_tool = DirectoryReadTool(directory,config=dict(
        llm=dict(
            provider="ollama", # Options include ollama, google, anthropic, llama2, and more
            config=dict(
                model="llama3:instruct",
                api_key="NA",
                api_base="http://localhost:11434/v1"
            ),
        ),
        embedder=dict(
            provider="ollama",
            config=dict(
                model="llama3:instruct",
                api_key="NA",
                api_base="http://localhost:11434/v1"
            ),
        ),
    )
)"""
directory_read_tool = DirectoryReadTool(directory)
"""file_read_tool = FileReadTool(config=dict(
        llm=dict(
            provider="ollama", # Options include ollama, google, anthropic, llama2, and more
            config=dict(
                model="llama3:instruct",
                api_key="NA",
                api_base="http://localhost:11434/v1"
            ),
        ),
        embedder=dict(
            provider="ollama",
            config=dict(
                model="llama3:instruct",
                api_key="NA",
                api_base="http://localhost:11434/v1"
            ),
        ),
    ))"""
file_read_tool = FileReadTool()

tasks = CodeReviewTasks()
agents = CodeReviewAgents()

code_reviewer = agents.code_reviewer()
documentation_generator = agents.documentation_generator()
report_creator = agents.report_creator()

read_directory_task = tasks.read_directory_task(directory_read_tool, code_reviewer)
analyze_java_files_task = tasks.analyze_java_files_task(file_read_tool, code_reviewer)
generate_documentation_task = tasks.generate_documentation_task(documentation_generator)
create_pdf_report_task = tasks.create_pdf_report_task(report_creator)

# Form the Crew with the defined agents and tasks
crew = Crew(
    agents=[code_reviewer, documentation_generator, report_creator],
    tasks=[read_directory_task, analyze_java_files_task, generate_documentation_task, create_pdf_report_task],
    process=Process.sequential,  # Sequential task execution
)

# Kick off the Crew with the specified input
result = crew.kickoff(inputs={'directory': directory})
print(result)