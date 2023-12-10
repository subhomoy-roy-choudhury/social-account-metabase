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
    tweet_id, content = None, None

    payload = json.dumps({"text": content})
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if 200 <= response.status_code <= 299:
        data = response.json()
        tweet_id = data["id"]
        content = data["text"]
    else:
        print("Error in Twitter create tweets API")
    return tweet_id, content


def get_research_paper_tweet_content():
    while True:
        # Define your search query, author, or category
        search_query = random.choice(
            [
                "large language models",
                "generative ai",
                "stable diffusion",
                "general artificial intelligance",
            ]
        )
        max_results = 100  # Number of results to fetch

        # Search for papers on arXiv
        search = arxiv.Search(
            query=search_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
        )

        # Fetching and printing the papers
        # for paper in arxiv.Client().results(search):
        paper = random.choice(list(arxiv.Client().results(search)))

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


def format_research_tweet(text, link):
    hashtags = ["llm", "research", "gai", "ai", "nlp"]
    tweet = """💡 New paper alert! 🚨\n\n{text}\n\nCheck out the link below to learn more:\n\n🔗 {link}\n\n"""
    tweet += " ".join(["#" + tag for tag in hashtags])

    return tweet.format(**{"text": text, "link": link})
