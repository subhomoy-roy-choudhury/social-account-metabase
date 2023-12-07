import requests
from github_app.helpers import GithubHelper
from leetcode_app.helpers import get_all_leetcode_questions, get_leetcode_question, fetch_leetcode_question_slug

github_client = GithubHelper()

def solved_leetcode_question_scraper():
    repository = github_client.get_repository("Leetcode-problem-solving")
    initial_contents = repository.get_contents("")
    all_leetcode_questions = get_all_leetcode_questions()
    leetcode_questions_dict = {}
    for content in initial_contents:
        if content.type == "dir":
            # Leetcode Content
            leetcode_question_name = fetch_leetcode_question_slug(content.name)
            question_filter_lambda = lambda x : x["stat"]["question__title_slug"] == leetcode_question_name
            filtered_questions = list(filter(question_filter_lambda, all_leetcode_questions))
            if filtered_questions:
                question_details = filtered_questions[0]
            else:
                question_details = None

            # Github Content
            leetcode_problem_contents = repository.get_contents(content.path)
            leetcode_problem_dict = {}
            for item in leetcode_problem_contents:
                file_content = repository.get_contents(item.path)
                file_name = item.path.split("/")[-1]
                leetcode_problem_dict[file_name] = file_content.decoded_content
                print(f"File: {item.path}")
            leetcode_questions_dict[content.path] = {**leetcode_problem_dict, "question_details": question_details}
    return True