# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Tests for srlearn.background.Background
"""

import pathlib
import pytest
from srlearn.background import Background
from srlearn.datasets import load_toy_cancer


@pytest.mark.parametrize("std", [False, True])
@pytest.mark.parametrize("pro", [False, True])
def test_iff_variables(std, pro):
    """Variable representation cannot be equal."""
    if std == pro:
        with pytest.raises(ValueError):
            _bk = Background(
                use_std_logic_variables=std,
                use_prolog_variables=pro,
            )
    else:
        _bk = Background(
            use_std_logic_variables=std,
            use_prolog_variables=pro,
        )

        assert _bk.use_std_logic_variables == std
        assert _bk.use_prolog_variables == pro


def test_initialize_background_knowledge_1():
    """
    Test initializing a Background object with default settings.
    """
    _bk = Background()
    assert _bk.modes is None
    assert not _bk.line_search
    assert not _bk.recursion


def test_initialize_example_background_knowledge_1():
    """Test initializing with example data modes"""
    toy_cancer = load_toy_cancer()
    _bk = Background(modes=toy_cancer.train.modes)
    assert _bk.modes == toy_cancer.train.modes
    assert not _bk.line_search
    assert not _bk.recursion

    _capture = str(_bk)
    assert "setParam: nodeSize=2." in _capture
    assert "setParam: maxTreeDepth=3." in _capture
    assert "setParam: numOfCycles=100." in _capture
    assert "setParam: numOfClauses=100." in _capture
    assert "friends(+Person,-Person)." in _capture
    assert "friends(-Person,+Person)." in _capture
    assert "smokes(+Person)." in _capture
    assert "cancer(+Person)." in _capture


def test_initializing_example_background_knowledge_2():
    """Test initializing with example data modes and extra parameters."""
    toy_cancer = load_toy_cancer()
    _bk = Background(
        modes=toy_cancer.train.modes,
        line_search=True,
        recursion=True,
        node_size=3,
        max_tree_depth=4,
        number_of_clauses=8,
        number_of_cycles=10,
    )
    assert _bk.modes == toy_cancer.train.modes

    _capture = str(_bk)
    assert "setParam: nodeSize=3." in _capture
    assert "setParam: maxTreeDepth=4." in _capture
    assert "setParam: numOfCycles=10." in _capture
    assert "setParam: numOfClauses=8." in _capture
    assert "setParam: lineSearch=true." in _capture
    assert "setParam: recursion=true." in _capture
    assert "friends(+Person,-Person)." in _capture
    assert "friends(-Person,+Person)." in _capture
    assert "smokes(+Person)." in _capture
    assert "cancer(+Person)." in _capture


def test_initializing_example_background_knowledge_3():
    """Test initializing with example data modes and extra parameters."""
    toy_cancer = load_toy_cancer()
    _bk = Background(
        modes=toy_cancer.train.modes,
        line_search=True,
        recursion=True,
        node_size=3,
        max_tree_depth=4,
        number_of_clauses=8,
        number_of_cycles=10,
        ok_if_unknown=["smokes/1", "friends/2"],
        bridgers=["friends/2"],
    )
    assert _bk.modes == toy_cancer.train.modes

    _capture = str(_bk)
    assert "setParam: nodeSize=3." in _capture
    assert "setParam: maxTreeDepth=4." in _capture
    assert "setParam: numOfCycles=10." in _capture
    assert "setParam: numOfClauses=8." in _capture
    assert "setParam: lineSearch=true." in _capture
    assert "setParam: recursion=true." in _capture
    assert "friends(+Person,-Person)." in _capture
    assert "friends(-Person,+Person)." in _capture
    assert "smokes(+Person)." in _capture
    assert "cancer(+Person)." in _capture
    assert "okIfUnknown: smokes/1." in _capture
    assert "okIfUnknown: friends/2." in _capture
    assert "bridger: friends/2." in _capture


def test_write_background_to_file_1(tmpdir):
    """Test writing Background object to a file with default parameters."""
    _bk = Background()
    _bk.write(filename="train", location=pathlib.Path(tmpdir))
    assert tmpdir.join("train_bk.txt").read() == str(_bk)


def test_write_background_to_file_2(tmpdir):
    """Test writing Background object to a file with extra parameters."""
    toy_cancer = load_toy_cancer()
    _bk = Background(modes=toy_cancer.train.modes, node_size=1, max_tree_depth=5)
    _bk.write(filename="train", location=pathlib.Path(tmpdir))
    assert tmpdir.join("train_bk.txt").read() == str(_bk)


def test_string_conversion_no_modes():
    """Test initializing when no modes are provided."""

    _bk = Background()
    _capture = str(_bk)
    assert "smokes(+person)." not in _capture


@pytest.mark.parametrize("test_input", [1.5, 4, "True", "False", bool, int, 0, 1])
def test_initialize_bad_background_knowledge_modes(test_input):
    """Incorrect modes settings"""
    with pytest.raises(ValueError):
        _bk = Background(modes=test_input)


@pytest.mark.parametrize("test_input", [1.5, 4, None, "True", "False", bool, int, 0, 1])
def test_initialize_bad_background_knowledge_recursion(test_input):
    """Incorrect recursion settings."""
    with pytest.raises(ValueError):
        _bk = Background(recursion=test_input)


@pytest.mark.parametrize("test_input", [1.5, 4, None, "True", "False", bool, int, 0, 1])
def test_initialize_bad_background_knowledge_line_search(test_input):
    """Incorrect line_search settings"""
    with pytest.raises(ValueError):
        _bk = Background(line_search=test_input)


@pytest.mark.parametrize(
    "test_input", [0, -1, None, "True", "False", bool, int, 1.5, True, False]
)
def test_initialize_bad_background_knowledge_max_tree_depth(test_input):
    """Incorrect max_tree_depth settings."""
    with pytest.raises(ValueError):
        _bk = Background(max_tree_depth=test_input)


@pytest.mark.parametrize(
    "test_input", [0, -1, None, "True", "False", bool, int, 1.5, True, False]
)
def test_initialize_bad_background_knowledge_number_of_cycles(test_input):
    """Incorrect number_of_cycles settings."""
    with pytest.raises(ValueError):
        _bk = Background(number_of_cycles=test_input)


@pytest.mark.parametrize(
    "test_input", [0, -1, None, "True", "False", bool, int, 1.5, True, False]
)
def test_initialize_bad_background_knowledge_number_of_clauses(test_input):
    """Incorrect number_of_cycles settings."""
    with pytest.raises(ValueError):
        _bk = Background(number_of_clauses=test_input)


@pytest.mark.parametrize(
    "test_input", [0, -1, 1, 4, None, "True", "False", bool, int, 1.5]
)
def test_initialize_bad_background_knowledge_load_all_libraries(test_input):
    """Incorrect load_all_libraries arguments."""
    with pytest.raises(ValueError):
        _bk = Background(load_all_libraries=test_input)


@pytest.mark.parametrize(
    "test_input", [0, -1, 1, 4, None, "True", "False", bool, int, 1.5]
)
def test_initialize_bad_background_knowledge_load_all_basic_modes(test_input):
    """Incorrect load_all_basic_modes arguments."""
    with pytest.raises(ValueError):
        _bk = Background(load_all_basic_modes=test_input)


@pytest.mark.parametrize(
    "test_input", [0, -1, 1, 4, None, "True", "False", bool, int, 1.5]
)
def test_initialize_bad_logic_variables(test_input):
    """Initialize use_std_logic_variables with input which raises error."""
    with pytest.raises(ValueError):
        _bk = Background(use_std_logic_variables=test_input)


@pytest.mark.parametrize(
    "test_input", [0, -1, 1, 4, None, "True", "False", bool, int, 1.5]
)
def test_initialize_bad_prolog_variables(test_input):
    """Initialize use_prolog_variables with input which raises error."""
    with pytest.raises(ValueError):
        _bk = Background(use_prolog_variables=test_input)


@pytest.mark.parametrize(
    "test_input", [0, -1, 1, 4, "True", "False", bool, int, 1.5]
)
def test_initialize_bad_ok_if_unknown_variables(test_input):
    """Initialize ok_if_unknown with input that should raise error."""
    with pytest.raises(ValueError):
        _bk = Background(ok_if_unknown=test_input)


@pytest.mark.parametrize(
    "test_input", [0, -1, 1, 4, "True", "False", bool, int, 1.5]
)
def test_initialize_bad_bridgers(test_input):
    """Initialize bridgers with input that should raise an error."""
    with pytest.raises(ValueError):
        _bk = Background(bridgers=test_input)
