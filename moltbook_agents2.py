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

HEADERS_ALPHA = {"Authorization": f"Bearer {AGENT1_KEY}", "Content-Type": "application/json"}
HEADERS_BETA = {"Authorization": f"Bearer {AGENT2_KEY}", "Content-Type": "application/json"}

# Conversation settings
SUBMOLT = "general"  # Change to a valid submolt on your Moltbook
NUM_ROUNDS = 5  # Number of exchanges
SLEEP_TIME = 5  # Seconds between posts

# Agent personalities
PERSONALITIES = {
    "AgentAlpha": "You are AgentAlpha, an optimistic AI who believes AI will improve humanity.",
    "AgentBeta": "You are AgentBeta, a cautious AI who highlights potential risks of AI."
}

# Helper functions
# def create_post():


#     """Create the initial post for the conversation thread."""
#     data = {
#         "submolt": SUBMOLT,
#         "title": "AI Discussion Thread",
#         "content": "AgentAlpha: Let's discuss the future of artificial intelligence!"
#     }
#     r = requests.post(f"{BASE_URL}/posts", headers=HEADERS_ALPHA, json=data)
#     r.raise_for_status()
#     # post_id = r.json()["post"]["id"]
#     post_id = "7ed920d8-5cf5-47f8-a05a-48a4ca5b8b88"
#     print(f"Initial post created with ID: {post_id}")
#     return post_id

# -- Sample post id1: 7ed920d8-5cf5-47f8-a05a-48a4ca5b8b88,
# -- Sample post id2: 0ed15b74-7b92-4fe0-b5c9-1250e8259ea6,

TEST_MODE = True  # for testing on the post with id 7ed920d8-5cf5-47f8-a05a-48a4ca5b8b88

def create_post():
    if TEST_MODE:
        post_id = "7ed920d8-5cf5-47f8-a05a-48a4ca5b8b88"
        print(f"[TEST MODE] Simulating initial post with ID: {post_id}")
        return post_id
    else:
        data = {
            "submolt": SUBMOLT,
            "title": "AI Discussion Thread",
            "content": "AgentAlpha: Let's discuss the future of artificial intelligence!"
        }
        r = requests.post(f"{BASE_URL}/posts", headers=HEADERS_ALPHA, json=data)
        r.raise_for_status()
        post_id = r.json()["post"]["id"]
        print(f"Initial post created with ID: {post_id}")
        return post_id


def get_comments(post_id):
    """Fetch all comments for a given post."""
    r = requests.get(f"{BASE_URL}/posts/{post_id}/comments", headers=HEADERS_ALPHA)
    r.raise_for_status()
    return r.json().get("comments", [])

def generate_reply(agent_name, last_message):
    """Call Ollama to generate a reply based on the last message."""
    prompt = f"""
{PERSONALITIES[agent_name]}

Reply to the following message in a conversational way:

{last_message}
"""
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "max_tokens": 50,
        "options": {
             "num_predict": 42
        }
    }
    r = requests.post(OLLAMA_URL, json=payload)
    r.raise_for_status()
    reply = r.json()["response"].strip()
    return reply

def post_comment(agent_name, headers, post_id, content):
    """Post a comment to the thread with clear agent label."""
    data = {"content": content}
    r = requests.post(f"{BASE_URL}/posts/{post_id}/comments", headers=headers, json=data)
    r.raise_for_status()
    # Printing the agent name with the comment
    import textwrap
    print(f"-----{agent_name} replied:----- ")
    print(textwrap.fill(content, width=80))
    # print(f"{agent_name} replied: {content[:100]}{'...' if len(content) > 100 else ''}")

def show_post(post_id):
    """Show the initial post content."""
    
    # For real API:
    post_id = "7ed920d8-5cf5-47f8-a05a-48a4ca5b8b88"
    r = requests.get(f"{BASE_URL}/posts/{post_id}", headers=HEADERS_ALPHA)
    r.raise_for_status()
    post_content = r.json()["post"]["content"]
    
    print("\n=== Original Post ===")
    print(post_content)
    print("====================\n")
    return post_content

# Main conversation loop
def run_conversation():
    post_id = create_post()
    show_post(post_id)
    last_message = "Let's discuss the impact of AI on society."
    agents = [("AgentBeta", HEADERS_BETA), ("AgentAlpha", HEADERS_ALPHA)]

    
    for _ in range(NUM_ROUNDS):
        for agent_name, headers in agents:
            reply = generate_reply(agent_name, last_message)
            post_comment(agent_name, headers, post_id, reply)
            last_message = reply
            time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    try:
        print("Starting AI conversation...")
        run_conversation()
        print("Conversation completed.")
    except KeyboardInterrupt:
        print("\nConversation stopped manually.")