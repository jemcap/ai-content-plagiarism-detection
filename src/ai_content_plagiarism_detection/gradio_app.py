import gradio as gr
import os
import uuid
from pathlib import Path
from datetime import datetime

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
        # Create a unique output directory for this analysis
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_basename = os.path.basename(file.name).split('.')[0]
        unique_id = str(uuid.uuid4())[:8]
        output_dir = f"output/{timestamp}_{file_basename}_{unique_id}"
        
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Track the current analysis
        with open("output/last_analysis.txt", "w") as status_file:
            status_info = {
                "timestamp": timestamp,
                "filename": os.path.basename(file.name),
                "output_dir": output_dir
            }
            status_file.write(str(status_info))
        
        # Define output paths for this analysis
        text_segments_path = f"{output_dir}/text_segments.json"
        similarity_report_path = f"{output_dir}/similarity_report.md"
        plagiarism_report_path = f"{output_dir}/plagiarism_report.md"
        
        print(f"Analysis output directory: {output_dir}")
        print(f"Plagiarism report will be saved to: {plagiarism_report_path}")

        # Update the inputs with the output directory
        inputs = {
            "input": text_content, 
            "file_name": os.path.basename(file.name),
            "output_dir": output_dir
        }
        
        # Create and configure the crew
        crew_instance = AiContentPlagiarismDetection()
        crew = crew_instance.crew()
        
        # Update all task output paths for this analysis using the new method
        crew_instance.update_output_paths(output_dir)
        
        result = crew.kickoff(inputs=inputs)

        # First check if the report exists at the expected path
        if Path(plagiarism_report_path).exists():
            with open(plagiarism_report_path, "r", encoding="utf-8") as report_file:
                report_content = report_file.read()
            formatted_report = format_report(
                report_content, 
                os.path.basename(file.name),
                output_dir  # Pass the output directory to the formatter
            )
            return formatted_report
        else:
            return (
                f"Plagiarism report not found at {plagiarism_report_path}. Please ensure the crew ran successfully."
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
                "Upload a document and click 'Analyse Document' to see the plagiarism analysis results here.",
            ),
            outputs=[file_input, output_report],
        )

    return app


# Launch function
def launch_app():
    """Launch the Gradio app."""
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    app = create_app()
    app.launch(
        server_name="0.0.0.0", 
        server_port=7860, 
        share=False
    )


# if __name__ == "__main__":
#     launch_app()
