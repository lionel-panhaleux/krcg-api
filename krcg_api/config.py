from krcg import models

#: languages krcg ships translated data for (used for content negotiation)
SUPPORTED_LANGUAGES = [lang.value for lang in models.Lang]
KRCG_STATIC_SERVER = "https://static.krcg.org"
