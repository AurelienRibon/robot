import openai
import os
import pydub
from google.cloud import texttospeech
from .utils import log, suid, timer, tmp_file

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "googlecloud.json"

# ------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------


def text_to_speech(text):
    tick = timer()
    path = tmp_file("tts", "mp3")

    log("[tts] Converting text to audio file...", tick)
    _tts_googlecloud(text, path)

    log("[tts] Mutating audio...", tick)
    audio = pydub.AudioSegment.from_mp3(path)
    audio = audio._spawn(
        audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * 0.8)}
    )
    audio = audio.speedup(playback_speed=1.2)
    audio.export(path, format="mp3")

    log("[tts] Done.", tick)
    return path


def speech_to_text(path):
    tick = timer()

    log("[stt] Converting audio file to text...", tick)
    text = _stt_openai(path)

    log("[stt] Done. text: " + text, tick)
    return text


def ask_gpt(chat, model="gpt-4"):
    tick = timer()

    log("[gpt] Asking OpenAI...", tick)
    messages = [{"role": "system", "content": chat[0]}]
    role = "user"

    for content in chat[1:]:
        messages.append({"role": role, "content": content})
        role = "user" if role == "assistant" else "assistant"

    response = openai.ChatCompletion.create(model=model, messages=messages)
    reply = response["choices"][0]["message"]["content"]

    log("[gpt] Done.", tick)
    return reply


# ------------------------------------------------------------------------------
# IMPLEMENTATIONS
# ------------------------------------------------------------------------------


def _tts_googlecloud(text, path):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="fr-FR", name="fr-FR-Neural2-B"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(path, "wb") as out:
        out.write(response.audio_content)


def _stt_openai(path):
    with open(path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file, language="fr")
    return transcript["text"]
