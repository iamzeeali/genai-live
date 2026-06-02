uvicorn main:app --reload
# Few-shot
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "The product broke after one day.", "mode": "few-shot"}'

# CoT
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "If I have 3 apples and give away 1, then buy 5 more, how many do I have?", "mode": "cot"}'

# ReAct
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the capital of Japan?", "mode": "react"}'