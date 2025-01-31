import anywidget
import traitlets
import pathlib


class URLWidget(anywidget.AnyWidget):
    # Python-side trait to store the URL
    current_url = traitlets.Unicode("").tag(sync=True)
    _esm = """
        function render({model, el}) {
            model.set('current_url', window.location.href);
            model.save_changes();
        }

        export default {render}
    """
