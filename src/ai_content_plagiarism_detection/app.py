import gradio as gr
import os
from pathlib import Path

from .crew import AiContentPlagiarismDetection
from .utils.file_processor import extract_text_from_file
from .utils.output_formatter import format_report


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
            formatted_report = format_report(
                report_content, os.path.basename(file.name)
            )
            return formatted_report
        else:
            return (
                "Plagiarism report not found. Please ensure the crew ran successfully."
            )
    except Exception as e:
        return f"An error occurred while running the crew: {str(e)}"


# Create the Gradio interface
def create_app():
    """Create and return the Gradio app."""

    with gr.Blocks(
        title="🔍 AI Plagiarism Detection",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 100% !important;
            margin: 0 !important;
            padding: 20px !important;
            height: 100% !important;
        }
        .main-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .upload-section {
            border: 2px dashed #e0e0e0;
            border-radius: 10px;
            padding: 2rem;
            margin: 1rem 0;
        }
        .component {
            width: 100% ;
        }

        #plagiarism-report {
            height: 70vh ;
            min-height: 500px ;
            overflow-y: auto ;
        }
        """,
    ) as app:
        with gr.Row():
            gr.Markdown(
                """
                # AI Plagiarism Detection System
                
                **Analyse your documents for potential plagiarism using advanced AI agents**
                
                Upload a text or PDF file to get a comprehensive plagiarism analysis report.
                """,
                elem_classes=["main-header", "component"],
            )

        with gr.Row():
            gr.Markdown(
                """
                ### Instructions
                1. Upload your document using the file uploader
                2. Click 'Analyse Document' to start the plagiarism detection
                3. Review the detailed analysis report
                (Please note that the analysis may take a few moments depending on document length.)
                """,
                elem_classes=["instructions", "component"],
            )

        with gr.Row():
            file_input = gr.File(
                label="Upload Document",
                file_types=[".txt", ".pdf"],
                file_count="single",
                elem_classes=["upload-section", "component"],
            )

        with gr.Row():
            analyze_btn = gr.Button(
                "Analyse Document", variant="primary", size="lg", scale=1
            )
            clear_btn = gr.Button("Clear", variant="secondary", scale=1)

        with gr.Row():
            output_report = gr.Markdown(
                label="Analysis Report",
                value="Upload a document and click 'Analyse Document' to see the plagiarism analysis results here.",
                elem_id="plagiarism-report",
                elem_classes=["full-width-component", "report-box"],
            )

        with gr.Row():
            with gr.Accordion("Supported File Types & Instructions", open=False):
                gr.Markdown(
                    """
                    **Supported Formats:**
                    - Text files (.txt)
                    - PDF documents (.pdf)
                    
                    **Instructions:**
                    1. Upload your document using the file uploader
                    2. Click 'Analyse Document' to start the plagiarism detection
                    3. Review the detailed analysis report
                    
                    **Note:** The analysis may take a few moments depending on document length.
                    """
                )

        # Event handlers
        analyze_btn.click(
            fn=analyze_uploaded_file,
            inputs=file_input,
            outputs=output_report,
            show_progress=True,
        )

        clear_btn.click(
            fn=lambda: (
                None,
                "Upload a document and click 'Analyze Document' to see the plagiarism analysis results here.",
            ),
            outputs=[file_input, output_report],
        )

    return app


# Launch function
def launch_app():
    """Launch the Gradio app."""
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)


if __name__ == "__main__":
    launch_app()
