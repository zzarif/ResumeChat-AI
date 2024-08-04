from fastapi import UploadFile
from typing import List
import aiofiles
import os


# Function to save uploaded files
async def save_uploaded_files(files: List[UploadFile]):
    saved_files = []

    # Create the directory if it doesn't exist
    save_dir = os.path.join(os.path.dirname(__file__), 'pdfs')
    os.makedirs(save_dir, exist_ok=True)

    for uploaded_file in files:
        file_path = os.path.join(save_dir, uploaded_file.filename)
        try:
            async with aiofiles.open(file_path, "wb") as buffer:
                content = await uploaded_file.read()
                await buffer.write(content)
            saved_files.append(uploaded_file.filename)
        except IOError:
            return False, f"Error saving file: {uploaded_file.filename}"
    return True, saved_files
