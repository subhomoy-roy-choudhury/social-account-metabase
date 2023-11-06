from gnews import GNews
import openai
import tiktoken
import random
import requests
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
from linkedin.error import NoSuitableArticleFound

# Reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

openai.api_key = settings.OPENAI_API_KEY


def count_tokens(string: str, model_name: str = "gpt-3.5-turbo") -> int:
    """
    Returns the number of tokens in a text string.
    Reference Link := https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    """
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_suitable_article(search_key, google_news):
    news = google_news.get_news(search_key)
    for article_info in news:
        try:
            article = google_news.get_full_article(article_info["url"])
            if article and article.text and count_tokens(article.text) <= 3000:
                return article
        except Exception as error:
            print("Error in get_suitable_article", str(error))


def get_article(
    search_key, country="US", period="1d", max_results=10, exclude_websites=[]
):
    google_news = GNews(
        language="en",
        country=country,
        period=period,
        max_results=int(max_results),
        exclude_websites=exclude_websites,
    )
    try:
        return get_suitable_article(search_key, google_news)
    except NoSuitableArticleFound as e:
        print(e)  # Or any other form of logging you prefer.
        return None


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
        request_timeout=15,
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
        f"🚀 {to_bold_text('[TechFlash]: Your Daily Software & Tech Update')}!\n\n"
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
    MAX_ATTEMPTS = 10
    for key, value in ALLOWED_SEARCH_KEYS.items():
        # Get a random string from the list

        random_string = random.choice(value)
        for _ in range(MAX_ATTEMPTS):
            article = get_article(
                random_string,
                settings.COUNTRY,
                settings.PERIOD,
                settings.MAX_RESULTS,
                EXCLUDE_WEBSITES,
            )
            if article:
                break
        if article is None:
            raise NoSuitableArticleFound(
                "Unable to find a suitable article after several attempts."
            )
        else:
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


