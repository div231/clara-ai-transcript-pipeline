import streamlit as st
import json
import os

BASE_PATH = "outputs/accounts"


def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None


st.title("Clara AI Account Configuration Viewer")

# Get available accounts
accounts = os.listdir(BASE_PATH)

account = st.selectbox("Select Account", accounts)

versions_path = os.path.join(BASE_PATH, account)

versions = [v for v in os.listdir(versions_path) if v.startswith("v")]

version = st.selectbox("Select Version", sorted(versions))

memo_path = os.path.join(BASE_PATH, account, version, "memo.json")
agent_path = os.path.join(BASE_PATH, account, version, "agent.json")
changes_path = os.path.join(BASE_PATH, account, "changes.json")

memo = load_json(memo_path)
agent = load_json(agent_path)
changes = load_json(changes_path)

st.header("Account Memo")

if memo:
    st.json(memo)
else:
    st.warning("Memo not found")

st.header("Agent Configuration")

if agent:
    st.json(agent)
else:
    st.warning("Agent config not found")

st.header("Changes")

if changes:
    st.json(changes)
else:
    st.info("No changes file found")