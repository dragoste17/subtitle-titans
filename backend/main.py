import os.path

from fastapi import FastAPI
from fastapi import File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from deepgram_transcribe import main
from time_converter import convert_seconds_to_timestamp
import json
import logging

logging_format = "Module: %(name)s\tFilename: %(filename)s:%(lineno)d\tFunction: %(funcName)s" \
                 "\n\t%(levelname)s: %(message)s"
logging.basicConfig(format=logging_format)  # 標準出力のフォーマットは、loggingで設定
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
file_sh = logging.FileHandler('./debug.log')  # ログファイルに出力するHandlerの設定
file_sh.setFormatter(logging.Formatter(logging_format))

app = FastAPI()
origins = ["http://localhost:3000"]  # Replace with your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}


class AudioDataModel(BaseModel):
    audio_filename: str
    transcription_filename: str


def write_json(filename, data):
    with open(filename, "w", encoding="utf8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    logger.info(f"{filename} written to file.")


def read_json(filename):
    assert os.path.isfile(filename), f"{filename} does not exist."
    with open(filename, "r", encoding="utf8") as file:
        data = json.load(file)
    logger.info(f"{filename} read in.")
    return data

def write_string_to_file(filename, contents):
    with open(filename, 'w', encoding='utf8') as file:
        file.write(contents)
    logger.info(f'{filename} has been written.')


@app.post("/transcribe/")
def transcribe(audio: AudioDataModel):
    """

    """
    transcription = main(audio.audio_filename)
    json_transcription = json.loads(transcription)
    write_json(audio.transcription_filename, json_transcription)
    sentences = json_transcription["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"][0]["sentences"]
    return sentences


class SrtInputData(BaseModel):
    input_filename: str
    output_filename: str


def sentences_to_srt(sentences_list):
    output = ""
    for sdx, sentence in enumerate(sentences_list):
        start_ts = convert_seconds_to_timestamp(sentence["start"])
        end_ts = convert_seconds_to_timestamp(sentence["end"])
        output += f"{sdx}\n{start_ts} --> {end_ts}\n{sentence['text']}\n\n"

    return output


@app.post("/srt/")
def srt(srt_input: SrtInputData):
    data = read_json(srt_input.input_filename)
    sentences = data["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"][0]["sentences"]
    srt_output = sentences_to_srt(sentences)
    write_string_to_file(srt_input.output_filename, srt_output)
    return {"sentences": sentences}
