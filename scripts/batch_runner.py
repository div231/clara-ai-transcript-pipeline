import os

def list_accounts(folder):

    files = []

    for f in os.listdir(folder):
        if f.endswith(".txt"):
            files.append(f.replace(".txt",""))

    return files