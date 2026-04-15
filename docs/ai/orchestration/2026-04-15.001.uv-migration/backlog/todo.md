# Backlog

1. [ ] Remove legacy setup.py shim
   - backlog-item-id: BI-001
   - deliverable-name: remove-setup-py
   - status: pending
   - work-item:
   - depends-on:
   - summary: Delete setup.py since pyproject.toml is already the canonical build configuration and UV does not need the shim.

2. [ ] Update .gitignore for UV conventions
   - backlog-item-id: BI-002
   - deliverable-name: update-gitignore
   - status: pending
   - work-item:
   - depends-on:
   - summary: Remove .python-version from .gitignore so UV's Python version pin can be committed.

3. [ ] Add .python-version file
   - backlog-item-id: BI-003
   - deliverable-name: add-python-version
   - status: pending
   - work-item:
   - depends-on: BI-002
   - summary: Create a .python-version file pinning the Python version for UV to use when creating the virtual environment.

4. [ ] Generate uv.lock
   - backlog-item-id: BI-004
   - deliverable-name: generate-uv-lock
   - status: pending
   - work-item:
   - depends-on: BI-001, BI-003
   - summary: Run uv sync to generate the cross-platform lockfile and commit it to the repository.

5. [ ] Update README development setup instructions
   - backlog-item-id: BI-005
   - deliverable-name: update-readme-dev-setup
   - status: pending
   - work-item:
   - depends-on: BI-004
   - summary: Replace the venv/pip development setup section in README.md with UV-based workflow (uv sync, uv run).

6. [ ] Migrate CI workflow to UV
   - backlog-item-id: BI-006
   - deliverable-name: migrate-ci-to-uv
   - status: pending
   - work-item:
   - depends-on: BI-004
   - summary: Update .github/workflows/python-publish.yml to install UV and use it for building and publishing the package.
