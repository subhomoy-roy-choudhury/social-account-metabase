class NoSuitableArticleFound(Exception):
    pass

class DailyLinkedinPostTaskError(Exception):
    def __init__(self, message="Daily Linkedin Post Task Failed !!"):
        self.message = message
        super().__init__(self.message)