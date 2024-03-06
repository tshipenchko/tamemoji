import os
import uuid

import aiofiles
from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from ai.model import EmojiClassifier
from config import config

classifier = EmojiClassifier(config.classifier)
classifier.load(config.model_name)

EMOJIS = {
    "smile",
    "sad",
    "angry",
    "laugh",
    "cry",
    "shock",
}

app = FastAPI()

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


async def write_file(directory, filename, contents):
    os.makedirs(directory, exist_ok=True)
    async with aiofiles.open(f"{directory}/{filename}", "wb") as f:
        await f.write(contents)


@app.post("/send/{emoji}")
def send_file(emoji: str, file: UploadFile = Form(...)):
    contents = file.file.read()

    with open("/home/user/tmp/test.png", "wb") as f:
        f.write(contents)

    # Resize the image to classifier's input size
    image = classifier.resize_image(contents)
    predictions, answer = classifier.predict(image)

    return {
        "message": f"I think, it's a {answer}", "predictions": predictions
    }


@app.post("/upload/{emoji}")
async def upload_file(emoji: str, file: UploadFile = Form(...)):
    directory = f"dataset/{emoji}"
    filename = f"{uuid.uuid4().hex}.png"
    contents = await file.read()
    await write_file(directory, filename, contents)
    return {"file_size": len(contents)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
