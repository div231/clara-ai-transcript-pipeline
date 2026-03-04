import os
import json

from scripts.extract_demo import extract_demo
from scripts.extract_onboarding import extract_onboarding_updates
from scripts.agent_generator import generate_agent_spec
from scripts.diff_generator import generate_diff
from scripts.logger import logger

logger.info("Processing demo transcript...")

DEMO_FOLDER = "dataset/demo_calls"
ONBOARD_FOLDER = "dataset/onboarding_calls"
OUTPUT_FOLDER = "outputs/accounts"


# ----- DEMO PIPELINE -----

for file in os.listdir(DEMO_FOLDER):

    if not file.endswith(".txt"):
        continue

    account_id = file.replace(".txt", "")

    with open(f"{DEMO_FOLDER}/{file}") as f:
        transcript = f.read()

    memo = extract_demo(transcript, account_id)

    print("DEBUG memo:", memo)

    agent_spec = generate_agent_spec(memo, "v1")

    account_path = f"{OUTPUT_FOLDER}/{account_id}/v1"

    os.makedirs(account_path, exist_ok=True)

    with open(f"{account_path}/memo.json", "w") as f:
        json.dump(memo, f, indent=4)

    with open(f"{account_path}/agent.json", "w") as f:
        json.dump(agent_spec, f, indent=4)


# ----- ONBOARDING PIPELINE -----

for file in os.listdir(ONBOARD_FOLDER):

    if not file.endswith(".txt"):
        continue

    account_id = file.replace(".txt", "")

    with open(f"{ONBOARD_FOLDER}/{file}") as f:
        transcript = f.read()

    updates = extract_onboarding_updates(transcript)

    v1_path = f"{OUTPUT_FOLDER}/{account_id}/v1/memo.json"

    if not os.path.exists(v1_path):
        continue

    with open(v1_path) as f:
        memo = json.load(f)

    updated_memo = memo.copy()
    updated_memo.update(updates)

    agent_v2 = generate_agent_spec(updated_memo, "v2")

    v2_path = f"{OUTPUT_FOLDER}/{account_id}/v2"

    os.makedirs(v2_path, exist_ok=True)

    with open(f"{v2_path}/memo.json", "w") as f:
        json.dump(updated_memo, f, indent=4)

    with open(f"{v2_path}/agent.json", "w") as f:
        json.dump(agent_v2, f, indent=4)

    changes = generate_diff(memo, updated_memo)

    with open(f"{OUTPUT_FOLDER}/{account_id}/changes.json", "w") as f:
        json.dump(changes, f, indent=4)