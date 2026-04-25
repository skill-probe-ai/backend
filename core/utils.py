import json
import re

def safe_parse_json(data):
    # already parsed
    if isinstance(data, (dict, list)):
        return data

    if not isinstance(data, str):
        return None

    # remove markdown
    data = re.sub(r"```json|```", "", data).strip()

    # direct parse
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        pass

    # extract JSON object or array
    match = re.search(r'(\{[\s\S]*?\}|\[[\s\S]*?\])', data)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return None