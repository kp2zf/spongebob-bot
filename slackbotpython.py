class SlackbotPython:

    def __init__(self, channel):
        self.channel = channel
        self.username = "Mocking Spongebob"
        self.icon_emoji = ":mocking_spongebob:"
        self.timestamp = ""
        self.reaction_task_completed = False

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                *self._get_reaction_block(),
            ],
        }

    def _get_reaction_block(self):
        task_checkmark = self._get_checkmark(self.reaction_task_completed)
        text = (
            f"{task_checkmark} *Add an emoji reaction to this message* "
        )
        return self._get_task_block(text)

    @staticmethod
    def _get_checkmark(task_completed: bool) -> str:
        if task_completed:
            return ":white_check_mark:"
        return ":white_large_square:"

    @staticmethod
    def _get_task_block(text):
        return [
            {"type": "section", 
             "text": {
                 "type": "mrkdwn", 
                 "text": text
                 }
            },
        ]