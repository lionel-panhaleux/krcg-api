"""Entrypoint for the WSGI app (web API)
"""
from . import api

application = api.create_app()
