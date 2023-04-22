"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget

import tempfile
import time
import zulip

if TYPE_CHECKING:
    import napari

# Global parameters
realm = "napari.zulipchat.com"
config_path = f"/Users/kharrington/.zulip.d/{realm}.zuliprc"

# randoms_stream_id = 348229

# Globals vars
client = zulip.Client(config_file=config_path)

@magic_factory
def screenshot_to_zulip(img_layer: "napari.layers.Image", viewer: "napari.viewer.Viewer"):
    local_path = f"/tmp/napari_{int(time.time())}.png"

    # Save screenshot into temp file
    viewer.screenshot(path=local_path)
    
    with open(local_path, "rb") as fp:
        upload_result = client.upload_file(fp)

    message_request = {
        "type": "stream",
        "to": "randoms",
        "topic": "emacs zulip",
        "content": "does a screenshot directly from a live napari work? [a screenshot from a live napari session]({})".format(upload_result["uri"]),
    }

    # Share the file by including it in a
    client.send_message(
        message_request
    )


