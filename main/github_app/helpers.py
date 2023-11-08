from github import Github, InputGitTreeElement, InputGitAuthor

from authentication.helpers import check_github_token


class GithubHelper(object):
    def __init__(self) -> None:
        self.access_token, error = check_github_token()
        # Authentication
        self.github_client = Github(self.access_token)
        self.organization_name = "Oderna"
        # Set up the author information for the commit
        self.author = InputGitAuthor(
            "Subhomoy Roy Choudhury", "subhomoyrchoudhury@gmail.com"
        )

    def add_file(self):
        # Get the organization
        org = self.github_client.get_organization(self.organization_name)
        repo_name = "hugo-blog"
        folder_path = "content/posts"
        file_path = f"{folder_path}/second-post.md"
        commit_message = "Update file"
        with open("github_app/blog-template.md", "r") as file:
            content = file.read()

        file_content = content.format(
            **{
                "title": "Second Post",
                "heading": "Test Heading",
                "content": "Test Heading Content",
            }
        )

        # Get the contents of the file (assuming it already exists)
        # contents = repo.get_contents(file_path, ref="master")

        # Get the repo
        repo = org.get_repo(repo_name)

        # Update the file
        try:
            repo.create_file(
                file_path, commit_message, file_content, author=self.author
            )
        except Exception as error:
            # If the file already exists, it will raise an exception
            print(f"An error occurred: {error}")

        print(f"File {file_path} has been created in {repo_name}")
        return True
