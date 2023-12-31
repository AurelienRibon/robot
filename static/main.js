import { Howl } from 'https://cdn.skypack.dev/howler@2.2.3?min';

export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function disableContextMenu() {
  document.addEventListener('contextmenu', (event) => event.preventDefault());
}

export async function setupRecorder() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  return new MediaRecorder(stream);
}

export function startRecorder(recorder, onTranscribe) {
  recorder.start();

  const chunks = [];
  const chunkListener = (event) => {
    chunks.push(event.data);
  };

  const stopListener = async () => {
    recorder.removeEventListener('dataavailable', chunkListener);
    recorder.removeEventListener('stop', stopListener);
    const audioBlob = new Blob(chunks);
    const text = await speechToText(audioBlob);
    onTranscribe(text);
  };

  recorder.addEventListener('dataavailable', chunkListener);
  recorder.addEventListener('stop', stopListener);
}

export function stopRecorder(recorder) {
  recorder.stop();
}

// -----------------------------------------------------------------------------
// SERVER API CALLS
// -----------------------------------------------------------------------------

export async function askGpt(messages) {
  const response = await fetch('/gpt', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages }),
  });
  const text = await response.json();
  return text;
}

export async function speechToText(audioBlob) {
  const formData = new FormData();
  formData.append('file', audioBlob);

  const response = await fetch('/stt', { method: 'POST', body: formData });
  const text = await response.json();
  return text;
}

export async function textToSpeech(text) {
  const response = await fetch('/tts', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });

  const blob = await response.blob();
  playAudioBlob(blob);
}

export function playAudioBlob(blob, format = 'mp3') {
  const url = URL.createObjectURL(blob);
  const sound = new Howl({ src: [url], format: [format] });
  sound.play();
}
