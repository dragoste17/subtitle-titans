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
logging.basicConfig(format=logging_format)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
# file_sh = logging.FileHandler('./debug.log')
# file_sh.setFormatter(logging.Formatter(logging_format))


def initialize_client() -> DeepgramClient:
    """
    Load the api key and initialize a deepgram-client.

    Returns:
        deepgram_client (DeepgramClient): DeepgramClient instance.
    """
    api_key = os.environ.get('DEEPGRAM_API_KEY', "")
    assert api_key, 'Failure retrieving API key.'
    config: DeepgramClientOptions = DeepgramClientOptions(
        verbose=verboselogs.SPAM,
    )
    return DeepgramClient(api_key, config)


def initialize_client_options() -> PrerecordedOptions:
    """
    Initialize the options for a pre-recorded transcription service.

    Returns:
        options (PrerecordedOptions): PrerecordedOptions instance.
    """
    return PrerecordedOptions(
        model="nova-2",
        smart_format=True,
        utterances=True,
        punctuate=True,
        diarize=True,
    )


def prepare_payload(audio_filename: str):
    """
    Prepare the payload with the audio data to transcribe.

    Args:
        audio_filename (str): file-path of the audio file to send to deepgram.

    Returns:
        payload (dict): dictionary containing the file data.
    """
    audio_filepath = os.path.join('./audio_files', audio_filename)
    if not os.path.isfile(audio_filepath):
        logger.error(f"The audio file: {audio_filepath} does not exist.")
        raise FileNotFoundError(f'{audio_filepath} is not a file.')

    with open(audio_filepath, "rb") as file:
        buffer_data = file.read()
    logger.info(f"{audio_filepath} read in, preparing to send to deepgram.")
    payload: FileSource = {"buffer": buffer_data}
    return payload


def deepgram_transcribe(audio_filename):
    deepgram_client = initialize_client()
    options = initialize_client_options()
    try:
        payload = prepare_payload(audio_filename)
    except FileNotFoundError as e:
        logger.error(f"An audio file: {audio_filename} does not exist, preparing the deepgram payload has failed."
                     f"Exception: {e}")
        raise e

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
    deepgram_transcribe('./server/57196.mp3')
