export function disableContextMenu() {
  document.addEventListener("contextmenu", (event) => event.preventDefault());
}

export async function recordAudio(onTranscribe) {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.start();

  const audioChunks = [];
  mediaRecorder.addEventListener("dataavailable", (event) => {
    audioChunks.push(event.data);
  });

  mediaRecorder.addEventListener("stop", async () => {
    const audioBlob = new Blob(audioChunks);
    const text = await speechToText(audioBlob);
    onTranscribe(text);
  });

  return mediaRecorder;
}

// -----------------------------------------------------------------------------
// SERVER API CALLS
// -----------------------------------------------------------------------------

export async function askGpt(messages) {
  const response = await fetch("/gpt", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages }),
  });
  const text = await response.json();
  return text;
}

export async function speechToText(audioBlob) {
  const formData = new FormData();
  formData.append("file", audioBlob);

  const response = await fetch("/stt", { method: "POST", body: formData });
  const text = await response.json();
  return text;
}

export async function textToSpeech(text) {
  const response = await fetch("/tts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  const audioBlob = await response.blob();
  const audioUrl = URL.createObjectURL(audioBlob);
  const audio = new Audio(audioUrl);
  audio.play();
}
