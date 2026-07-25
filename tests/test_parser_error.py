from agents.patient_understanding.parser import parse_response

raw = """
{
    "clinical_summary": "Missing closing brace"
"""

parse_response(raw)