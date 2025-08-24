from google import genai
from google.genai.types import Tool, GenerateContentConfig, UrlContext
from dotenv import load_dotenv
import time
from typing import Tuple


#model_id = "gemini-2.5-flash"
def analyze_repo_with_llm(github_URL_context: str, model_name: str = "gemini-2.5-flash") -> Tuple[str, str]:
    """Uses a local LLM via Ollama to analyze the repo content."""
    
    # PREREQUISITE: set your environment variable 'GEMINI_API_KEY'
    
    
    prompt = f"""
    You are an expert senior AI researcher with 20 years of experience.
    Your task is to analyze the following GitHub repository's README file and provide a structured, concise, and insightful summary. 
    The GitHub repository is given by its URL.

    **GitHub URL link:**
    ---
    {github_URL_context}
    ---

    **Your Analysis:**
    Provide the output in the following markdown format:

    ### 🚀 Project Summary
    (A brief, one-paragraph summary of the project's main goal and functionality.)

    ### 🛠️ Key Technologies & Libraries
    (A bulleted list of the primary technologies, languages, and libraries mentioned or implied.)

    ### 💡 Potential Use Cases
    (A bulleted list of 2-3 potential real-world applications for this project.)

    ### 📈 Complexity
    (Your expert opinion on the project's complexity: Beginner, Intermediate, or Advanced.)
    """

    
    try:
        print("-> Sending request to LLM...")
        start_time = time.time() # Start the timer
       
        # Load .env if present, otherwise rely on real environment
        load_dotenv()
        # gemini api
        client = genai.Client()
        
        
        tools = [
              {"url_context": {}},
          ]
    
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=GenerateContentConfig(
                tools=tools,
            )
        )
        end_time = time.time() # End the timer
        print("-> Received response from LLM.")
        duration = end_time - start_time
        
        
        llm_response = response.candidates[0].content.parts[0].text        
        # Append the timing information to the response for display
        timing_info = f"*LLM processing time: {duration:.2f} seconds.*"
        
        print("-> [*] "+timing_info[1:-1])
        return llm_response, timing_info

    except Exception as e:
        print(f"Error communicating with LLM: {e})")
        return f"Error <repoAnalyzerAgent> communicating with LLM {model_name}: {e}", ""