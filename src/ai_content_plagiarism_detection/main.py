#!/usr/bin/env python
import sys
import warnings

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
    inputs = {
        'input': "Artificial intelligence is a branch of computer science that aims to create intelligent machines. These systems can perform tasks that typically require human intelligence, such as visual perception, speech recognition, decision-making, and language translation. Machine learning, a subset of AI, enables computers to learn and improve from experience without being explicitly programmed. Deep learning, which uses neural networks with multiple layers, has revolutionized fields like image recognition and natural language processing. AI has applications in healthcare, finance, transportation, and entertainment, transforming how we live and work.",
    }
    try:
        result = AiContentPlagiarismDetection().crew().kickoff(inputs=inputs)
        print(f"Crew run completed successfully at {datetime.now()}.")
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


# if __name__ == "__main__":
#     run()

    
