# Contributing Guide

> If you have no prior experience contributing to open-source projects, you
> might want to look at the official [GitHub documentation][github-docs] or
> alternative resources, such as [First Contribution][first-contribution].

You are welcome to contribute by:

- opening issues;
- creating pull requests;
- participating in discussions on the existing issues and PRs.

Use our forms and templates, and adhere to the guidelines and checklists
provided, whether you're opening an issue or submitting a pull request.

## Issues

There are several types of issues one can [open][open-issue] to contribute to
the project. An issue of each type can be created using a specific form.
Irrespective of the issue type, all contributors are requested to confirm that
they are familiar with this guide and the project's [Code of Conduct][code-of-conduct],
as well as that they have inspected that the issue they want to open is not
a duplicate.

## Pull Requests

If you're looking to make small tweaks (e.g., fix typos in the documentation),
feel free to jump straight to creating a pull request. But if it's something
more substantial, like reporting a bug or suggesting a new feature, it's better
to start off by opening an issue. This gives everyone in the community a chance
to chime in and make sure we're all on the same page. Once there's a general
agreement, you'll be encouraged to submit your pull request.

To contribute to the project via a pull request, follow the instructions:

1. [Fork][fork] the repo, clone it to your machine, and to the project's root.
2. The project uses a couple of non-Python utilities that can be installed using
   the Node package manager `npm`. To install them, run:

   ```console
   npm install
   ```

   > This assumes you have Node on your machine. If you don't, download and
   > install the latest release from the official [Node.js][node] website.

3. Create and activate the virtual environment:

   ```console
   python -m venv .venv && source .venv/bin/activate
   ```

   > See the [`.python-version`][python-version] file to check the interpreter
   > version used in the development.

4. Install the package in development mode:

   ```console
   pip install -e ".[dev]"
   ```

5. Install [Pre-commit][pre-commit] hooks:

   ```console
   pre-commit install
   ```

6. Check the setup by running [Nox][nox]:

   ```console
   nox
   ```

   This will inspect the code quality with linters, run the existing tests in
   different Python/Django/database environments, and measure their coverage.
   Add the `-l` flag to echo more details on the available Nox sessions.

   > Note that you should have all the versions of Python installed on your
   > machine. Consider using [`pyenv`][pyenv] to work with multiple Python
   > interpreters. The app supports the PostgreSQL database, so make sure
   > a local instance has been set up. Connection data and credentials can be
   > defined via environment variables (see [`.env.example`][env-example]).

7. Check out a new feature branch and introduce changes.

   > First of all, we request that your PR be as "atomic" as possible. Any
   > changes that impact the codebase should be accompanied by relevant unit
   > tests and updates to the documentation. We strive to maintain 100% test
   > coverage and expect the same from all pull requests. PRs lacking tests will
   > not be considered for merging.

8. Run Nox again. If all the sessions are successful and the changes are covered
   by tests, commit your changes and push them to remote.

   > Keep in mind that when you create a pull request, the CI will run all the
   > checks anyway. Nevertheless, it is still strongly recommended to test
   > everything locally before pushing to remote and opening a pull request.

9. [Create a pull request][create-pull-request] from the feature branch of your
   fork to the `main` branch of the upstream repository.

   > Please note that our project adheres to the [Conventional Commits][conventional-commits]
   > scheme, using the [@commitizen/conventional-commit-types][conventional-commit-types]
   > set of rules. The [@action-semantic-pull-request][action-semantic-pull-request]
   > is utilized to validate whether the title of your PR conforms to the
   > established convention. The number and format of the PR's commits are at
   > your discretion. When merging the branch from your fork into `main`, all
   > commits will be squashed into a single commit, with the PR title serving
   > as the commit subject.

That's it!

Once your pull request passes all CI checks, the project maintainers will
examine it as quickly as feasible.

## Coding Style

The project uses a variety of tools to enforce uniform and consistent coding
style throughout the entire codebase.

- [Prettier][prettier] is used for non-Python assets auto-formatting.
- [Markdownlint][markdownlint] is adopted to lint documentation files.
- [Ruff][ruff] is used to lint and format the Python codebase.
- [Mypy][mypy] is incorporated to perform the Python type-checking.

All those tools are in the package's development dependencies, so they can be
used separately on demand. They are also set up as Pre-commit hooks, so one can
run them collectively:

```console
pre-commit run --all-files
```

[action-semantic-pull-request]: https://github.com/amannn/action-semantic-pull-request
[code-of-conduct]: https://github.com/paduszyk/django-xlsx-serializer/blob/main/docs/CODE_OF_CONDUCT.md
[conventional-commit-types]: https://github.com/commitizen/conventional-commit-types
[conventional-commits]: https://www.conventionalcommits.org/en/v1.0.0/
[create-pull-request]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
[env-example]: https://github.com/paduszyk/django-xlsx-serializer/blob/main/.env.example
[first-contribution]: https://github.com/firstcontributions/first-contributions
[fork]: https://docs.github.com/en/get-started/quickstart/fork-a-repo
[github-docs]: https://docs.github.com/en/get-started/quickstart/contributing-to-projects
[markdownlint]: https://github.com/DavidAnson/markdownlint
[mypy]: https://mypy.readthedocs.io
[node]: https://nodejs.org/
[nox]: https://github.com/wntrblm/nox
[open-issue]: https://github.com/paduszyk/django-xlsx-serializer/issues/new/choose
[pre-commit]: https://pre-commit.com
[prettier]: https://prettier.io
[pyenv]: https://github.com/pyenv/pyenv
[python-version]: https://github.com/paduszyk/django-xlsx-serializer/blob/main/.python-version
[ruff]: https://docs.astral.sh/ruff/