def create_linkedin_post(access_token, post_text):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }
    data = {
        "author": "urn:li:person:CTJGCF2Lyd",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    return response.json()


class LinkedinPostPDF(object):
    def __init__(self, filename):
        self.load_font()
        self.canvas = canvas.Canvas(filename)
        self.width, self.height = (500, 500)
        self.canvas.setPageSize((self.width, self.height))

    def wrap_text(self, text, width, font, size):
        """
        Wrap the text to fit within the specified width.
        Returns a list of lines.
        """
        # Set the font you will be using for the size check
        self.canvas.setFont(font, size)
        words = text.split()
        lines = []
        line = ""

        for word in words:
            if self.canvas.stringWidth(line + " " + word, font, size) <= width:
                line += " " + word
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    def draw_wrapped_text(
        self, text, x, y, width, font="Helvetica", size=15, x_leading=50, y_leading=20
    ):
        """
        Draw the wrapped text on the canvas.
        """
        lines = self.wrap_text(text, width, font, size)
        for index, line in enumerate(lines):
            self.canvas.drawString(x, y, line.strip())
            y -= y_leading

        return y

    def load_font(self):
        pdfmetrics.registerFont(TTFont("Symbola", "fonts/Symbola/Symbola_hint.ttf"))
        pdfmetrics.registerFont(TTFont("Futura", "fonts/futura/futur.ttf"))

    def set_background(self):
        left_padding = 0
        bottom_padding = 0
        self.canvas.setFillColor(HexColor("#f9f3ff"))
        self.canvas.rect(left_padding, bottom_padding, self.width, self.height, fill=1)

    def draw_image(self, image_path, x_ccordinate, y_ccordinate, size):
        # Position and size for the image
        x_position = x_ccordinate
        y_position = y_ccordinate  # Adjust to place the image as desired
        image_width = size  # Width of the image on the PDF
        image_height = size  # Height of the image on the PDF

        # Draw the image on the canvas
        self.canvas.drawImage(
            image_path, x_position, y_position, width=image_width, height=image_height
        )

    def initiate_default_page(self):
        # Set Background
        self.set_background()

        # Page Header
        image_path = "images/company_image.png"

        self.draw_image(image_path, self.width - 120, self.height - 40, 20)
        self.canvas.setFillColor(HexColor("#7b56b1"))
        self.canvas.setFont("Futura", 20)
        self.canvas.drawString(self.width - 90, self.height - 40, "Oderna")

        # Page Footer
        self.canvas.setFillColor(HexColor("#7b56b1"))
        self.canvas.setFont("Helvetica", 15)
        self.canvas.drawAlignedString(
            self.width // 2 + 100, 20, "@subhomoy-roy-choudhury", direction="center"
        )
        # Add hyperlink over the text
        url = "https://src-portfolio.oderna.in/"
        self.canvas.linkURL(
            url, (self.width // 2 - 100, 20, self.width // 2 + 100, 30), relative=1
        )

    def front_page(self):
        # Default Page
        self.initiate_default_page()

        # Starting Coordinates
        x_coordinate = self.width // 2 - 125
        y_coordinate = self.height // 2 + 50

        self.canvas.setFillColor(HexColor("#7b56b1"))
        self.canvas.setFont("Symbola", 40)
        self.canvas.drawString(x_coordinate - 30, y_coordinate, "🚀")
        self.canvas.setFont("Helvetica-Bold", 40)
        self.canvas.drawString(x_coordinate + 10, y_coordinate, "TECH FLASH")

        # Line
        self.canvas.setStrokeColor("#d5b8f6")
        self.canvas.line(
            x_coordinate + 70, y_coordinate - 10, x_coordinate + 200, y_coordinate - 10
        )

        self.canvas.setFillColor(HexColor("#7b56b1"))
        self.canvas.setFont("Helvetica", 20)
        self.canvas.drawString(
            x_coordinate - 50,
            y_coordinate - 40,
            "Your Daily Software and Tech Updates!",
        )

        # Date
        self.canvas.setFillColor(HexColor("#6b6671"))
        self.canvas.setFont("Helvetica", 20)
        self.canvas.drawString(
            x_coordinate + 10,
            y_coordinate - 80,
            f"Date :- {datetime.now().strftime('%B %d, %Y')}",
        )

    def next_pages(self, header, content):
        # Default Page
        self.initiate_default_page()

        margin = 30
        x_coordinate = self.width // 2 - 100
        y_coordinate = self.height - 100

        # Heading
        self.canvas.setFillColor(HexColor("#7b56b1"))
        self.canvas.setFont("Helvetica-Bold", 25)
        self.canvas.drawString(x_coordinate, y_coordinate, header)

        # Title
        self.canvas.setFillColor(HexColor("#1a1a1a"))
        next_y = self.draw_wrapped_text(
            content["title"],
            margin,
            y_coordinate - 40,
            self.width - 2 * margin,
            font="Helvetica-Bold",
            size=15,
        )

        # Summary
        self.canvas.setFillColor(HexColor("#1a1a1a"))
        next_y = self.draw_wrapped_text(
            content["summary"],
            margin,
            next_y - 15,
            self.width - 2 * margin,
            font="Helvetica",
            size=15,
        )

        # Link
        self.canvas.setFillColor(HexColor("#3579A6"))
        self.canvas.setFont("Futura", 15)
        self.draw_wrapped_text(
            "Know More",
            x_coordinate + 50,
            next_y - 15,
            self.width - 7 * margin,
            font="Futura",
            size=15,
        )
        # Add hyperlink over the text
        url = content["url"]
        self.canvas.linkURL(
            url,
            (x_coordinate + 50, next_y - 15, x_coordinate + 150, next_y),
            relative=1,
        )

    def advertising_page(self):
        pass

    def get_end_x(self, text, x, font="Helvetica", size=12):
        """
        Given a starting x-coordinate, return the x-coordinate where the text will end after drawing.
        """
        text_width = self.canvas.stringWidth(text, font, size)
        end_x = x + text_width
        return end_x

    def last_page(self):
        # Default Page
        self.initiate_default_page()

        # Starting Coordinates
        x_coordinate = self.width // 2 - 175
        y_coordinate = self.height // 2 + 50

        self.canvas.setFillColor(HexColor("#7b56b1"))
        self.canvas.setFont("Helvetica-Bold", 40)
        self.canvas.drawString(x_coordinate - 30, y_coordinate, "Thanks for Reading")
        # Get the x-coordinate where the text ends
        end_x = self.get_end_x(
            "Thanks for Reading", x_coordinate, font="Helvetica-Bold", size=40
        )
        self.canvas.setFont("Symbola", 40)
        self.canvas.drawRightString(end_x + 10, y_coordinate, "🙏")

    def prepare(self, content):
        self.front_page()
        self.canvas.showPage()
        for key, value in content.items():
            self.next_pages(key, value)
            self.canvas.showPage()
        self.last_page()
        self.canvas.showPage()
        self.canvas.save()


# if __name__ == "__main__":
#     import json
#     with open('data.json', 'r') as file:
#         data = json.load(file)
#     linkedin_post_pdf_obj = LinkedinPostPDF("linkedin_post.pdf")
#     linkedin_post_pdf_obj.prepare(data)
