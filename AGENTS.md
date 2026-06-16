# ovos-tts-plugin-coqui

OVOS TTS plugin wrapping [Coqui TTS](https://coqui-tts.readthedocs.io). Ships four plugin entry points: a generic Coqui model loader, an XTTS-v2 multilingual/voice-cloning plugin, a FreeVC voice-conversion wrapper around any base OVOS TTS plugin, and a FairSeq/MMS plugin covering 1100+ languages.

## Setup

```
pip install .
```

Runtime deps: `coqui-tts`, `langcodes`, `ovos-plugin-manager>=2.1.0,<2.2.0`. Coqui pulls in heavy ML stack (torch). GPU is opt-in via the `"gpu": true` config flag (`tts.to("cuda")`).

## Test

No test suite exists. There is no `tests/` directory and no test runner configured. The module `__main__` block is ad-hoc manual scripting (and contains hardcoded local paths), not a test harness.

## Lint/Typecheck

None configured.

## Layout

- `ovos_tts_plugin_coqui/__init__.py` — all four plugin classes:
  - `CoquiTTSPlugin` — loads arbitrary Coqui pretrained model IDs or local checkpoints; `LANG2MODEL` maps lang -> preferred model id; `_MODELS` is a class-level model cache; handles multi-speaker/multi-lingual model dispatch.
  - `CoquiXTTSPlugin` — thin wrapper delegating to `CoquiTTSPlugin` pinned to `xtts_v2`; 17 supported langs.
  - `CoquiFreeVCTTS` — loads a base OVOS TTS plugin via `load_tts_plugin`, synthesizes, then applies `freevc24` voice conversion to a `reference_speaker` wav.
  - `CoquiFairSeqTTSPlugin` — per-language `tts_models/{alpha3}/fairseq/vits` MMS models; alpha3 derived via `langcodes.Language`.
  - `standardize_lang_tag()` — langcodes-based tag normalization helper.
- `setup.py` — packaging; entry points under group **`mycroft.plugin.tts`** (the OVOS/OPM TTS plugin group).
- `requirements.txt`, `version.py`, `CHANGELOG.md`, `renovate.json`.

Companion: STT side is `ovos-stt-plugin-mms` (same MMS models).

## Conventions (org hard rules)

- Branches: work on `dev`, stable is `master`. NEVER use `main`.
- Never edit `ovos_tts_plugin_coqui/version.py` — gh-automations bumps semver from conventional-commit prefixes (`feat:`/`fix:`/`feat!:`).
- New repos private by default; do not make source public without asking.
- Commit identity: JarbasAi <jarbasai@mailfence.com>.
- Reference reusable workflows from gh-automations at `@dev`.
- No Neon / `neon-*` references. (Note: `@NeonGeckoCom` strings in the README model table are upstream Coqui model-author attributions, not plugin dependencies.)
- No meta-commentary in docs/commits/code (no history, no dates).
- CI is provided by gh-automations reusable workflows.

## Gotchas

- Packaging uses `setup.py` (no `pyproject.toml`). Classifiers still list Python 2.x / 3.0-3.6 — stale.
- Workflows reference `TigreGotico/gh-automations/...@master`, not `OpenVoiceOS/gh-automations@dev`.
- `.github/workflows/build_tests.yml` is hand-rolled (not the standard gh-automations build-tests) and has a YAML indentation error in the "Build Source Packages" step plus an irrelevant core-install step — it does not actually exercise this plugin.
- `CoquiTTSPlugin.get_tts` has a dead/broken `use_freeVC` branch: it calls `tts.tts_with_vc_to_file(pt, ...)` where `pt` is undefined and a hardcoded `/home/miro/...` speaker_wav path. Real voice conversion lives in `CoquiFreeVCTTS`.
- `_MODELS` is a class attribute (shared across instances); model selection is keyed by lang, so two plugins for different model ids on the same lang can collide.
- `ovos_tts_plugin_coqui.egg-info/` build artifact is committed.
