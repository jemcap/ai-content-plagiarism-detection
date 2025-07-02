import gradio as gr
import os
from pathlib import Path

from .crew import AiContentPlagiarismDetection
from .utils.file_processor import extract_text_from_file


def analyze_uploaded_file(file):
    if file is None:
        return "No file uploaded."

    try:
        text_content = extract_text_from_file(file.name)
        if (
            "Unsupported file type" in text_content
            or "Error reading file" in text_content
        ):
            return text_content
        if not text_content.strip():
            return "The uploaded file is empty or contains no readable text."

    except Exception as e:
        return f"Error processing file: {str(e)}"

    try:
        inputs = {"input": text_content, "file_name": os.path.basename(file.name)}

        crew = AiContentPlagiarismDetection().crew()
        result = crew.kickoff(inputs=inputs)

        report_path = Path("output/plagiarism_report.md")
        if report_path.exists():
            with open(report_path, "r", encoding="utf-8") as report_file:
                report_content = report_file.read()
            return report_content
        else:
            return (
                "Plagiarism report not found. Please ensure the crew ran successfully."
            )
    except Exception as e:
        return f"An error occurred while running the crew: {str(e)}"


# Create the Gradio interface
def create_app():
    """Create and return the Gradio app."""

    app = gr.Interface(
        fn=analyze_uploaded_file,
        inputs=gr.File(
            label="📁 Upload Document (.txt, .pdf files supported)",
            file_types=[".txt", ".pdf"],
        ),
        outputs=gr.Markdown(
            label="🔍 Plagiarism Analysis Report", elem_id="plagiarism-report"
        ),
        title="🔍 AI Plagiarism Detection",
        description="Upload a text file to analyze for potential plagiarism using AI agents.",
        examples=None,
        allow_flagging="never",
        live=False,
        show_progress="full",
    )

    return app


# Launch function
def launch_app():
    """Launch the Gradio app."""
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)


if __name__ == "__main__":
    launch_app()
