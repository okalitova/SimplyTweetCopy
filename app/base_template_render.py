from flask import render_template
from secret_keys import KeysAccessor


def render_over_base_template(*args, **kwargs):
    keys_accessor = KeysAccessor()
    return render_template(*args,
                           **kwargs,
                           GOOGLE_CLIENT_ID=keys_accessor.
                           get_google_client_id())
