# Tests generated from: ../slugify.rune

import pytest
from slugify import slugify


class TestBasic:
    def test_simple_text(self):
        assert slugify("Hello World") == "hello-world"

    def test_multi_word(self):
        assert slugify("My Blog Post Title") == "my-blog-post-title"


class TestAccents:
    def test_french_accents(self):
        assert slugify("Café Résumé") == "cafe-resume"

    def test_spanish_accents(self):
        assert slugify("Ñoño año") == "nono-ano"

    def test_german_accents(self):
        assert slugify("Ünïcödé") == "unicode"


class TestSpecialCharacters:
    def test_punctuation(self):
        assert slugify("Hello, World!") == "hello-world"

    def test_symbols(self):
        assert slugify("price = $100") == "price-100"

    def test_ampersand(self):
        assert slugify("foo & bar") == "foo-bar"


class TestWhitespace:
    def test_multiple_spaces(self):
        assert slugify("  too   many   spaces  ") == "too-many-spaces"

    def test_already_slugged(self):
        assert slugify("already-slugged") == "already-slugged"


class TestEdgeCases:
    def test_empty_string(self):
        assert slugify("") == ""

    def test_only_special_chars(self):
        assert slugify("!!!") == ""

    def test_numbers_only(self):
        assert slugify("123") == "123"


class TestCustomSeparator:
    def test_underscore(self):
        assert slugify("Hello World", "_") == "hello_world"

    def test_dot(self):
        assert slugify("My Blog Post", ".") == "my.blog.post"
