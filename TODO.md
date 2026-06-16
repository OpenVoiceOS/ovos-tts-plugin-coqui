# TODO

## Open issues

- [ ] #18 Cannot install because missing pytorch dependence
- [ ] #12 Dependency Dashboard
- [ ] #6 change catalan default model

## Gaps

- [ ] No test suite and no `tests/` directory.
- [ ] No `pyproject.toml`; packaging via `setup.py` with stale Python 2.x / 3.0-3.6 classifiers.
- [ ] Workflows reference `TigreGotico/gh-automations@master` instead of `OpenVoiceOS/gh-automations@dev`.
- [ ] `build_tests.yml` is hand-rolled (not gh-automations build-tests) and has a YAML indentation error in the "Build Source Packages" step; it installs a core repo rather than testing this plugin.
- [ ] Missing standard gh-automations workflows: build-tests, coverage, license-check, opm-check (TTS plugin declares `mycroft.plugin.tts` entry points).
- [ ] `ovos_tts_plugin_coqui.egg-info/` build artifact committed to the repo.
- [ ] Broken `use_freeVC` branch in `CoquiTTSPlugin.get_tts` references undefined `pt` and a hardcoded `/home/miro/...` path.
- [ ] `__main__` block contains hardcoded local development paths.

## Code TODOs

- [ ] `ovos_tts_plugin_coqui/__init__.py:14` — `# TODO - move to ovos-utils` (the `standardize_lang_tag` helper).
