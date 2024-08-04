from fastapi import FastAPI, File, UploadFile
from docs.uploader import save_uploaded_files
from docs.vectorizer import save_doc_to_vector_store
from fastapi.responses import JSONResponse, StreamingResponse
from streamer import stream_response, extension_response
from pydantic import BaseModel
from typing import List
import uvicorn


app = FastAPI()


@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    success, result = await save_uploaded_files(files)

    if not success:
        return JSONResponse(content={"status": "error", "message": result}, status_code=500)

    # Convert files to vector embeddings
    if save_doc_to_vector_store() is not None:
        return {"status": "success", "message": f"Files uploaded: {', '.join(result)}", "conversion_status": True}
    else:
        return {"status": "success", "message": f"Files uploaded: {', '.join(result)}", "conversion_status": False}


class ChatQuery(BaseModel):
    query: str


@app.post("/chat")
async def chat(chat_query: ChatQuery):
    return StreamingResponse(stream_response(chat_query.query), media_type="text/event-stream")


@app.post("/extension")
async def extension(ext_query: ChatQuery):
    return {'message': extension_response(ext_query.query)}


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000)
