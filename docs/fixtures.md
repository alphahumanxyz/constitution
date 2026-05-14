# Fixtures and Runtime Outputs

Tracked fixtures are deterministic inputs or expected outputs used to validate the
Constitution. Keep them small enough to review in pull requests, and store them
outside local runtime directories.

Runtime logs, caches, scratch evidence, and generated validation output must use
the default local paths from `scripts/runtime_paths.sh`:

- `.local/constitution/evidence/`
- `.local/constitution/cache/`
- `.local/constitution/logs/`

Those paths are ignored by git. Promote a generated artifact into a tracked
fixture only after reviewing it for private material and documenting why it is
stable evidence.
