from gnews import GNews
import openai
import random
from datetime import datetime
from linkedin.constants import (
    ALLOWED_AUTOMATION_TIP_OF_THE_DAY,
    FUN_FACTS,
    ALLOWED_SEARCH_KEYS,
    EXCLUDE_WEBSITES,
    BOLD_CHARS,
    RELEVANT_HASHTAGS,
)
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


def count_tokens(text):
    # Simple tokenization using split (doesn't handle punctuation well)
    tokens = text.split()
    number_of_tokens = len(tokens)
    return number_of_tokens


def get_article(
    search_key, country="US", period="1d", max_results=1, exclude_websites=[]
):
    start = True
    content = ""
    while start or count_tokens(content) > 3000:
        start = False
        google_news = GNews(
            language="en",
            country=country,
            period=period,
            max_results=int(max_results),
            exclude_websites=exclude_websites,
        )
        news = google_news.get_news(search_key)
        if len(news) > 0:
            article = google_news.get_full_article(news[0]["url"])
            content = article.text
        else :
            start = True

    return article


def generate_summarizer(
    max_tokens,
    temperature,
    top_p,
    frequency_penalty,
    prompt,
    person_type,
):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=int(max_tokens),
        temperature=float(temperature),
        top_p=float(top_p),
        frequency_penalty=float(frequency_penalty),
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant for text summarization.",
            },
            {
                "role": "user",
                "content": f"Summarize this for a {person_type} within 20 words: {prompt}",
            },
        ],
    )
    return res["choices"][0]["message"]["content"]


def to_bold_text(input_text):
    return "".join(BOLD_CHARS.get(c, c) for c in input_text)


def format_linkedin_post(data):
    # Formatting the news using the template
    formatted_news = (
        f"🚀 {to_bold_text('[TechFlash]: Your Weekly Software & Tech Update')}!\n\n"
    )
    formatted_news += f"📅 Date: {datetime.now().strftime('%B %d, %Y')}\n\n"  # Change this to the current date

    for heading, article in data.items():
        title = article["title"]
        description = article["summary"]
        url = article["url"]

        formatted_news += f"{to_bold_text(heading)}:\n"
        formatted_news += f"📰 {to_bold_text(title)}\n"
        formatted_news += f"Brief Summary: {description}\n"
        formatted_news += f"🔗 {url}\n\n"

    # Add any additional information you like, such as the 'Did You Know?' section
    automation_tip = random.choice(list(ALLOWED_AUTOMATION_TIP_OF_THE_DAY.values()))
    fun_fact = random.choice(list(FUN_FACTS.values()))
    formatted_news += f"🧐 {to_bold_text('Did You Know?')}\n{fun_fact}\n\n"
    formatted_news += (
        f"🤖 {to_bold_text('Automation Tip of the Week')}:\n{automation_tip}\n\n"
    )
    formatted_news += "---\n\n"
    formatted_news += f"💡 {to_bold_text('Share & Discuss!')}\nWhich news excites you the most? Drop your thoughts below!\n\n"
    formatted_news += " ".join(["#" + tag for tag in RELEVANT_HASHTAGS])

    return formatted_news


def get_linkedin_post():
    daily_article_data = {}
    for key, value in ALLOWED_SEARCH_KEYS.items():
        # Get a random string from the list
        random_string = random.choice(value)
        article = get_article(
            random_string,
            settings.COUNTRY,
            settings.PERIOD,
            settings.MAX_RESULTS,
            EXCLUDE_WEBSITES,
        )
        summary = generate_summarizer(
            settings.MAX_TOKENS,
            settings.TEMPERATURE,
            settings.TOP_P,
            settings.FREQUENCY_PENALTY,
            prompt=article.text,
            person_type="Linkedin User",
        )
        daily_article_data[key] = {
            "source_url": article.source_url,
            "url": article.url,
            "title": article.title,
            "meta_img": article.meta_img,
            "text": article.text,
            "authors": article.authors,
            "meta_description": article.meta_description,
            "html": article.html,
            "summary": summary,
        }

    linkedin_post_text = format_linkedin_post(daily_article_data)
    return linkedin_post_text
