class GatherSessionError(Exception):
    def __init__(self, message="Cannot gather session infos, please check your authorization token."):
        self.message = message
        super().__init__(self.message)