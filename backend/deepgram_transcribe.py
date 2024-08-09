import os
# from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs
from datetime import datetime
import httpx

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    PrerecordedOptions,
    FileSource,
)

logging_format = "Module: %(name)s\tFilename: %(filename)s:%(lineno)d\tFunction: %(funcName)s" \
                 "\n\t%(levelname)s: %(message)s"
logging.basicConfig(format=logging_format)  # 標準出力のフォーマットは、loggingで設定
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
file_sh = logging.FileHandler('../../../server/debug.log')  # ログファイルに出力するHandlerの設定
file_sh.setFormatter(logging.Formatter(logging_format))


def initialize_client():
    api_key = os.environ.get('DEEPGRAM_API_KEY', "")
    assert api_key, 'Getting API key fucked up.'
    # STEP 1 Create a Deepgram client using the API key in the environment variables
    config: DeepgramClientOptions = DeepgramClientOptions(
        verbose=verboselogs.SPAM,
    )
    deepgram: DeepgramClient = DeepgramClient(api_key, config)
    return deepgram


def initialize_client_options():
    options: PrerecordedOptions = PrerecordedOptions(
        model="nova-2",
        smart_format=True,
        utterances=True,
        punctuate=True,
        diarize=True,
    )
    return options


def prepare_payload(audio_filename):
    """
    Call the transcribe_file method on the rest class
    """
    print(audio_filename)
    assert os.path.isfile(audio_filename), f'{audio_filename} is not a file.'
    with open(audio_filename, "rb") as file:
        buffer_data = file.read()

    payload: FileSource = {
        "buffer": buffer_data,
    }
    return payload


def main(audio_filename):
    deepgram_client = initialize_client()
    options = initialize_client_options()
    payload = prepare_payload(audio_filename)

    t0 = datetime.now()
    response = None
    try:
        response = deepgram_client.listen.rest.v("1").transcribe_file(
            payload, options, timeout=httpx.Timeout(300.0, connect=10.0)
        )
    except Exception as e:
        logger.error(f"Exception: {e}")
    t1 = datetime.now()
    difference = t1 - t0
    logger.info(f"Transcription time: {difference.seconds}")

    return response.to_json(indent=4)


if __name__ == "__main__":
    main('./server/57196.mp3')
