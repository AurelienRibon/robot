import src.api as api
import src.utils as utils
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


class TTSInput(BaseModel):
    text: str


class GPTInput(BaseModel):
    messages: list[str]


app = FastAPI()


@app.post("/stt")
async def stt(file: UploadFile):
    path = utils.tmp_file("stt", "wav")
    utils.write_stream(file.file, path)
    return api.speech_to_text(path)


@app.post("/tts")
async def tts(data: TTSInput):
    path = api.text_to_speech(data.text)
    return FileResponse(path)


@app.post("/gpt")
async def gpt(data: GPTInput):
    return api.ask_gpt(data.messages)


app.mount("/", StaticFiles(directory="static", html=True), name="static")
