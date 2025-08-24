# simple tests to verify that the core functions of the application are working as expected
import pytest
from gemini_analyzer_with_url_context import analyze_repo_with_llm


def test_analyze_repo_with_llm():
    """
    Tests the LLM analysis function with mock data.
    Note: This test assumes Ollama is running and has a model available.
    For a true unit test, you would mock the ollama.chat call.
    """
    mock_URL = "https://github.com/openai/gpt-oss"
    
    analysis, timing_info = analyze_repo_with_llm(mock_URL, "gemini-2.5-flash")
    
    assert "Error" not in analysis
    assert "Project Summary" in analysis
    assert "seconds" in timing_info
    

def test_analyze_repo_with_llm_invalid_model():
    """
    Tests that the analysis function returns a user-friendly error
    when a non-existent model name is provided.
    """
    mock_URL = "https://github.com/openai/gpt-oss"
    invalid_model = "this-model-does-not-exist-12345"
    
    analysis, timing = analyze_repo_with_llm(mock_URL, invalid_model)
    
    # Check that a clear error message is returned to the user
    assert "Error" in analysis
    assert invalid_model in analysis # The error should mention the invalid model name
