from crewai import Task
from textwrap import dedent


class CodeReviewTasks():
    # Read Directory Task
    def read_directory_task(self, tool, agent):
        return Task(
            description=dedent("""Read the directory tree and identify all Java files at the Project Directory.
                               Project Directory: 
                            {directory}
                               """),
            expected_output='A list of all the Java files in the project directory',
            tools=[tool],
            agent=agent
    )

    # Analyze Java Files Task
    def analyze_java_files_task(self, tool, agent): 
        return Task(
        description='Analyze each Java file and extract relevant, in-depth technical information. Approach this task thinking step by step.',
        expected_output='Technical documentation of each Java file',
        tools=[tool],
        agent=agent
    )

    # Generate Documentation Task
    def generate_documentation_task(self, agent): 
        return Task(
            description='Compile the extracted information into a comprehensive technical document',
            expected_output='A detailed technical document covering all Java files',
            tools=[],  # No specific tools needed for this task
            agent=agent
    )

    # Create PDF Report Task
    def create_pdf_report_task(self, agent):
        return Task(
        description='Format the technical document into a Markdown report',
        expected_output='A Markdown formated report containing the technical documentation',
        tools=[],  # No specific tools needed for this task
        agent=agent,
        output_file='technical_documentation_report.md'
    )
