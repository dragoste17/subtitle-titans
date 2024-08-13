from pydantic import BaseModel


class AudioFile(BaseModel):
    filename: str


class TranscriptionFile(BaseModel):
    filename: str
