import json
import os.path

import pytest


@pytest.fixture
def load_json():
    def _load_json(fixture_path):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), fixture_path)
        with open(path) as f:
            data = f.read()
        return json.loads(data)

    return _load_json
