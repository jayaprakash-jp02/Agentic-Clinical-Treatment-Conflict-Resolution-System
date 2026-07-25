from agents.patient_understanding.llm_client import call_model

prompt = """
Return ONLY this JSON:

{
    "message":"hello"
}
"""

response = call_model(prompt)

print(response)