import json


def generate_diff(v1, v2):

    changes = []

    keys = set(v1.keys()).union(set(v2.keys()))

    for key in keys:

        val1 = v1.get(key)
        val2 = v2.get(key)

        if val1 != val2:

            changes.append(
                f"{key} changed from {val1} → {val2}"
            )

    return changes


if __name__ == "__main__":

    with open("memo_v1.json") as f:
        memo_v1 = json.load(f)

    with open("memo_v2.json") as f:
        memo_v2 = json.load(f)

    changes = generate_diff(memo_v1, memo_v2)

    with open("changelog.txt", "w") as f:

        for c in changes:
            f.write(c + "\n")

    print("changelog.txt generated")