# OVOS TTS Plugin Coqui

## Description

OVOS TTS plugin for [Coqui TTS](https://coqui-tts.readthedocs.io/en/latest)

This repository provides 4 plugins:
- `"ovos-tts-plugin-coqui"` - load arbitrary coqui models (see list below)
- `"ovos-tts-plugin-coqui-xtts"` - XTTS-v2 is a multilingual model supporting 17 languages and voice cloning
- `"ovos-tts-plugin-coqui-freevc"` - [FreeVC](https://github.com/OlaWod/FreeVC) uses a base OVOS TTS plugin and applies Voice Conversion on top, infinite voices for your existing plugins!
- `"ovos-tts-plugin-coqui-fairseq"` - supports [1127 languages](https://dl.fbaipublicfiles.com/mms/tts/all-tts-languages.html)


## Install

`pip install ovos-tts-plugin-coqui`

## Configuration

### **ovos-tts-plugin-coqui**

if `"model"` is not set it will be automatically selected based on language

```json
  "tts": {
    "module": "ovos-tts-plugin-coqui",
    "ovos-tts-plugin-coqui": {}
  }
 
```

you can set a specific model id to use pretrained models (see full list below), some models accept a `"voice"` (often also called a "speaker" in each model)
```json
  "tts": {
    "module": "ovos-tts-plugin-coqui",
    "ovos-tts-plugin-coqui": {
      "model": "tts_models/en/vctk/XXX",
      "voice": "p232"
    }
  }
 
```
you can also set a model from a path, optionally with a vocoder if the mode architecture needs it

```json
  "tts": {
    "module": "ovos-tts-plugin-coqui",
    "ovos-tts-plugin-coqui": {
      "model": "full/path/to/model.ckpt",
      "model_config": "full/path/to/model_config.json",
      "vocoder": "full/path/to/vocoder.ckpt",
      "vocoder_config": "full/path/to/vocoder_config.json"
    }
  }
 
```

### **ovos-tts-plugin-coqui-fairseq**

[1127 supported languages](https://dl.fbaipublicfiles.com/mms/tts/all-tts-languages.html) using models from [The Massively Multilingual Speech (MMS) project](https://huggingface.co/docs/transformers/main/en/model_doc/mms)

The equivalent STT models can be used via [ovos-stt-plugin-mms](https://github.com/OpenVoiceOS/ovos-stt-plugin-mms) companion plugin

```json
  "tts": {
    "module": "ovos-tts-plugin-coqui-fairseq",
    "ovos-tts-plugin-coqui-fairseq": {}
  }
 
```

### **ovos-tts-plugin-coqui-xtts**

supported langs: `"ar"`, `"zh"`, `"cs"`, `"nl"`, `"en"`, `"fr"`, `"de"`, `"hi"`, `"hu"`, `"it"`, `"ja"`, `"ko"`, `"pl"`, `"pt"`, `"ru"`, `"es"`, `"tr"`
```json
  "tts": {
    "module": "ovos-tts-plugin-coqui-xtts",
    "ovos-tts-plugin-coqui-xtts": {
      "reference_speaker": "/path/to/voice/to/be/cloned.wav"
    }
  }
 
```
`"reference_speaker"` (optional) can be used for voice cloning

### **ovos-tts-plugin-coqui-freevc**

Use any audio sample as reference, voice conversion will be applied on top of any existing OVOS plugins
```json
  "tts": {
    "module": "ovos-tts-plugin-coqui-freevc",
    "ovos-tts-plugin-coqui-freevc": {
      "tts_module": "ovos-tts-plugin-XXX",
      "reference_speaker": "/path/to/voice/to/be/cloned.wav",
      "voice": "overrides-ovos-tts-plugin-XXX"
    },
    "ovos-tts-plugin-XXX": {
      "voice": "XXX"
    }
  }
 
```
- `"reference_speaker"` - voice to be cloned
- `"tts_module"` - base plugin to generate audio 

> **WARNING**: the configuration section for `"ovos-tts-plugin-coqui-freevc"` takes precedence over fields from the selected base plugin

### Supported Models

#### Overflow TTS

Neural HMMs are a type of neural transducer recently proposed for sequence-to-sequence modelling in text-to-speech. 
They combine the best features of classic statistical speech synthesis and modern neural TTS

```python
# {'model_id': 'tts_models/en/ljspeech/overflow', 'lang': 'en', 'author': 'Eren Gölge @erogol', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/en/ljspeech/neural_hmm', 'lang': 'en', 'author': 'Shivam Metha @shivammehta25', 'license': 'apache 2.0'}
```

#### Forward TTS model(s)

- **FastSpeech:** It’s a feed-forward model TTS model that uses Feed Forward Transformer (FFT) modules as the encoder and decoder.
- **FastPitch:** It uses the same FastSpeech architecture that is conditioned on fundamental frequency (f0) contours with the promise of more expressive speech.
- **SpeedySpeech:** It uses Residual Convolution layers instead of Transformers that leads to a more compute friendly model.

```python
# {'model_id': 'tts_models/en/ljspeech/fast_pitch', 'lang': 'en', 'author': 'Eren Gölge @erogol', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/en/vctk/fast_pitch', 'lang': 'en', 'author': 'Eren @erogol', 'license': 'CC BY-NC-ND 4.0'}
# {'model_id': 'tts_models/en/ljspeech/speedy-speech', 'lang': 'en', 'author': 'Eren Gölge @erogol', 'license': 'apache 2.0'}
```

#### XTTS

ⓍTTS lets you clone voices in different languages by using just a quick 3-second audio clip.

XTTS-v2 supports **17 languages**: Arabic (ar) Chinese (zh-cn) Czech (cs) Dutch (nl) English (en) French (fr) German (de) Hindi (hi) Hungarian (hu)  Italian (it) Japanese (ja) Korean (ko)  Polish (pl)  Portuguese (pt)  Russian (ru) Spanish (es)  Turkish (tr)

```python
# {'model_id': 'tts_models/multilingual/multi-dataset/xtts_v2', 'lang': 'multilingual', 'author': '?', 'license': 'CPML'}
# {'model_id': 'tts_models/multilingual/multi-dataset/xtts_v1.1', 'lang': 'multilingual', 'author': '?', 'license': 'CPML'}
```

#### Tacotron

Tacotron mainly is an encoder-decoder model with attention. The encoder takes input tokens (characters or phonemes) and the decoder outputs mel-spectrogram* frames. Attention module in-between learns to align the input tokens with the output mel-spectrgorams.

```python
# {'model_id': 'tts_models/en/ek1/tacotron2', 'lang': 'en', 'author': '?', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/en/ljspeech/tacotron2-DDC', 'lang': 'en', 'author': 'Eren Gölge @erogol', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/en/ljspeech/tacotron2-DDC_ph', 'lang': 'en', 'author': 'Eren Gölge @erogol', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/en/ljspeech/tacotron2-DCA', 'lang': 'en', 'author': 'Eren Gölge @erogol', 'license': 'MPL'}
# {'model_id': 'tts_models/en/sam/tacotron-DDC', 'lang': 'en', 'author': 'Eren Gölge @erogol', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/es/mai/tacotron2-DDC', 'lang': 'es', 'author': 'Eren Gölge @erogol', 'license': 'MPL'}
# {'model_id': 'tts_models/fr/mai/tacotron2-DDC', 'lang': 'fr', 'author': 'Eren Gölge @erogol', 'license': 'MPL'}
# {'model_id': 'tts_models/zh-CN/baker/tacotron2-DDC-GST', 'lang': 'zh-CN', 'author': '@kirianguiller', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/nl/mai/tacotron2-DDC', 'lang': 'nl', 'author': '@r-dh', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/de/thorsten/tacotron2-DCA', 'lang': 'de', 'author': '@thorstenMueller', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/de/thorsten/tacotron2-DDC', 'lang': 'de', 'author': '@thorstenMueller', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/ja/kokoro/tacotron2-DDC', 'lang': 'ja', 'author': '@kaiidams', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/en/blizzard2013/capacitron-t2-c50', 'lang': 'en', 'author': 'Adam Froghyar @a-froghyar', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/en/blizzard2013/capacitron-t2-c150_v2', 'lang': 'en', 'author': 'Adam Froghyar @a-froghyar', 'license': 'apache 2.0'}
```

#### Glow TTS

Glow TTS is a normalizing flow model for text-to-speech. It is built on the generic Glow model that is previously used in computer vision and vocoder models. It uses “monotonic alignment search” (MAS) to fine the text-to-speech alignment and uses the output to train a separate duration predictor network for faster inference run-time.

```python
# {'model_id': 'tts_models/en/ljspeech/glow-tts', 'lang': 'en', 'author': 'Eren Gölge @erogol', 'license': 'MPL'}
# {'model_id': 'tts_models/uk/mai/glow-tts', 'lang': 'uk', 'author': '@robinhad', 'license': 'MIT'}
# {'model_id': 'tts_models/tr/common-voice/glow-tts', 'lang': 'tr', 'author': 'Fatih Akademi', 'license': 'MIT'}
# {'model_id': 'tts_models/it/mai_female/glow-tts', 'lang': 'it', 'author': '@nicolalandro', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/it/mai_male/glow-tts', 'lang': 'it', 'author': '@nicolalandro', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/fa/custom/glow-tts', 'lang': 'fa', 'author': '@karim23657', 'license': 'CC-BY-4.0'}
# {'model_id': 'tts_models/be/common-voice/glow-tts', 'lang': 'be', 'author': '?', 'license': 'CC-BY-SA 4.0'}
```

#### VITS

VITS (Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech ) is an End-to-End (encoder -> vocoder together) TTS model that takes advantage of SOTA DL techniques like GANs, VAE, Normalizing Flows. The model architecture is a combination of GlowTTS encoder and HiFiGAN vocoder.

```python
# {'model_id': 'tts_models/bg/cv/vits', 'lang': 'bg', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/cs/cv/vits', 'lang': 'cs', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/da/cv/vits', 'lang': 'da', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/et/cv/vits', 'lang': 'et', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/ga/cv/vits', 'lang': 'ga', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/en/ljspeech/vits', 'lang': 'en', 'author': 'Eren Gölge @erogol', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/en/ljspeech/vits--neon', 'lang': 'en', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/en/vctk/vits', 'lang': 'en', 'author': 'Eren @erogol', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/es/css10/vits', 'lang': 'es', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/fr/css10/vits', 'lang': 'fr', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/uk/mai/vits', 'lang': 'uk', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/nl/css10/vits', 'lang': 'nl', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/de/thorsten/vits', 'lang': 'de', 'author': '@thorstenMueller', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/de/css10/vits-neon', 'lang': 'de', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/it/mai_female/vits', 'lang': 'it', 'author': '@nicolalandro', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/it/mai_male/vits', 'lang': 'it', 'author': '@nicolalandro', 'license': 'apache 2.0'}
# {'model_id': 'tts_models/ewe/openbible/vits', 'lang': 'ewe', 'author': '@coqui_ai', 'license': 'CC-BY-SA 4.0'}
# {'model_id': 'tts_models/hau/openbible/vits', 'lang': 'hau', 'author': '@coqui_ai', 'license': 'CC-BY-SA 4.0'}
# {'model_id': 'tts_models/lin/openbible/vits', 'lang': 'lin', 'author': '@coqui_ai', 'license': 'CC-BY-SA 4.0'}
# {'model_id': 'tts_models/tw_akuapem/openbible/vits', 'lang': 'tw_akuapem', 'author': '@coqui_ai', 'license': 'CC-BY-SA 4.0'}
# {'model_id': 'tts_models/tw_asante/openbible/vits', 'lang': 'tw_asante', 'author': '@coqui_ai', 'license': 'CC-BY-SA 4.0'}
# {'model_id': 'tts_models/yor/openbible/vits', 'lang': 'yor', 'author': '@coqui_ai', 'license': 'CC-BY-SA 4.0'}
# {'model_id': 'tts_models/hu/css10/vits', 'lang': 'hu', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/el/cv/vits', 'lang': 'el', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/fi/css10/vits', 'lang': 'fi', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/hr/cv/vits', 'lang': 'hr', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/lt/cv/vits', 'lang': 'lt', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/lv/cv/vits', 'lang': 'lv', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/mt/cv/vits', 'lang': 'mt', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/pl/mai_female/vits', 'lang': 'pl', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/pt/cv/vits', 'lang': 'pt', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/ro/cv/vits', 'lang': 'ro', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/sk/cv/vits', 'lang': 'sk', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/sl/cv/vits', 'lang': 'sl', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/sv/cv/vits', 'lang': 'sv', 'author': '@NeonGeckoCom', 'license': 'bsd-3-clause'}
# {'model_id': 'tts_models/ca/custom/vits', 'lang': 'ca', 'author': '@gullabi', 'license': 'CC-BY-4.0'}
# {'model_id': 'tts_models/bn/custom/vits-male', 'lang': 'bn', 'author': '@mobassir94', 'license': 'Apache 2.0'}
# {'model_id': 'tts_models/bn/custom/vits-female', 'lang': 'bn', 'author': '@mobassir94', 'license': 'Apache 2.0'}
```

## Credits

<img src="img.png" width="128"/>

> This plugin was funded by the Ministerio para la Transformación Digital y de la Función Pública and Plan de Recuperación, Transformación y Resiliencia - Funded by EU – NextGenerationEU within the framework of the project ILENIA with reference 2022/TL22/00215337
