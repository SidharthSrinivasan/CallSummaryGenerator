from transformers import pipeline
import torch

def load_summarizer(model_name="mistralai/Mistral-7B-Instruct-v0.2", dtype=torch.float16, device=0):
    """
    Load and return the summarizer pipeline for text generation.
    Args:
        model_name: Name of the Hugging Face model to use.
        dtype: Torch data type (default: float16 for GPU).
        device: Device index (default: 0 for first GPU).
    Returns:
        Hugging Face pipeline object for text generation.
    """
    return pipeline(
        "text-generation",
        model=model_name,
        torch_dtype=dtype,
        device=device
    )

def build_prompt(transcript: str) -> str:
    """
    Build the prompt for the LLM based on the transcript.
    Args:
        transcript: The call transcript as a string.
    Returns:
        The formatted prompt string for the LLM.
    """
    return f"""
You are an AI call center assistant. Extract key information from the transcript below and return it as a JSON object. Do not include any explanation or repeated instructions—just valid JSON.

Use the following format:
{{
  "call_info": {{
    "customer_name": <customer name>,
    "agent_name": <agent name>,
    "date": <call date if available>,
    "duration": <estimated duration if available>
  }},
  "conversation_highlights": [
    <exact problem explained by customer>,
    <brief highlight 1>,
    <brief highlight 2>,
    ...
  ],
  "action_items": [
    {{
      "task": <task>,
      "assigned_to": <person/team>,
      "due": <due date if mentioned>
    }}
  ]
}}

Transcript:
{transcript}
"""

def extract_last_json(text: str) -> str:
    """
    Extracts the last complete JSON object from the provided text.
    Args:
        text: The string containing JSON objects.
    Returns:
        The last complete JSON object as a string.
    Raises:
        ValueError: If no JSON object is found.
    """
    brace_count = 0
    start = None
    json_blocks = []
    for i, char in enumerate(text):
        if char == '{':
            if brace_count == 0:
                start = i
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0 and start is not None:
                json_blocks.append(text[start:i+1])
                start = None
    if not json_blocks:
        raise ValueError("No JSON object found in the response.")
    return json_blocks[-1]

def summarize_transcript(summarizer, transcript: str) -> dict:
    """
    Generate summary JSON from transcript using the LLM pipeline.
    Args:
        summarizer: The loaded Hugging Face pipeline for text generation.
        transcript: The call transcript as a string.
    Returns:
        Parsed summary as a Python dictionary.
    Raises:
        json.JSONDecodeError: If the model output is not valid JSON.
    """
    prompt = build_prompt(transcript)
    response = summarizer(prompt, max_new_tokens=512, do_sample=False)
    generated_text = response[0]["generated_text"]
    json_str = extract_last_json(generated_text)
    import json
    return json.loads(json_str)
