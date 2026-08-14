from app.commands.base import BaseCommand
from app.services.browser_service import BrowserService


class BrowserCommand(BaseCommand):

    def __init__(self):

        self.browser = BrowserService()

    def can_handle(self, command: str) -> bool:

        return command.startswith("open ")

    def execute(self, command: str) -> str:

        website = command.replace("open", "", 1).strip()

        if self.browser.open(website):
            return f"Opening {website}"

        return "Sorry, I don't know that website."