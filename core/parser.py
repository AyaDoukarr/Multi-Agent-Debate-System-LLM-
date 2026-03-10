import re


def extract_score(block: str, label: str):
    pattern = rf"{label}\s*:\s*([0-9]|10)\s*/\s*10"
    match = re.search(pattern, block, flags=re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0


def parse_judge_scores(judge_text: str):
    result = {
        "POUR": {"Logique": 0, "Clarté": 0, "Persuasion": 0},
        "CONTRE": {"Logique": 0, "Clarté": 0, "Persuasion": 0},
    }

    if "CONTRE" in judge_text:
        parts = re.split(r"\bCONTRE\b", judge_text, maxsplit=1, flags=re.IGNORECASE)
        pour_block = parts[0]
        contre_block = parts[1] if len(parts) > 1 else judge_text
    else:
        pour_block = judge_text
        contre_block = judge_text

    result["POUR"]["Logique"] = extract_score(pour_block, "Logique")
    result["POUR"]["Clarté"] = extract_score(pour_block, "Clarté")
    result["POUR"]["Persuasion"] = extract_score(pour_block, "Persuasion")

    result["CONTRE"]["Logique"] = extract_score(contre_block, "Logique")
    result["CONTRE"]["Clarté"] = extract_score(contre_block, "Clarté")
    result["CONTRE"]["Persuasion"] = extract_score(contre_block, "Persuasion")

    return result