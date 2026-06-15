"""End-to-end TTS intelligibility test for ovos-tts-plugin-coqui.

Synthesises a small set of phrases with the real plugin, transcribes the
rendered audio back with a reference STT and scores the round-trip with
WER/CER via ovoscope. Report-only by default (TTS_MAX_WER=1.0).
"""
import os

from ovoscope.tts_intelligibility import score_tts_intelligibility

from ovos_tts_plugin_coqui import CoquiTTSPlugin

LANG = "en"
PHRASES = [
    "hello world",
    "what time is it",
    "the weather is nice today",
    "thank you very much",
    "see you later",
]


def test_tts_intelligibility():
    tts = CoquiTTSPlugin({"lang": LANG})
    report = score_tts_intelligibility(tts, PHRASES, lang=LANG, mode="playback")
    print(f"::TTS-INTELLIGIBILITY:: {report.to_dict()}")
    assert report.mean_wer <= float(os.environ.get("TTS_MAX_WER", "1.0"))
