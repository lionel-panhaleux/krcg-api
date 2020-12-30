from . import api

application = api.create_app()


def main():
    application.run()
