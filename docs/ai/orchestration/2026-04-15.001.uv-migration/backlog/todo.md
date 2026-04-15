# Backlog

1. [x] Remove legacy setup.py shim
   - backlog-item-id: BI-001
   - deliverable-name: uv-migration
   - status: complete
   - work-item: [01.uv-migration](./01.uv-migration/)
   - depends-on:
   - summary: Delete setup.py since pyproject.toml is already the canonical build configuration.

2. [x] Update .gitignore for UV conventions
   - backlog-item-id: BI-002
   - deliverable-name: uv-migration
   - status: complete
   - work-item: [01.uv-migration](./01.uv-migration/)
   - depends-on:
   - summary: Remove .python-version from .gitignore so UV's Python version pin can be committed.

3. [x] Add .python-version file
   - backlog-item-id: BI-003
   - deliverable-name: uv-migration
   - status: complete
   - work-item: [01.uv-migration](./01.uv-migration/)
   - depends-on: BI-002
   - summary: Create a .python-version file pinning the Python version for UV.

4. [x] Generate uv.lock
   - backlog-item-id: BI-004
   - deliverable-name: uv-migration
   - status: complete
   - work-item: [01.uv-migration](./01.uv-migration/)
   - depends-on: BI-001, BI-003
   - summary: Run uv sync to generate the cross-platform lockfile and commit it.

5. [x] Update README development setup instructions
   - backlog-item-id: BI-005
   - deliverable-name: uv-migration
   - status: complete
   - work-item: [01.uv-migration](./01.uv-migration/)
   - depends-on: BI-004
   - summary: Replace venv/pip development setup in README.md with UV workflow (uv sync, uv run).

6. [x] Migrate CI workflow to UV
   - backlog-item-id: BI-006
   - deliverable-name: uv-migration
   - status: complete
   - work-item: [01.uv-migration](./01.uv-migration/)
   - depends-on: BI-004
   - summary: Update .github/workflows/python-publish.yml to use UV for building and publishing.
