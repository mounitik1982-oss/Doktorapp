import re
import requests

OPENFDA_ENDPOINT = "https://api.fda.gov/drug/label.json"

def fetch_drug_info(generic_name):
    """
    Calls OpenFDA API to fetch drug label information.
    Returns dict with uses and warnings or None if not found.
    """
    try:
        params = {
            'search': f'openfda.generic_name:"{generic_name}"',
            'limit': 1
        }
        resp = requests.get(OPENFDA_ENDPOINT, params=params, timeout=5)
        data = resp.json()
        results = data.get('results')
        if not results:
            return None
        label = results[0]
        uses = label.get('indications_and_usage', ["N/A"])[0]
        warnings = label.get('warnings', ["N/A"])[0]
        return {
            'name': generic_name,
            'uses': uses,
            'warnings': warnings
        }
    except Exception as e:
        return {'error': str(e)}

def analyze_text(text):
    """
    Parses OCR text for drug names and dosages.
    Fetches drug info for each found item and formats output.
    """
    lines = text.splitlines()
    drugs = []
    pattern = re.compile(r'([A-Za-z]+)\s+(\d+\s?(mg|ml|tablets?))', re.IGNORECASE)

    for line in lines:
        match = pattern.search(line)
        if not match:
            continue
        name = match.group(1)
        dosage = match.group(2)
        info = fetch_drug_info(name)
        if info and 'error' not in info:
            drugs.append({
                'name': info['name'],
                'dosage': dosage,
                'uses': info['uses'],
                'warnings': info['warnings']
            })
        else:
            drugs.append({
                'name': name,
                'dosage': dosage,
                'uses': 'Info not found',
                'warnings': 'N/A'
            })

    if not drugs:
        return "No drugs detected in the text."

    output = []
    for d in drugs:
        block = (
            f"Drug: {d['name']}\n"
            f"Dosage: {d['dosage']}\n"
            f"Usage: {d['uses']}\n"
            f"Warnings: {d['warnings']}"
        )
        output.append(block)
    return "\n\n".join(output)
