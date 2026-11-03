import os
import shutil
import uuid

from fastapi import UploadFile

def save_file(file : UploadFile, directory : str):
    upload_file = os.path.join("images/upload", directory)
    os.makedirs(upload_file, exist_ok=True)

    file_name = f"{uuid.uuid4()}{file.filename}"
    file_path = os.path.join(upload_file, file_name)

    with open(file_path, "wb") as record:
        shutil.copyfileobj(file.file, record)

    return file_path


def delete_file(file_url : str, directory : str):
    delete_file = os.path.join("images/delete", directory)
    os.makedirs(delete_file, exist_ok=True)

    file_name = os.path.basename(file_url)
    destination = os.path.join(delete_file, file_name)

    shutil.move(file_url, destination)
