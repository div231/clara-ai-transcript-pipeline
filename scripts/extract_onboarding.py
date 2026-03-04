import re
import json


def clean_text(text):
    text = text.lower()
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text


def extract_updates(transcript):

    text = transcript.lower()
    updates = {}

    # EMAILS
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", transcript)
    if emails:
        updates["emails"] = list(set(emails))

    # PHONES
    phones = re.findall(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", transcript)
    if phones:
        updates["phone_numbers"] = list(set(phones))

    # PRICING
    prices = re.findall(r"\$\d+", transcript)
    if prices:
        updates["pricing_mentions"] = prices

    # BUSINESS HOURS
    hours = re.search(
        r"(\d{1,2}[:.]?\d{0,2}\s?(?:am|pm))\s*(?:to|-|–)\s*(\d{1,2}[:.]?\d{0,2}\s?(?:am|pm))",
        text,
    )

    if hours:
        updates["business_hours"] = f"{hours.group(1)} - {hours.group(2)}"

    # SOFTWARE / CRM
    tools = ["jobber", "quickbooks", "servicetitan", "housecall", "service fusion"]
    integrations = [t for t in tools if t in text]

    if integrations:
        updates["integration_constraints"] = integrations

    return updates

def update_memo(memo_v1, updates):

    memo_v2 = memo_v1.copy()

    for key, value in updates.items():
        memo_v2[key] = value

    memo_v2["notes"] = "Updated from onboarding transcript"

    return memo_v2
def extract_onboarding_updates(transcript):
    transcript = clean_text(transcript)
    updates = extract_updates(transcript)
    return updates


if __name__ == "__main__":

    ONBOARD_PATH = "dataset/onboarding_calls/account.txt"
    MEMO_V1_PATH = "outputs/accounts/account/v1/memo.json"
    OUTPUT_PATH = "outputs/accounts/account/v2/memo.json"

    # read onboarding transcript
    with open(ONBOARD_PATH, "r", encoding="utf-8") as f:
        transcript = f.read()

    transcript = clean_text(transcript)

    updates = extract_updates(transcript)

    # load memo v1
    with open(MEMO_V1_PATH) as f:
        memo_v1 = json.load(f)

    # update memo
    memo_v2 = update_memo(memo_v1, updates)

    # save memo v2
    with open(OUTPUT_PATH, "w") as f:
        json.dump(memo_v2, f, indent=4)

    print("memo_v2.json generated")