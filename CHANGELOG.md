# Changelog

All notable changes to this project will be documented in this file. This project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

<details>
<!-- prettier-ignore-start -->
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
<summary>Table of contents</summary>

- [Version 3.1.0 (2020-05)](#version-310-2020-05)
- [Version 3.0.0 (2020-03)](#version-300-2020-03)
  - [Features](#features)
  - [Other](#other)
- [Version 2.5 (2019-06)](#version-25-2019-06)
- [Version 2.4.2 (2019-06)](#version-242-2019-06)
- [Version 2.4 (2019-06)](#version-24-2019-06)
- [Version 2.3 (2019-04)](#version-23-2019-04)
- [Version 2.2 (2019-04)](#version-22-2019-04)
- [Version 2.1 (2019-02)](#version-21-2019-02)
- [Version 2.0 (2019-02)](#version-20-2019-02)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
<!-- prettier-ignore-end -->
</details>

### Version 3.1.0 (2020-05)

[All changes here](https://github.com/pykong/copier/milestone/7?closed=1). Summary:

- Assert minimum copier version.
- Prettier prompts.
- Prompt self-templating.
- Better README.

### Version 3.0.0 (2020-03)

This is a big release with many new features added and improved. The code base also
received a lot of love and hardening.

#### Features

- Minimal supported Python version is now 3.6.
- Dropped support for deprecated `voodoo.json`.
- Introduced gitignore-style patterns for `exclude` und `skip-if-exists`.
- Dropped support for `include` option.
- Added support for extending content of config files via content of other files via
  `pyaml-include`.
- Customizable template extension.
- Ability to remember last answers.
- Ability to choose where to remember them.
- Template upgrades support, (based on the previous points) with migration tasks
  specification.
- Extended questions format, supporting help, format, choices and secrets.
- More beautiful prompts.
- New CLI experience.

#### Other

- Moved to `poetry` for package management.
- Type annotated entire code base.
- Increased test coverage.
- Ditched `ruamel.yaml` for `PyYaml`.
- Ditched Travis CI for GitHub Actions.
- Added `pre-commit` for enforced linting.
- Added `prettier`, `black` and `isort` for code formatting.
- Added `pytest` for running tests.
- Use `plumbum` as CLI and subprocess engine.

### Version 2.5 (2019-06)

- Expanduser on all paths (so "~/foo/bar" is expanded to "<YOUR_HOME_FOLDER>/foo/bar").
- Improve the output when running tasks.
- Remove the destination folder if the copy process or one of the tasks fail.
- Add a `cleanup_on_error` flag to optionally disable the cleanup feature.
- Add the `skip_if_exists` option to skip files, without asking, if they already exists
  in the destination folder.

### Version 2.4.2 (2019-06)

- Fix MAJOR bug that was preventing the `_exclude`, `_include` and `_tasks` keys from
  `copier.yml` (or alternatives) to be used at all. It also interpreted `_tasks` as a
  user-provided variable.

### Version 2.4 (2019-06)

- Empty folders are now copied. The folders are also displayed in the console output
  instead of just the files.
- `prompt_bool` can now have an undefined default (ans answer is mandatory in that
  case).
- Reactivates the `copier.yml` and `copier.yaml` as configuration files.
- The new `extra_paths` argument specifies additional paths to find templates to inherit
  from.

### Version 2.3 (2019-04)

- Back to using a setup.py intead of a pyproject.toml.
- The recommended configuration file is now `copier.toml`.

### Version 2.2 (2019-04)

- The `copier` command-line script now accepts "help" and "version" as commands.

### Version 2.1 (2019-02)

- Task runner 🎉.
- Use `_exclude`, `_include`, and `_tasks` keys in `copier.yml` as the default values
  for the `.copy()` arguments `exclude`, `include`, and `tasks`.

### Version 2.0 (2019-02)

- Rebranded from `Voodoo` to `Copier`!
- Dropped support for Python 2.x, the minimal version is now Python 3.5.
- Cleanup and 100% test coverage.
- The recommended configuration file is now `copier.yaml`, but a `copier.json` can be
  used as well. The old `voodoo.json` is also supported _for now_ but is deprecated and
  will be removed in version 2.2.
- Python package format updated to the latest standard (no `setup.py` 😵).
- Renamed the `render_skeleton()` function to `copy()`. The function signature remains
  almost the same, the only changes are:
  - `filter_this` parameter is now called `exclude`.
  - `ignore_this` parameter is now called just `ignore`.
- Dropped the idea of storing the templates in a hidden `$HOME` folder.
