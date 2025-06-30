class EmailNotValid(Exception):
    def __init__(self, detail, f):
        self.detail = detail
        self.f = f

