from pyrannic.support.inflect import ADJECTIVE, pluralize


def test_pluralize():
    """Test the pluralize function with various inputs."""
    assert pluralize("cat") == "cats"
    assert pluralize("dog") == "dogs"
    assert pluralize("fish") == "fish"
    assert pluralize("child") == "children"
    assert pluralize("person") == "people"


def test_pluralize__with_custom_rules():
    assert pluralize("mouse", custom={"mouse": "mice"}) == "mice"


def test_pluralize__with_genitive():
    assert pluralize("dog's") == "dogs'"
    assert pluralize("mouse's") == "mice's"


def test_pluralize__recurse_compound_words():
    assert pluralize("mother-in-law") == "mothers-in-law"
    assert pluralize("Postmaster General") == "Postmasters General"
    assert pluralize("Roman deity") == "Roman deities"


def test_pluralize__pos_adjective():
    assert pluralize("my", pos=ADJECTIVE) == "our"
    assert pluralize("they", pos=ADJECTIVE) == "they"


def test_pluralize__with_irregular_nouns():
    assert pluralize("bison") == "bison"
