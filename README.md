# AiContentPlagiarismDetection Crew

Welcome to the AiContentPlagiarismDetection Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/ai_content_plagiarism_detection/config/agents.yaml` to define your agents
- Modify `src/ai_content_plagiarism_detection/config/tasks.yaml` to define your tasks
- Modify `src/ai_content_plagiarism_detection/crew.py` to add your own logic, tools and specific args
- Modify `src/ai_content_plagiarism_detection/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the ai-content-plagiarism-detection Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The ai-content-plagiarism-detection Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Features

### Unique Report Generation

Each document analysis creates a unique report in its own directory, preventing any overlap between different analyses. The system:

- Creates a timestamped and unique output directory for each file upload
- Ensures that output paths are correctly updated for all tasks
- Includes a unique report ID in each report for traceability
- Properly handles file serving to display the correct report for each analysis

This ensures that when users upload multiple files in sequence, each analysis is completely independent and reports are not mixed up.

### Gradio Web Interface

The system includes a user-friendly web interface built with Gradio, allowing users to:
- Upload text and PDF documents
- Analyze documents for potential plagiarism
- View formatted plagiarism reports with clear source attribution
- Reset the interface between analyses

## Support

For support, questions, or feedback regarding the AiContentPlagiarismDetection Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
# ai-content-plagiarism-detection
