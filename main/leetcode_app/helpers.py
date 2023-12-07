import re
import requests

def fetch_leetcode_question_slug(string):
    pattern = r'\d+-(.*)'
    match = re.match(pattern, string)
    if match:
        result = match.group(1)
        return result

def get_all_leetcode_questions():
    response = requests.get("https://leetcode.com/api/problems/algorithms/")
    return response.json()["stat_status_pairs"]

def get_leetcode_question(question_slug):
    response = requests.get("https://leetcode.com/problems/" + question_slug)
    return response.json()