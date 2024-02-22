from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/upload/smile")
async def upload_smile_image(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": file.filename}
