"""
Application entry point.
"""

from app.assistant.assistant import Assistant


def main() -> None:

    assistant = Assistant()

    assistant.run()


if __name__ == "__main__":
    main()