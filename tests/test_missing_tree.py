import ast
import logging

import awkward as ak
import numpy as np
import pytest
import qastle
import uproot

from func_adl_uproot import (
    UprootDataset,
    ast_executor,
    generate_function,
    generate_python_source,
)


@pytest.fixture
def inputs(tmp_path):
    missing = tmp_path / "missing.root"
    populated = tmp_path / "populated.root"
    with uproot.recreate(missing) as output:
        output.mktree("other", {"value": "int64"})
    with uproot.recreate(populated) as output:
        output.mktree("reco", {"value": "int64"})
        output["reco"].extend({"value": np.array([4, 9])})
    return str(missing), str(populated)


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("as_qastle", [False, True])
def test_named_missing_tree_default(inputs, reverse, as_qastle, caplog):
    files = list(inputs)[:: (-1 if reverse else 1)]
    query = UprootDataset(files, "reco").Select("lambda row: row.value").query_ast
    if as_qastle:
        query = qastle.python_ast_to_text_ast(query)
    with caplog.at_level(logging.WARNING):
        assert ak.to_list(ast_executor(query)) == [4, 9]
    assert inputs[0] in [record.args[0] for record in caplog.records]
    assert "reco" in caplog.text


def test_all_absent_retains_error(inputs):
    with pytest.raises(ValueError, match="No input contains.*reco"):
        UprootDataset([inputs[0]], "reco").value()


def test_generated_module_identifies_missing_tree(tmp_path):
    keyless = tmp_path / "keyless.root"
    with uproot.recreate(keyless):
        pass
    namespace = {}
    exec(generate_python_source(ast.parse("EventDataset(None, 'reco')")), namespace)
    with pytest.raises(
        namespace["NoMatchingTreeError"], match="No input contains.*reco"
    ):
        namespace["run_query"](str(keyless))


@pytest.mark.parametrize("as_qastle", [False, True])
def test_zero_entry_tree_does_not_require_filter_field(tmp_path, as_qastle):
    empty = tmp_path / "empty.root"
    with uproot.recreate(empty) as output:
        output.mktree("reco", {"value": "int64"})
    query = (
        UprootDataset(str(empty), "reco")
        .Where("lambda row: row.trigger > 0")
        .Select("lambda row: {'value': row.value}")
        .query_ast
    )
    if as_qastle:
        query = qastle.python_ast_to_text_ast(query)
    result = ast_executor(query)
    assert ak.to_list(result) == []
    assert str(ak.type(result)) == "0 * {value: int64}"


def test_zero_entry_tree_still_requires_projected_field(tmp_path):
    empty = tmp_path / "empty.root"
    with uproot.recreate(empty) as output:
        output.mktree("reco", {"value": "int64"})
    query = (
        UprootDataset(str(empty), "reco")
        .Where("lambda row: row.trigger > 0")
        .Select("lambda row: row.absent")
        .query_ast
    )
    with pytest.raises(
        (AttributeError, uproot.exceptions.KeyInFileError), match="absent"
    ):
        ast_executor(query)


def test_runtime_override(inputs):
    function = generate_function(
        ast.parse("Select(EventDataset(), lambda row: row.value)")
    )
    assert ak.to_list(function(list(inputs), "reco")) == [4, 9]


def test_errors_not_suppressed(inputs, tmp_path):
    corrupt = tmp_path / "corrupt.root"
    corrupt.write_bytes(b"not a ROOT file")
    queries = [
        (UprootDataset([str(corrupt), inputs[1]], "reco").query_ast, OSError),
        (UprootDataset([str(tmp_path / "unreadable.root")], "reco").query_ast, OSError),
        (
            UprootDataset(inputs[1], "reco").Select("lambda row: row.absent").query_ast,
            (AttributeError, uproot.exceptions.KeyInFileError),
        ),
        (
            ast.parse(
                "UnknownOperation(EventDataset(" + repr(inputs[1]) + ", 'reco'))"
            ),
            NameError,
        ),
    ]
    for query, error in queries:
        with pytest.raises(error):
            ast_executor(query)


@pytest.mark.parametrize("reverse", [False, True])
def test_known_typed_empty_and_mixed_schema(inputs, tmp_path, reverse):
    empty = tmp_path / "empty.root"
    with uproot.recreate(empty) as output:
        output.mktree("reco", {"value": "int64", "unused": "float64"})
    files = [str(empty), inputs[1]][:: (-1 if reverse else 1)]
    query = UprootDataset(files, "reco").Select("lambda row: row.value")
    assert ak.to_list(ast_executor(query.query_ast)) == [4, 9]
    empty_query = UprootDataset(str(empty), "reco").Select("lambda row: row.value")
    result = ast_executor(empty_query.query_ast)
    assert ak.to_list(result) == []
    assert str(ak.type(result)) == "0 * int64"
    rejected = query.Where("lambda value: value < 0")
    assert ak.to_list(ast_executor(rejected.query_ast)) == []


def test_wrong_object_not_suppressed(tmp_path):
    path = tmp_path / "wrong.root"
    with uproot.recreate(path) as output:
        output["reco"] = "not a tree"
    with pytest.raises((TypeError, AttributeError, ValueError)):
        ast_executor(UprootDataset(str(path), "reco").query_ast)


@pytest.mark.parametrize("reverse", [False, True])
def test_populated_missing_output_in_mixed_inputs(inputs, tmp_path, reverse):
    missing_branch = tmp_path / "missing_branch.root"
    with uproot.recreate(missing_branch) as output:
        output.mktree("reco", {"other": "int64"})
        output["reco"].extend({"other": np.array([7])})
    files = [inputs[1], str(missing_branch)][:: (-1 if reverse else 1)]
    with pytest.raises(ValueError, match="have no TBranches in common"):
        UprootDataset(files, "reco").Select("lambda row: row.value").value()


def test_filename_pattern_preserves_uproot_expansion(inputs):
    pattern = inputs[1].replace("populated.root", "pop*.root")
    query = UprootDataset(pattern, "reco").Select("lambda row: row.value")
    assert ak.to_list(query.value()) == [4, 9]
