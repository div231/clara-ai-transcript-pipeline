from pathlib import Path

def generate_agent_spec(memo, version="v1"):

    template = Path("templates/agent_prompt.txt").read_text()

    # Convert every None value to empty string
    clean_memo = {k: ("" if v is None else v) for k, v in memo.items()}

    prompt = template

    for key, value in clean_memo.items():
        prompt = prompt.replace(f"{{{{{key}}}}}", str(value))

    company_name = clean_memo.get("company_name") or "Unknown"

    return {
        "agent_name": f"{company_name} Dispatcher",
        "version": version,
        "system_prompt": prompt,
        "voice_style": "professional"
    }