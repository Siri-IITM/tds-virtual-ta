import requests
import json
import time

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_SLUG = "tools-in-data-science"

def get_topics(category_id=60):  # Use actual category ID or find via /categories.json
    url = f"{BASE_URL}/c/{CATEGORY_SLUG}/{category_id}.json"
    r = requests.get(url)
    topics = r.json()["topic_list"]["topics"]
    return topics

def get_posts(topic_id):
    url = f"{BASE_URL}/t/{topic_id}.json"
    r = requests.get(url)
    return r.json()

def scrape():
    topics = get_topics()
    posts = []
    for topic in topics:
        topic_id = topic["id"]
        full_topic = get_posts(topic_id)
        posts.append({
            "title": full_topic["title"],
            "posts": [post["cooked"] for post in full_topic["post_stream"]["posts"]]
        })
        time.sleep(1)  # Avoid rate limiting

    with open("discourse_data.json", "w") as f:
        json.dump(posts, f, indent=2)

if __name__ == "__main__":
    scrape()
