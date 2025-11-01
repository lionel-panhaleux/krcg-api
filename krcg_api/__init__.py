from . import api

application = api.create_app()


def main() -> None:
    application.run()
