# GitLab CI/CD Pipeline for MkDocs Deployment

This document explains the purpose and function of a GitLab CI/CD pipeline that builds and deploys MkDocs-based documentation to GitLab Pages.

---

## CI Configuration

The pipeline is defined in the `.gitlab-ci.yml` file, which looks like this:

```yaml
image: python:3.9-slim

before_script:
  - time apt update
  - time pip install -r requirements.txt
  - time cd mdocotion && python setup.py install && cd ..

pages:
  stage: deploy
  tags:
    - hva
  script:
    - time mkdocs build --site-dir public
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

variables:
  GIT_SUBMODULE_STRATEGY: recursive
```

---

## Explanation

### `image: python:3.9-slim`

This line sets the Docker image used to run the CI/CD pipeline. It uses a minimal version of Python 3.9 to keep the environment lightweight and fast. This is ideal for Python-based projects like MkDocs.

---

### `before_script`

```yaml
before_script:
  - time apt update
  - time pip install -r requirements.txt
  - time cd mdocotion && python setup.py install && cd ..
```

This section runs before any job and sets up the environment:

- `apt update`: Updates the list of available packages for `apt`, the Debian package manager.
- `pip install -r requirements.txt`: Installs all required Python packages listed in `requirements.txt`.
- `cd mdocotion && python setup.py install && cd ..`: Installs a local Python package (`mdocotion`) from its source code using `setup.py`.

The `time` command is used on each line to measure how long each step takes.

---

### `pages` Job

```yaml
pages:
  stage: deploy
  tags:
    - hva
  script:
    - time mkdocs build --site-dir public
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

This job is responsible for building and deploying the MkDocs documentation to GitLab Pages.

#### Breakdown:

- `stage: deploy`: Indicates that this job belongs to the `deploy` stage of the pipeline.
- `tags: [hva]`: This job will only run on GitLab runners that have the `hva` tag.
- `script`: Runs the MkDocs build command, outputting the static site files to the `public` directory.
- `artifacts`: Specifies that the `public` folder should be saved and made available as a build artifact (this is required for GitLab Pages).
- `rules`: Ensures this job only runs when the current branch is the default branch (e.g., `main` or `master`), preventing deployments from feature branches.

---

### `variables`

```yaml
variables:
  GIT_SUBMODULE_STRATEGY: recursive
```

This variable ensures that if the project uses Git submodules (e.g., a theme stored as a submodule), they are cloned recursively. Without this, the pipeline may fail if it depends on submodule content.

---

## Summary

This GitLab CI/CD configuration is designed to:

- Set up a Python 3.9 environment.
- Install required dependencies and a local Python module (`mdocotion`).
- Build documentation using MkDocs.
- Deploy the site to GitLab Pages (only from the default branch).
- Clone submodules if necessary.

It is optimized for projects hosted on GitLab and intended to run on runners tagged with `hva`. This setup allows teams to automatically publish updated documentation whenever changes are pushed to the default branch.
