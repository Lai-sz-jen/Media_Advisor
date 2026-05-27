import os
from dotenv import load_dotenv
import json
from google import genai
from google.genai import types

def evaluate(environment: str, job: str, feedback: str) -> str|None:
    ## Initialize
    # This line reads your .env file and hides your key in the background
    load_dotenv()

    # You don't need to pass the key here anymore; the client finds it automatically!
    client = genai.Client()
    model_name = "gemini-2.5-flash"


    ## Get user input
    # This is the specific scenario you want the system to evaluate
    test_case :dict = {
        "environment": environment,
        "job": job,
        "feedback": feedback
    }

    user_scenario :str = json.dumps(test_case)

    ## Get the rules
    with open("rules.txt", "r", encoding="utf-8") as file:
        expert_rules: str = file.read()
    instruction = ("""
                   You are a strict deterministic inference engine. 
                   Your ONLY job is to evaluate the user's JSON scenario against the following rulebase. 
                   1. Apply the rules strictly using forward-chaining logic. 
                   2. Never guess, invent, or use outside knowledge. 
                   3. Always return the answer in json format '{"medium": your-answer, "logic": [rules-used as int]}'.
                   4. If the provided facts do not trigger a specific rule, your answer should be 'INSUFFICIENT DATA'.\n\n"""
                   f"--- RULEBASE START ---\n{expert_rules}\n--- RULEBASE END ---"
                   )


    ## Evaluate scenario
    print("Evaluating scenario against rules...")
    response = client.models.generate_content(
        model=model_name,
        contents=user_scenario,
        config=types.GenerateContentConfig(
            system_instruction=instruction,
            temperature=0.0,           # CRITICAL: Forces logical, strict adherence
        )
    )

    ## Output
    print("Evaluation successful!")
    return response.text

if __name__ == "__main__":
    resp: str|None = evaluate("machines", "repairing", "required")
    print(resp)
