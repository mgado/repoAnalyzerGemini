# This is the main entry point of the application. Imports other modules, defines the UI, and orchestrate the logic.
import gradio as gr
from typing import Tuple
import argparse
import os

# Import functions from our other modules
from gemini_config import GEMINI_MODEL_LIST
from gemini_analyzer_with_url_context import analyze_repo_with_llm



def analyze_github_repo(url: str, model_name: str, progress = gr.Progress(track_tqdm=True)) -> Tuple[str, str]:
    """The main function that ties everything together for the UI."""
    if not url or not model_name:
        return "Please enter a GitHub repository URL to begin and select a model.", "Please enter a GitHub repository URL to begin and select a model."

    # step 0: start 
    msg_0 = "Initiating github repo analysis..."
    if isinstance(progress, gr.Progress):
        progress(0, desc=msg_0)
    else:
        print(msg_0)


    # Step 1: Analyze with the LLM
    msg_1 = f"Step (1/2) Analyzing content with LLM -> {model_name}..."
    if isinstance(progress, gr.Progress):
        progress(0.5, desc=msg_1)
    else:
        print(msg_1)
    analysis, timing_info = analyze_repo_with_llm(url, model_name)
    #print(timing_info)

    # Step 2: Done
    msg_2 = "Step (2/2) Done!"
    if isinstance(progress, gr.Progress):
        progress(1, desc= msg_2)
    else:
        print(msg_2)
    return analysis, timing_info


def clear_fields():
    """Returns empty values to clear all input and output fields."""
    # Clears: url_input, analysis_output, time_output, model_dropdown
    return "", "", "", GEMINI_MODEL_LIST[0]

def create_ui():
    """Creates the layout and returns the Gradio UI Blocks"""
    with gr.Blocks() as iface:
        gr.Markdown("# 🤖 GitHub Repo Analyzer Agent")
        gr.Markdown("Enter a GitHub repo URL to get an expert analysis from a cloud based LLM (gemini) and using URL context. You need to set up your $GEMINI_API_KEY.")

        with gr.Row():
            with gr.Column(scale=3):
                url_input = gr.Textbox(
                    lines=15,
                    placeholder="e.g., https://github.com/ollama/ollama",
                    label="GitHub Repository URL"
                )
            with gr.Column(scale=1):
                model_dropdown = gr.Dropdown(
                    choices=GEMINI_MODEL_LIST, 
                    value=GEMINI_MODEL_LIST[0], 
                    label="Select or Enter a LLM Model Name",
                    allow_custom_value=True
                )
                submit_btn = gr.Button("Submit", variant="primary")
                stop_btn = gr.Button("Stop", variant="stop")
                clear_btn = gr.Button("Clear")
                time_output = gr.Textbox(label="Processing information", elem_id="time-output")

        with gr.Row():
            analysis_output = gr.Markdown(label="Expert Analysis", elem_id="analysis-output")

        gr.Examples(
            examples=[
                ["https://github.com/openai/gpt-oss"],
                ["https://github.com/facebookresearch/llama"],
                ["https://github.com/huggingface/transformers"],
                ["https://github.com/matlab-deep-learning/llms-with-matlab"],
            ],
            inputs=url_input
        )

        # Event handling
        analysis_event = submit_btn.click(
            fn=analyze_github_repo,
            inputs=[url_input, model_dropdown],
            outputs=[analysis_output, time_output]
        )
        stop_btn.click(fn=None, inputs=None, outputs=None, cancels=[analysis_event])
        clear_btn.click(fn=clear_fields, inputs=None, outputs=[url_input, analysis_output, time_output, model_dropdown])
    
    return iface


def main_cli():
    """Handles the command-line interface logic."""
    parser = argparse.ArgumentParser(description="GitHub Repo Analyzer CLI")
    parser.add_argument("--url", required=True, type=str, help="URL of the GitHub repository to analyze.")
    parser.add_argument("--model", type=str, default=GEMINI_MODEL_LIST[0], help=f"Name of the gemini model to use (default: {GEMINI_MODEL_LIST[0]}).")
    args = parser.parse_args()

    print("--- GitHub Repo Analyzer CLI ---")
   
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not found. Please create a .env file with your key.")
        return    
    
    analysis, timing_info = analyze_github_repo(args.url, args.model, progress=None)
    print("\n--- Analysis Result ---")
    print(analysis)
    print("-----------------------")
    print(f"Processing Time: {timing_info}")
    print("-----------------------")
    
    

if __name__ == "__main__":
    import sys
    # Check if any command-line arguments for the CLI were provided
    if len(sys.argv) > 1 and any(arg.startswith('--') for arg in sys.argv):
        main_cli()
    else:
        # If no CLI arguments, launch the Gradio UI
        app_ui = create_ui()
        print("Launching Gradio Interface...")
        app_ui.launch(debug=True)
