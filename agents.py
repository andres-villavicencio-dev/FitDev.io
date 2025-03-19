from crewai import Agent
from crewai_tools import DirectoryReadTool, FileReadTool
from langchain_openai import ChatOpenAI
import os
#os.environ["OPENAI_API_BASE"]='http://localhost:11434/v1'
#os.environ["OPENAI_MODEL_NAME"]='llama3:instruct'
os.environ["OPENAI_API_KEY"]='NA'

llm_mistral = ChatOpenAI(
    model = "mistral-small",
    base_url = "http://localhost:11434/v1",
    api_key="NA")

llm_gemma = ChatOpenAI(
    model = "gemma3",
    base_url = "http://localhost:11434/v1",
    api_key="NA")

# Define the Directory Read Tool
directory = "/home/andus/Documents/Fitbank/Projects/fit-base/fuentes/negocio/electronic-money/src/"
directory_read_tool = DirectoryReadTool(directory)

# Define the File Read Tool
file_read_tool = FileReadTool()

class CodeReviewAgents():
    # Define the Code Reviewer Agent
    def code_reviewer(self): 
        return Agent(
            role='Code Reviewer',
            goal='Read and analyze each Java file in the project directory',
            verbose=True,
            #memory=True,
            backstory='A seasoned developer with a knack for understanding and documenting code.',
            tools=[directory_read_tool, file_read_tool],
            allow_delegation=True,
            llm=llm_mistral,
            function_calling=llm_mistral
    )

    # Define the Documentation Generator Agent
    def documentation_generator(self):
        return Agent(
            role='Documentation Generator',
            goal='Compile analysis into a comprehensive technical document',
            verbose=True,
            #memory=True,
            backstory='An expert in creating detailed technical documentation from code analysis.',
            tools=[],  # No specific tools needed for this agent
            allow_delegation=True,
            llm=llm_mistral
    )

    # Define the Report Creator Agent
    def report_creator(self): 
        return Agent(
            role='Report Creator',
            goal='Format the technical documentation into a Markdown report',
            verbose=True,
            #memory=True,
            backstory='A skilled writer who can present technical information clearly and concisely.',
            tools=[],  # No specific tools needed for this agent
            allow_delegation=True,
            llm=llm_gemma
    )
