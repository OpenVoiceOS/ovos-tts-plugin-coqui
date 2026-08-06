# Coqui TTS served through ovos-tts-server's ElevenLabs-compatible API.
#
# Runs the plugin behind ovos-tts-server on a CPU-only base. The Coqui models are
# multi-GB and download on first use into the mounted cache volume (TTS_HOME), so
# they are not baked into the image.
FROM python:3.14-slim

# System deps: libsndfile1 (soundfile), git/build tooling for any source wheels.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libsndfile1 \
        git \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# the plugin + Coqui runtime + the OVOS TTS server.
# - CPU-only torch first so the multi-GB CUDA wheels never land in this CPU image.
# - torch<2.9 avoids coqui-tts's torchcodec audio-IO requirement (PyTorch 2.9 drops
#   the torchaudio codepath coqui relies on; without torchcodec every coqui entry
#   point fails to load and the server reports "unknown plugin").
# - setuptools<81 keeps ovos-plugin-manager's pkg_resources usage working.
# - ovos-tts-server>=1.13.5a1 alpha floor lets pip resolve the prerelease without --pre.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "torch<2.9" "torchaudio<2.9" --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir "setuptools<81" "." "ovos-tts-server>=1.13.5a1"

# Default synthesis language, overridable with the COQUI_LANG build arg. The plugin
# maps the language to a Coqui model (see LANG2MODEL); pass a "model" in mycroft.conf
# to pick a specific one.
ARG COQUI_LANG=en
RUN useradd -m -u 1000 ovos \
    && mkdir -p /home/ovos/.config/mycroft \
    && printf '{\n  "lang": "%s",\n  "tts": {\n    "module": "ovos-tts-plugin-coqui",\n    "ovos-tts-plugin-coqui": {\n      "lang": "%s"\n    }\n  }\n}\n' "${COQUI_LANG}" "${COQUI_LANG}" \
        > /home/ovos/.config/mycroft/mycroft.conf \
    && chown -R 1000:1000 /home/ovos/.config

# Coqui downloads models here; keep it under the mounted cache volume so the
# multi-GB weights are fetched only once.
ENV TTS_HOME=/home/ovos/.cache/coqui
USER 1000

EXPOSE 9666
ENTRYPOINT ["ovos-tts-server", "--engine", "ovos-tts-plugin-coqui", \
            "--host", "0.0.0.0", "--port", "9666", "--cache"]
