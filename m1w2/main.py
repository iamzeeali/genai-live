# main.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Request/Response schemas ---


class PromptRequest(BaseModel):
    text: str
    mode: str  # "few-shot" | "cot" | "react"


class AnalysisResponse(BaseModel):
    mode: str
    result: str

# --- Mode builders ---


def build_few_shot_messages(text: str) -> list:
    return [
        {"role": "system", "content": "Classify the sentiment as positive, negative, or neutral."},
        {"role": "user", "content": "I love this product!"},
        {"role": "assistant", "content": "positive"},
        {"role": "user", "content": "This is absolutely terrible."},
        {"role": "assistant", "content": "negative"},
        {"role": "user", "content": "It arrived on time."},
        {"role": "assistant", "content": "neutral"},
        {"role": "user", "content": text},  # actual query
    ]


def build_cot_messages(text: str) -> list:
    return [
        {"role": "system", "content": "Think step by step before giving your final answer."},
        {"role": "user", "content": text},
    ]


def build_react_messages(text: str) -> list:
    # Simulate a ReAct loop with a mock tool result
    return [
        {"role": "system", "content": """You are a helpful assistant that reasons step by step.
Use this format:
Thought: <your reasoning>
Action: <tool to call, e.g. search("query")>
Observation: <tool result>
... repeat if needed ...
Final Answer: <your answer>"""},
        {"role": "user", "content": text},
        # Simulate an observation from a mock tool
        {"role": "assistant",
            "content": 'Thought: I need to search for this.\nAction: search("' + text + '")'},
        {"role": "user",
            "content": "Observation: Here is a relevant result: [mock search result for: " + text + "]"},
    ]

# --- Main endpoint ---


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(req: PromptRequest):
    print('req', req)
    if req.mode == "few-shot":
        messages = build_few_shot_messages(req.text)
    elif req.mode == "cot":
        messages = build_cot_messages(req.text)
    elif req.mode == "react":
        messages = build_react_messages(req.text)
    else:
        return AnalysisResponse(mode=req.mode, result="Unknown mode")

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
    )

    return AnalysisResponse(
        mode=req.mode,
        result=response.choices[0].message.content
    )
