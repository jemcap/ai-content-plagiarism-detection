#!/usr/bin/env python
import sys
import warnings
import os
import uuid
from pathlib import Path
from datetime import datetime

from ai_content_plagiarism_detection.crew import AiContentPlagiarismDetection

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # Create a unique output directory for this analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    output_dir = f"output/{timestamp}_cli_run_{unique_id}"
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define output paths for this analysis
    text_segments_path = f"{output_dir}/text_segments.json"
    similarity_report_path = f"{output_dir}/similarity_report.md"
    plagiarism_report_path = f"{output_dir}/plagiarism_report.md"
    
    print(f"Analysis output directory: {output_dir}")
    
    sample_text = "Artificial intelligence is a branch of computer science that aims to create intelligent machines. These systems can perform tasks that typically require human intelligence, such as visual perception, speech recognition, decision-making, and language translation. Machine learning, a subset of AI, enables computers to learn and improve from experience without being explicitly programmed. Deep learning, which uses neural networks with multiple layers, has revolutionized fields like image recognition and natural language processing. AI has applications in healthcare, finance, transportation, and entertainment, transforming how we live and work."
    
    inputs = {
        'input': sample_text,
        'file_name': 'sample_text.txt',
        'output_dir': output_dir
    }
    
    try:
        # Create and configure the crew
        crew_instance = AiContentPlagiarismDetection()
        crew = crew_instance.crew()
        
        # Update all task output paths for this analysis using the new method
        crew_instance.update_output_paths(output_dir)
        
        result = crew.kickoff(inputs=inputs)
        print(f"Crew run completed successfully at {datetime.now()}.")
        print(f"Output files are available in: {output_dir}")
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()
