#!/usr/bin/env python
"""
Simple launcher for the Gradio plagiarism detection app
"""

import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and launch the app
from ai_content_plagiarism_detection.gradio_app import launch_app

if __name__ == "__main__":
    print("🚀 Starting Plagiarism Detection Web Interface...")
    print("🌐 Open your browser to: http://localhost:7860")
    
    launch_app()