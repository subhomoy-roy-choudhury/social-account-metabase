import time
import json
import random
import requests
import arxiv
from llm_app.utils import run_summerise_text
from llm_app.prompt_templates import RESEARCH_PAPER_TWEETS_PROMPT_TEMPLATE


def check_twitter_text_length(text):
    """Checks if a text exceeds the 300 character limit for Twitter.

    Args:
      text: The text to check.

    Returns:
      True if the text exceeds the 300 character limit, False otherwise.
    """

    if len(text) > 300:
        return True
    else:
        return False


def create_tweets(access_token, content):
    """
    Reference :- https://api.twitter.com/2/openapi.json
    """
    url = "https://api.twitter.com/2/tweets"
    tweet_id = None

    payload = json.dumps({"text": content})
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if 200 <= response.status_code <= 299:
        data = response.json()["data"]
        tweet_id = data["id"]
        return tweet_id
    else:
        raise Exception("Error in Twitter create tweets API")


def get_research_paper_tweet_content():
    # Define your search query, author, or category
    search_query = random.choice(
        [
            "large language models",
            "sofware engineering",
            "artificial intelligance",
            "deep learning",
            "Discrete Mathematics",
            "Emerging Technologies"
        ]
    )
    max_results = 200  # Number of results to fetch

    # Search for papers on arXiv
    search = arxiv.Search(
        query=search_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    research_paper_list = list(arxiv.Client().results(search))

    while True:
        # Fetching and printing the papers
        # for paper in arxiv.Client().results(search):
        paper = random.choice(research_paper_list)

        generated_text = run_summerise_text(paper.summary, RESEARCH_PAPER_TWEETS_PROMPT_TEMPLATE)
        formatted_generated_text = format_research_tweet(generated_text, paper.entry_id)
        if not check_twitter_text_length(formatted_generated_text):
            print("Title:", paper.title)
            print("Authors:", ", ".join(author.name for author in paper.authors))
            print("Abstract:", paper.summary)
            print("URL:", paper.entry_id)
            print("PDF URL:", paper.pdf_url)
            print("Published:", paper.published)
            print("----------------------------------------")
            return formatted_generated_text
        time.sleep(2)


def format_research_tweet(text, link):
    hashtags = ["LLMs", "research", "AI", "SoftwareEngineering", "GenerativeAI"]
    tweet = """💡 New paper alert! 🚨\n\n{text}\n\nCheck out the link below to learn more:\n\n🔗 {link}\n\n"""
    tweet += " ".join(["#" + tag for tag in hashtags])

    return tweet.format(**{"text": text, "link": link})
