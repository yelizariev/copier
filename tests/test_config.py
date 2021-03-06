import re
from pathlib import Path

import pytest
from pydantic import ValidationError

import copier
from copier.config.factory import make_config
from copier.config.objects import DEFAULT_DATA, DEFAULT_EXCLUDE, ConfigData, EnvOps
from copier.config.user_data import (
    InvalidConfigFileError,
    MultipleConfigFilesError,
    load_config_data,
    load_yaml_data,
)

GOOD_ENV_OPS = {
    "autoescape": True,
    "block_start_string": "<%",
    "block_end_string": "%>",
    "variable_start_string": "<<",
    "variable_end_string": ">>",
    "keep_trailing_newline": False,
    "i_am_not_a_member": None,
    "comment_end_string": "#>",
    "comment_start_string": "<#",
}


def test_config_data_is_loaded_from_file():
    config = load_config_data("tests/demo_data")
    assert config["_exclude"] == ["exclude1", "exclude2"]
    assert config["_skip_if_exists"] == ["skip_if_exists1", "skip_if_exists2"]
    assert config["_tasks"] == ["touch 1", "touch 2"]
    assert config["_extra_paths"] == ["tests"]


@pytest.mark.parametrize("template", ["tests/demo_yaml", "tests/demo_yml"])
def test_read_data(dst, template):
    copier.copy(template, dst, force=True)
    gen_file = dst / "user_data.txt"
    result = gen_file.read_text()
    expected = Path("tests/reference_files/user_data.txt").read_text()
    assert result == expected


def test_invalid_yaml(capsys):
    conf_path = Path("tests/demo_invalid/copier.yml")
    with pytest.raises(InvalidConfigFileError):
        load_yaml_data(conf_path)
    out, _ = capsys.readouterr()
    assert re.search(r"INVALID.*tests/demo_invalid/copier\.yml", out)


@pytest.mark.parametrize(
    "conf_path,flags,check_out",
    (
        ("tests/demo_invalid", {"_warning": False}, lambda x: "INVALID" in x),
        ("tests/demo_invalid", {"quiet": True}, lambda x: x == ""),
        # test key collision between including and included file
        ("tests/demo_transclude_invalid/demo", {}, None),
        # test key collision between two included files
        ("tests/demo_transclude_invalid_multi/demo", {}, None),
    ),
)
def test_invalid_config_data(conf_path, flags, check_out, capsys):
    with pytest.raises(InvalidConfigFileError):
        load_config_data(conf_path, **flags)
    if check_out:
        out, _ = capsys.readouterr()
        assert check_out(out)


def test_config_data_empty():
    data = load_config_data("tests/demo_config_empty")
    assert data is None


def test_multiple_config_file_error(capsys):
    with pytest.raises(MultipleConfigFilesError):
        load_config_data("tests/demo_multi_config", quiet=True)
    out, _ = capsys.readouterr()
    assert out == ""


# ConfigData
@pytest.mark.parametrize(
    "data",
    (
        {"pretend": "not_a_bool"},
        {"quiet": "not_a_bool"},
        {"force": "not_a_bool"},
        {"skip": "not_a_bool"},
        {"cleanup_on_error": "not_a_bool"},
        {"force": True, "skip": True},
    ),
)
def test_flags_bad_data(data):
    with pytest.raises(ValidationError):
        ConfigData(**data)


def test_flags_extra_ignored():
    key = "i_am_not_a_member"
    conf_data = {"src_path": "..", "dst_path": ".", key: "and_i_do_not_belong_here"}
    confs = ConfigData(**conf_data)
    assert key not in confs.dict()


# EnvOps
@pytest.mark.parametrize(
    "data",
    (
        {"autoescape": "not_a_bool"},
        {"block_start_string": None},
        {"block_end_string": None},
        {"variable_start_string": None},
        {"variable_end_string": None},
        {"keep_trailing_newline": "not_a_bool"},
    ),
)
def test_envops_bad_data(data):
    with pytest.raises(ValidationError):
        EnvOps(**data)


def test_envops_good_data():
    ops = EnvOps(**GOOD_ENV_OPS)
    assert ops.dict() == GOOD_ENV_OPS


# ConfigData
def test_config_data_paths_required():
    try:
        ConfigData(envops=EnvOps())
    except ValidationError as e:
        assert len(e.errors()) == 2
        for i, p in enumerate(("src_path", "dst_path")):
            err = e.errors()[i]
            assert err["loc"][0] == p
            assert err["type"] == "value_error.missing"
    else:
        raise AssertionError()


def test_config_data_paths_existing(dst):
    try:
        ConfigData(
            src_path="./i_do_not_exist",
            extra_paths=["./i_do_not_exist"],
            dst_path=dst,
            envops=EnvOps(),
        )
    except ValidationError as e:
        assert len(e.errors()) == 2
        for i, p in enumerate(("src_path", "extra_paths")):
            err = e.errors()[i]
            assert err["loc"][0] == p
            assert err["msg"] == "Project template not found."
    else:
        raise AssertionError()


def test_config_data_good_data(dst):
    dst = Path(dst).expanduser().resolve()
    expected = {
        "src_path": dst,
        "commit": None,
        "old_commit": None,
        "dst_path": dst,
        "data": DEFAULT_DATA,
        "extra_paths": [dst],
        "exclude": DEFAULT_EXCLUDE,
        "original_src_path": None,
        "skip_if_exists": ["skip_me"],
        "tasks": ["echo python rulez"],
        "templates_suffix": ".tmpl",
        "cleanup_on_error": True,
        "envops": EnvOps().dict(),
        "force": False,
        "only_diff": True,
        "pretend": False,
        "quiet": False,
        "skip": False,
        "vcs_ref": None,
        "migrations": (),
        "secret_questions": (),
        "subdirectory": None,
    }
    conf = ConfigData(**expected)
    expected["data"]["_folder_name"] = dst.name
    expected["answers_file"] = Path(".copier-answers.yml")
    assert conf.dict() == expected


def test_make_config_bad_data(dst):
    with pytest.raises(ValidationError):
        make_config("./i_do_not_exist", dst)


def is_subdict(small, big):
    return {**big, **small} == big


def test_make_config_good_data(dst):
    conf = make_config("./tests/demo_data", dst)
    assert conf is not None
    assert "_folder_name" in conf.data
    assert conf.data["_folder_name"] == dst.name
    assert conf.exclude == ["exclude1", "exclude2"]
    assert conf.skip_if_exists == ["skip_if_exists1", "skip_if_exists2"]
    assert conf.tasks == ["touch 1", "touch 2"]
    assert conf.extra_paths == [Path("tests").resolve()]


@pytest.mark.parametrize(
    "test_input, expected",
    [
        # func_args > defaults
        ({"src_path": ".", "exclude": ["aaa"]}, {"exclude": ["aaa"]}),
        # func_args > user_data
        ({"src_path": "tests/demo_data", "exclude": ["aaa"]}, {"exclude": ["aaa"]}),
    ],
)
def test_make_config_precedence(dst, test_input, expected):
    conf = make_config(dst_path=dst, vcs_ref="HEAD", **test_input)
    assert is_subdict(expected, conf.dict())


def test_config_data_transclusion():
    config = load_config_data("tests/demo_transclude/demo")
    assert config["_exclude"] == ["exclude1", "exclude2"]
