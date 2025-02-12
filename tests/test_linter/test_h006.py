"""Test linter code H006.

poetry run pytest tests/test_linter/test_h006.py
"""
import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ('<img alt="test"/>'),
        (
            [
                {
                    "code": "H006",
                    "line": "1:0",
                    "match": '<img alt="test"/>',
                    "message": "Img tag should have height and width attributes.",
                }
            ]
        ),
        id="one",
    ),
    pytest.param(
        (
            '{# [INFO][JINJA] I use syntax "{% if <img alt=""\n'
            ' if I want that something happened solely if "img" exists in the content of my articles #}\n'
            "\n"
            ' <script src="script.js" defer></script>\n'
        ),
        ([]),
        id="partial ignored",
    ),
    pytest.param(
        ("<img>"),
        (
            [
                {
                    "code": "H006",
                    "line": "1:0",
                    "match": "<img>",
                    "message": "Img tag should have height and width attributes.",
                },
                {
                    "code": "H013",
                    "line": "1:0",
                    "match": "<img>",
                    "message": "Img tag should have an alt attribute.",
                },
            ]
        ),
        id="test empty",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, nunjucks_config):
    filename = "test.html"
    output = linter(nunjucks_config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = list(filter(lambda x: x not in expected, output[filename])) + list(
        filter(lambda x: x not in output[filename], expected)
    )

    assert len(mismatch) == 0
