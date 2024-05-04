class Config():
    def __init__(self, token) -> None:
        self.url = f"https://api.telegram.org/bot{token}/"
        self.url_file = f"https://api.telegram.org/file/bot{token}/"