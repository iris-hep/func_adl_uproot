from func_adl_uproot import UprootDataset

import asyncio

import numpy as np
import pytest


def test_uproot_dataset():
    ds = UprootDataset("tests/scalars_tree_file.root")
    assert ds.value().fields == [
        "int_branch",
        "long_branch",
        "float_branch",
        "double_branch",
        "bool_branch",
    ]


def test_materialize_cloned_query():
    query = (
        UprootDataset("tests/scalars_tree_file.root")
        .Select("lambda row: row.int_branch")
        .Where("lambda value: value < 0")
    )
    assert query.value().tolist() == [-1]
    assert asyncio.run(query.execute_result_async(query.query_ast)).tolist() == [-1]


def test_literal_dictionary_four_momentum():
    source = UprootDataset("tests/scalars_tree_file.root")
    result = (
        source.Select(
            lambda row: {
                "pt": row.float_branch,
                "phi": row.float_branch * 0,
                "eta": row.float_branch * 0,
                "mass": row.float_branch * 0,
            }.ToFourMomentum()
        )
        .Select("lambda momentum: momentum.pt")
        .value()
    )
    expected = source.Select("lambda row: row.float_branch").value()
    assert np.allclose(result, expected)


def test_incomplete_dictionary_is_not_four_momentum():
    query = UprootDataset("tests/scalars_tree_file.root").Select(
        lambda row: {
            "pt": row.float_branch,
            "phi": row.float_branch * 0,
        }.ToFourMomentum()
    )
    # Older Vector defers coordinate validation until a 4D property is used.
    with pytest.raises((TypeError, ValueError)) as error:
        query.Select("lambda momentum: momentum.mass").value()
    if isinstance(error.value, TypeError):
        assert "coordinates of a 2D vector, not of a 4D vector" in str(error.value)
    else:
        assert "array does not have longitudinal coordinates" in str(error.value)
