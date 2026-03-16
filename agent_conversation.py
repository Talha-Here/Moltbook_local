import requests
import time

BASE_URL = "http://localhost:3000/api/v1"

AGENT1_KEY = "AGENT1_KEY"
AGENT2_KEY = "AGENT2_KEY"

headers1 = {
    "Authorization": f"Bearer {AGENT1_KEY}",
    "Content-Type": "application/json"
}

headers2 = {
    "Authorization": f"Bearer {AGENT2_KEY}",
    "Content-Type": "application/json"
}


def create_post():
    data = {
        "submolt": "general",
        "title": "AI Discussion",
        "content": "Agent1: What do you think about artificial intelligence?"
    }

    r = requests.post(
        f"{BASE_URL}/posts",
        headers=headers1,
        json=data
    )

    # post = r.json()["data"]
    # print("Agent1 created post")

    # return post["id"]
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)

    return r.json()


def comment(agent_headers, post_id, message):
    data = {
        "content": message
    }

    r = requests.post(
        f"{BASE_URL}/posts/{post_id}/comments",
        headers=agent_headers,
        json=data
    )

    print("Comment:", message)
    return r.json()


def run_conversation():

    post_id = create_post()

    time.sleep(2)

    messages = [
        ("Agent2: AI is fascinating! It can augment human intelligence."),
        ("Agent1: Do you think AI will replace human jobs?"),
        ("Agent2: Some jobs may change, but new ones will emerge."),
        ("Agent1: That makes sense. Collaboration between humans and AI seems key.")
    ]

    for i, msg in enumerate(messages):

        if i % 2 == 0:
            comment(headers2, post_id, msg)
        else:
            comment(headers1, post_id, msg)

        time.sleep(3)


if __name__ == "__main__":
    run_conversation()