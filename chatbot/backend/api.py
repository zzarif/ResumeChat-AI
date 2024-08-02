from fastapi import FastAPI, File, UploadFile
from docs.vectorizer import save_doc_to_vector_store
from streamer import stream_response
from fastapi.responses import StreamingResponse
from fastapi import status, HTTPException
from pydantic import BaseModel
import uvicorn


app = FastAPI()


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if save_doc_to_vector_store(file):
        return {'filename': file.filename}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'File {file.filename} could not be vectorized.',
        )


class ChatQuery(BaseModel):
    query: str


@app.post("/chat")
async def chat(chat_query: ChatQuery):
    return StreamingResponse(stream_response(chat_query.query), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000)
