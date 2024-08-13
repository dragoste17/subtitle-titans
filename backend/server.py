import os
import json
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from deepgram_transcribe import deepgram_transcribe
from utils import write_json, read_json, write_string_to_file, sentences_to_srt
from models import AudioFile, TranscriptionFile
from fastapi.responses import FileResponse

logging_format = "Module: %(name)s\tFilename: %(filename)s:%(lineno)d\tFunction: %(funcName)s" \
                 "\n\t%(levelname)s: %(message)s"
logging.basicConfig(format=logging_format)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
# file_sh = logging.FileHandler('./debug.log')
# file_sh.setFormatter(logging.Formatter(logging_format))

description = """
Subtitle-Titans API uses Deepgram to generate an automated transcription of an audio file.
Later you can generate an .srt file from that description. 🚀

 * Upload an mp3 file.
 * Generate a transcription file.
   * If a transcription file of the same name is already contained on the server, then that transcription will be used.
 * Generate an srt file.
"""

app = FastAPI(
    title="Subtitle Titans",
    description=description,
    summary="Make subtitles perfect, make em fast.",
    version="0.1.0",
    terms_of_service="http://www.example.com",
    contact={
        "name": "Matt J. Lav S.",
        "url": "http://www.example.com",
        "email": "noone@example.com",
    },
    license_info={
        "name": "Proprietary",
        "url": "http://www.example.com",
    },
)

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
    """
    Upload an audio file to later be transcribed.

    Call with a post command:
        key: file - value: <mp3 audio file>

    Args:

    **file** (UploadFile): the audio file to be uploaded.

    Example Request:

        {
            "file": <binary data-file>
        }

    Returns:

    **message** simply reports whether the process was successful or not.

    Example Response:

        {
            "message": "Successfully uploaded 57196_256br.mp3"
        }
    """
    audio_filepath = os.path.join('./audio_files', file.filename)
    file_on_server = os.path.isfile(audio_filepath)
    if file_on_server:
        logger.warning(f"File: {audio_filepath} already exists on the server, and will be overwritten.")
        # return {"message": f"A file named: {audio_filepath} already exists, please use a different filename."}

    logger.info(f"Saving file: {audio_filepath}.")
    try:
        contents = file.file.read()
        with open(audio_filepath, 'wb') as f:
            f.write(contents)
    except Exception as e:
        logger.error(f"Exception raised: {e}")
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    logger.info(f"{audio_filepath} saved.")
    return {"message": f"Successfully uploaded {file.filename}"}


@app.post("/transcribe/")
def transcribe(audio: AudioFile):
    """
    Transcribe an audio file contained on the server. If the file has already been transcribed, then the existing
    transcription will be used. Otherwise, the audio file is sent to the *Deepgram* API for transcription.

    Args:

    audio (AudioFile): a json object containing a filename to an audio file.
    The audio file needs to have been uploaded to the server via the /upload endpoint.

        {
            "filename": <name of audio file to transcribe>
        }

    Example Request:

        {
            "filename": "57196_256br.mp3"
        }

    Returns:

        {
            "sentences": sentences,
            "transcription_file_on_server": transcription_file_on_server,
            "message": "Success"
        }

    **sentences** is a list of json dictionaries.

        [
            {
                "text": "And, the engineers from other companies to join.",
                "start": 0.79999995,
                "end": 3.6999998
            },
            {
                "text": "And another one will not be this winter.",
                "start": 3.84,
                "end": 6.02
            }
        ]

    **transcription_file_on_server** is a boolean flag, True, if the file has already been transcribed and is on the
    server. False if the file is new, and thus being sent to Deepgram for transcription.

    **message** simply reports whether the process was successful or not.

    Example response:

        {
            "sentences": [
                {
                    "text": "And, the engineers from other companies to join.",
                    "start": 0.79999995,
                    "end": 3.6999998
                },
                {
                    "text": "And another one will not be this winter.",
                    "start": 3.84,
                    "end": 6.02
                }
            ],
            "transcription_file_on_server": False,
            "message": "Success"
        }

    """
    transcription_filename = os.path.join('./transcriptions', Path(audio.filename).stem + '.json')
    transcription_file_on_server = os.path.isfile(transcription_filename)

    if transcription_file_on_server:
        json_transcription = read_json(transcription_filename)
        logger.info(f"{transcription_filename} exists in data, read locally from server.")
    else:
        try:
            transcription = deepgram_transcribe(audio.filename)
        except FileNotFoundError as e:
            logger.error(f"Deepgram transcription has failed. The server does not contain an audio file: "
                         f"{audio.filename}. Exception: {e}")
            return {"sentences": {},
                    "message": f"The audio file: {audio.filename} does not exist on the server. Try calling /upload "
                               f"first.",
                    "transcription_file_on_server": transcription_file_on_server}
        json_transcription = json.loads(transcription)
        logger.info(f"New file: {transcription_filename}, calling to Deepgram for transcription.")

    write_json(transcription_filename, json_transcription)
    sentences = json_transcription["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"][0][
        "sentences"]
    return {"sentences": sentences, "transcription_file_on_server": transcription_file_on_server,
            "message": "Success"}


@app.post("/srt/")
def srt(transcription: TranscriptionFile):
    """
    Converts a transcription file (.json) to an SRT-file (.srt).

    Args:

    transcription (TranscriptionFile): a json object containing a filename.

        {
            "filename": <name of transcription file to convert to srt>
        }

    Example Request:

        {
            "filename": "57196_256br.json"
        }

    Returns:

    An SRT-file.
    """
    if Path(transcription.filename).suffix != '.json':
        return {"message": "transcription files must be .json"}

    transcription_data = read_json(os.path.join('./transcriptions', transcription.filename))
    sentences = transcription_data["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"][0][
        "sentences"]
    output_filepath = os.path.join('./srt', Path(transcription.filename).stem + '.srt')
    write_string_to_file(output_filepath, sentences_to_srt(sentences))
    return FileResponse(path=output_filepath, filename=Path(transcription.filename).stem + '.srt',
                        media_type='text/plain')
