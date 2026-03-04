import re
import json

def clean_text(text):
    text = text.lower()
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text


def extract_structured(text):
    data = {}

    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    if emails:
        data["emails"] = list(set(emails))

    phones = re.findall(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", text)
    if phones:
        data["phone_numbers"] = list(set(phones))

    prices = re.findall(r"\$\d+", text)
    if prices:
        data["pricing_mentions"] = prices

    hours_pattern = r"\b(\d{1,2}(?::\d{2})?\s?(?:am|pm))\s*(?:to|-|–)\s*(\d{1,2}(?::\d{2})?\s?(?:am|pm))"

    match = re.search(hours_pattern, text, re.I)

    if match:
        start = match.group(1)
        end = match.group(2)
        data["business_hours"] = f"{start} - {end}"
    return data


def extract_semantic(text):

    data = {}

    # SOFTWARE / CRM DETECTION
    integrations = [
        "jobber",
        "quickbooks",
        "servicetitan",
        "housecall",
        "service fusion"
    ]

    found_integrations = [tool for tool in integrations if tool in text]

    if found_integrations:
        data["integration_constraints"] = found_integrations


    # SERVICE DETECTION
    service_words = [
        "install", "installation", "repair", "maintenance",
        "service", "wiring", "electrical", "panel",
        "charger", "generator", "lighting", "troubleshooting"
    ]

    services = [w for w in service_words if w in text]

    if services:
        data["services_supported"] = list(set(services))


    # EMERGENCY RULES
    if "emergency" in text:
        data["emergency_definition"] = [
            "Emergency calls mentioned in transcript"
        ]


    # AFTER HOURS FLOW
    if "after hours" in text:
        data["after_hours_flow_summary"] = \
            "AI should capture call details and escalate if emergency"


    # OFFICE HOURS FLOW
    if "call" in text and "schedule" in text:
        data["office_hours_flow_summary"] = \
            "AI collects caller info and schedules service visit"


    # CALL TRANSFER RULES
    if "transfer" in text or "call me directly" in text:
        data["call_transfer_rules"] = \
            "Certain calls may transfer directly to business owner"


    return data

def detect_company(text):

    patterns = [
        r"[A-Za-z]+['’]s Electric Solutions",
        r"[A-Za-z]+ Electric Solutions",
        r"[A-Za-z]+ Electrical Services",
        r"[A-Za-z]+ Electric"
    ]

    for p in patterns:
        match = re.search(p, text, re.I)
        if match:
            return match.group(0).title()

    return None


def extract_demo(transcript, account_id):

    text = clean_text(transcript)

    memo = {
        "account_id": account_id,
        "company_name": None,
        "business_hours": None,
        "office_address": None,
        "services_supported": [],
        "emergency_definition": [],
        "emergency_routing_rules": None,
        "non_emergency_routing_rules": None,
        "call_transfer_rules": None,
        "integration_constraints": None,
        "after_hours_flow_summary": None,
        "office_hours_flow_summary": None,
        "questions_or_unknowns": [],
        "notes": "Generated from demo transcript"
    }

    structured = extract_structured(text)
    semantic = extract_semantic(text)
    memo.update(structured)
    memo.update(semantic)

    company = detect_company(text)

    if company:
        memo["company_name"] = company

    if "services_supported" in semantic:
        memo["services_supported"] = semantic["services_supported"]

    if "integrations" in semantic:
        memo["integration_constraints"] = semantic["integrations"]

    if "business_hours" in structured:
        memo["business_hours"] = structured["business_hours"]

    if not memo["business_hours"]:
        memo["questions_or_unknowns"].append("Business hours not confirmed")

    return memo


if __name__ == "__main__":

    DEMO_PATH = "dataset/demo_calls/account.txt"
    OUTPUT_PATH = "outputs/accounts/account/v1/memo.json"

    with open(DEMO_PATH, "r", encoding="utf-8") as f:
        transcript = f.read()

    memo_v1 = extract_demo(transcript)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(memo_v1, f, indent=4)

    print("memo_v1.json generated")