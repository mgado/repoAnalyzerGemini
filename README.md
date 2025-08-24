# 🤖 GitHub Repo Analyzer Agent (version with google urlcontext + gemini api )

This tool uses the Google Gemini API to analyze GitHub repositories.
## 🛠️ Setup
### Prerequisites
- Python 3.9+
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey).
### Installation
- **macOS/Linux:** `./setup.sh`
- **Windows:** `pip install -r requirements.txt`
## 🚀 How to Run
- **UI:** `cd repo_analyzer_agent; python app_core.py`
- **CLI:** `export GEMINI_API_KEY="YOUR_API_KEY"`, `cd repo_analyzer_agent` followed by `python app_core.py --url <URL> --model <gemini_model_name>`

📚Example: 
```bash
cd repo_analyzer_agent
python app_core.py --url https://github.com/huggingface/transformers --model gemini-2.5-flash
```
