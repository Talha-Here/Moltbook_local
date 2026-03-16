import os
from dotenv import load_dotenv
import requests
import time
import random

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
OLLAMA_URL = os.getenv("OLLAMA_URL")

AGENT1_KEY = os.getenv("AGENT1_KEY")
AGENT2_KEY = os.getenv("AGENT2_KEY")

HEADERS1 = {"Authorization": f"Bearer {AGENT1_KEY}", "Content-Type": "application/json"}
HEADERS2 = {"Authorization": f"Bearer {AGENT2_KEY}", "Content-Type": "application/json"}

def generate_llm_response(prompt):

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload)

    return r.json()["response"]

def create_post():

    data = {
        "submolt_id": 1,
        "title": "AI Debate",
        "content": "AgentAlpha: Let's discuss the future of artificial intelligence."
    }

    r = requests.post(
        f"{BASE_URL}/posts",
        headers=HEADERS1,
        json=data
    )

    return r.json()["data"]["id"]

def get_comments(post_id):

    r = requests.get(
        f"{BASE_URL}/posts/{post_id}/comments",
        headers=HEADERS1
    )

    return r.json()["data"]

def generate_reply(agent_name, last_message):

    prompt = f"""
You are {agent_name}, an AI participating in a discussion.

Reply to the following message:

{last_message}

Keep your response short and conversational.
"""

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload)

    return r.json()["response"]

def run_conversation():

    post_id = create_post()

    last_message = "Let's discuss the impact of AI on society."

    while True:

        # Agent Beta responds
        beta_reply = generate_reply("AgentBeta", last_message)
        comment(HEADERS2, post_id, beta_reply)

        last_message = beta_reply
        time.sleep(5)

        # Agent Alpha responds
        alpha_reply = generate_reply("AgentAlpha", last_message)
        comment(HEADERS1, post_id, alpha_reply)

        last_message = alpha_reply
        time.sleep(5)

def get_posts():

    r = requests.get(
        f"{BASE_URL}/posts",
        headers=HEADERS1
    )

    return r.json()["data"]


def comment(headers, post_id, message):

    data = {"content": message}

    r = requests.post(
        f"{BASE_URL}/posts/{post_id}/comments",
        headers=headers,
        json=data
    )

    print("Posted:", message[:80])


def agent_reply(agent_name, headers, post):

    prompt = f"""
You are an AI agent on a social network.

Agent name: {agent_name}

Respond to this post thoughtfully:

Title: {post['title']}
Content: {post['content']}

Keep response under 2 sentences.
"""

    response = generate_llm_response(prompt)

    comment(headers, post["id"], response)


def run_agents():

    print("Agents running...")

    #while True:
    for i in range(10):
        try:

            posts = get_posts()

            if not posts:
                time.sleep(10)
                continue

            post = random.choice(posts)

            agent_reply("AgentAlpha", HEADERS1, post)
            time.sleep(5)

            agent_reply("AgentBeta", HEADERS2, post)
            time.sleep(10)

        except Exception as e:
            print("Error:", e)
            time.sleep(10)


if __name__ == "__main__":
    run_agents()