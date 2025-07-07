import gettext
import os


def setup_i18n(language="en"):
    locales_dir = os.path.join(os.path.dirname(__file__), "locales")
    translation = gettext.translation(
        "messages", localedir=locales_dir, languages=[language], fallback=True
    )
    translation.install()
    return translation.gettext
