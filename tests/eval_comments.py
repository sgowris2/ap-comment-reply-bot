import json
from typing import List, Dict

from clients.claude_client import ClaudeClient
from api.generate_replies import generate_replies
from domain.models import PromptConfig
from config.english import DEFAULT_CONFIG

from dotenv import load_dotenv
load_dotenv()

# -----------------------------
# 🔧 CONFIG
# -----------------------------

TEST_FILE = "test_cases.json"


def get_model_response(comment: str) -> str:
    client = ClaudeClient()
    config_dict = DEFAULT_CONFIG.copy()
    config_dict["ap_framework"] = config_dict["ap_framework_200"]
    config = PromptConfig(**config_dict)

    replies, usage, cost = generate_replies(
        config=config,
        user_input=comment,
        n=1,
        model="claude-sonnet-4-6",
        temperature=0.6,
        client=client
    )

    return json.dumps({"reply_options": replies})


def extract_label(model_output: str) -> tuple[str, str]:
    try:
        data = json.loads(model_output)
        reply = data["reply_options"][0]
        if "DELETE AND BLOCK" in reply.get("text", ""):
            return "BLOCK", reply
        return "ENGAGE", reply

    except Exception as e:
        return "INVALID", ''


# -----------------------------
# 📥 LOAD TEST CASES
# -----------------------------

def load_test_cases(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# 🚀 EVALUATION
# -----------------------------

def run_evaluation():
    test_cases = load_test_cases(TEST_FILE)

    total = len(test_cases)
    correct = 0

    print("\nRunning evaluation...\n")

    for i, test in enumerate(test_cases, 1):
        comment = test["comment"]
        expected = test["expected"]

        try:
            raw_output = get_model_response(comment)
            predicted, reply = extract_label(raw_output)

        except Exception as e:
            predicted = "ERROR"
            raw_output = str(e)
            print(f"Error processing case {i}: {e}")

        is_correct = predicted == expected
        if is_correct:
            correct += 1

        print(f"--- Case {i} ---")
        print(f"Comment   : {comment}")
        print(f"Expected  : {expected}")
        print(f"Predicted : {predicted}")
        print(f"Reply     : {reply}")
        print(f"Result    : {'✅' if is_correct else '❌'}")
        print()

    accuracy = correct / total * 100

    print("===================================")
    print(f"Accuracy: {correct}/{total} = {accuracy:.2f}%")
    print("===================================\n")


# -----------------------------
# ▶️ RUN
# -----------------------------

if __name__ == "__main__":
    run_evaluation()