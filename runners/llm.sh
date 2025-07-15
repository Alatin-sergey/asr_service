#!\bin\bash
echo "Starting LLM..."
uvicorn llm_app:app --port ${LLM_PORT} --host ${LLM_HOST}