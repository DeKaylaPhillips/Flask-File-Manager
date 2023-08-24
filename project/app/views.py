import os
from flask import request, jsonify
from app import db
from sqlalchemy import select
from app.models import Files
from app.controllers.db_handler import DBHandler
from app.services.file_handler import FileHandler
from .services.validator import Validator
from .services.formatting import Formatter
from dotenv import load_dotenv
load_dotenv()


def register(app):
    @app.route('/files', methods=['GET'])
    def get_all_files():
        files = db.session.execute(select(Files)).scalars().all()
        if not files:
            return jsonify({"success": False, "data": "No existing files in database records."})
        data = [
            {
                "id": file.id,
                "name": file.name,
                "date_created": file.date_created,
                "date_modified": file.date_modified,
                "extension": file.extension,
                "path": f"files/{file.name}",
                "headers": file.headers
            } for file in files
        ]
        return jsonify({"success": True, "data": data})

    @app.route('/files', methods=['POST'])
    def create_file_with_headers():
        data = request.get_json()
        if 'name' not in data:
            return jsonify({"success": False, "data": "No file name specified in request."})
        filename = data['name']
        name, extension = os.path.splitext(filename)
        extension = extension[1:]
        if 'headers' not in data:
            return jsonify({"success": False, "data": "Headers are required for csv files."})
        headers = data['headers']

        try:
            file_handler = FileHandler(Validator, Formatter)
            db_handler = DBHandler(Formatter)
            file_handler.create_csv_file(filename=filename, headers=headers)
            db_handler.create_record(
                filename=name, extension=extension, headers=headers)
            return jsonify({"success": True, "data": f"File '{name}.{extension}' created successfully."})
        except Exception as e:
            return jsonify({"success": False, "data": f"File could not be created.", "error": str(e)})

    @app.route('/files/<int:file_id>', methods=['PUT'])
    def update_file_content(file_id):
        data = request.get_json()
        
        if 'content' not in data:
            return jsonify({"success": False, "data": "No file content specified in request."})
        
        file_record = db.session.execute(select(Files).where(Files.id == file_id)).scalars().one()
        if not file_record:
            return jsonify({"success": False, "data": f"File with ID {file_id} not found."})
        
        filename = f'{file_record.name}.{file_record.extension}'
        expected_headers = file_record.headers.split(",")
        content = data['content']
        
        try:
            file_handler = FileHandler(Validator, Formatter)
            file_handler.update(filename=filename, content_data=content, expected_headers=expected_headers)
            return jsonify({"success": True, "data": f"File with ID {file_id} successfully updated."})
        except Exception as e:
            return jsonify({"success": False, "data": f"File not found or content could not be updated.", "error": str(e)})

    @app.route('/files/<int:file_id>', methods=['GET'])
    def read_file_content(file_id):
        data = request.get_json()
        
        if 'name' not in data:
            return jsonify({"success": False, "data": "No file name supplied in request."}), 
        
        file_record = db.session.execute(select(Files).where(Files.id == file_id)).scalars().one()
        if not file_record:
            return jsonify({"success": False, "data": f"File with ID {file_id} not found.", })
        
        try:
            filename = f"{file_record.name}.{file_record.extension}"
            file_handler = FileHandler(Validator, Formatter)
            data = file_handler.read(filename=filename)
            return jsonify({"success": True, "data": data})
        except Exception as e:
            return jsonify({"success": False, "data": "File not found or content could not be read.", "error": str(e)})

    @app.route('/files/<int:file_id>', methods=['DELETE'])
    def delete_file(file_id):
        data = request.get_json()
        
        if 'name' not in data:
            return jsonify({"success": False, "data": f"No file name supplied in request."})
        
        file_record = db.session.execute(
            select(Files).where(Files.id == file_id)).scalars().one()
        if not file_record:
            return jsonify({"success": False, "data": f"File with ID {file_id} not found."})
        
        try:
            filename = f"{file_record.name}.{file_record.extension}"
            file_handler = FileHandler(Validator, Formatter)
            db_handler = DBHandler(Formatter)
            file_handler.delete(filename=filename)
            db_handler.delete_record(filename=file_record.name)
            return jsonify({"success": True, "data": f"File with ID {file_id} successfully deleted."})
        except Exception as e:
            return jsonify({"success": False, "data": "File not found or content could not be deleted.", "error": str(e)})
