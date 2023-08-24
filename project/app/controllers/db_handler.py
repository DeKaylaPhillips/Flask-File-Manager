from app.models import Files
from app import db
from typing import Type
from sqlalchemy import select
import os

class Formatter:
    pass


class DBHandler:
    BASE_DIR = "files"

    def __init__(self, Formatter: Type[Formatter]) -> None:
        self.format = Formatter()

    def create_record(self, filename: str, extension: str, headers: list[str]) -> Files:
        file_path = os.path.join(DBHandler.BASE_DIR, filename)
        new_file = Files(path=file_path, name=filename, extension=extension)
        new_file.headers = self.format.get_csv_formatted_headers(
            headers).strip()
        db.session.add(new_file)
        db.session.commit()
        return new_file

    def delete_record(self, filename):
        results = db.session.execute(select(Files).where(Files.name == filename))
        file = results.scalars().one()
        
        if not file:
            raise FileNotFoundError(f"File '{filename}' does not exist.")
        db.session.delete(file)
        db.session.commit()        
