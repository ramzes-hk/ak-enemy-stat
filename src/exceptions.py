class JSONException(Exception):
    def __init__(self, file, message="Incorrect JSON"):
        super().__init__(f"{message}: {file}")
