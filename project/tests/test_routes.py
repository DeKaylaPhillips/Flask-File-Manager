def test_get_all_files_status_and_response(client, test_db_files, db_file_counter):
    expected_file_count = 3
    expected_file_names = list(file.name for file in test_db_files)

    response = client.get("/files")
    data = response.json
    actual_file_count = db_file_counter
    response_file_names = list(file["name"] for file in data["data"])

    assert response.status_code == 200
    assert data["success"] == True
    assert len(data["data"]) == 3
    assert expected_file_count == actual_file_count
    assert response_file_names == expected_file_names


def test_create_file_status_and_response(client, db_file_counter, mock_set):
    initial_file_count = db_file_counter

    response = client.post("/files", json={
        "name": "testFile.csv",
        "headers": ["Col1", "Col2", "Col3", "Col4"]
    })
    data = response.json
    updated_file_count = db_file_counter + 1

    assert response.status_code == 200
    assert data["success"] == True
    assert data["data"] == "File created successfully."
    assert initial_file_count != updated_file_count

def test_create_file_file_operations(client, mock_set):
    client.post("/files", json={
        "name": "testFile.csv",
        "headers": ["Col1", "Col2", "Col3", "Col4"]
    })

    mock_set["mock_open"].assert_called_with('files/testFile.csv', 'w')
    mock_set["write"].assert_called_once()

def test_read_file_status_and_response(client, test_db_files, mock_set):
    test_file_id = test_db_files[0].id
    test_file_name = test_db_files[0].name

    response = client.get(f"/files/{test_file_id}", json={
        "name": test_file_name
    })
    data = response.json

    assert response.status_code == 200
    assert data["success"] == True
    assert data["data"] is not None

def test_read_file_file_operations(client, mock_set, test_db_files):    
    test_file_id = test_db_files[0].id
    test_file_name = test_db_files[0].name
    test_file_ext = test_db_files[0].extension
    
    response = client.get(f"/files/{test_file_id}", json={
        "name": test_file_name
    })
    data = response.json
    content = [content for column in data["data"]
               for content in column.values()]
    formatted_content = ",".join(content) + "\n"
    
    assert mock_set["content"] == formatted_content
    mock_set["mock_open"].assert_called_with(
        f"files/{test_file_name}.{test_file_ext}", "r")
    
def test_update_file_status_and_response(client, test_db_files, mock_set):
    test_file_id = test_db_files[0].id

    response = client.put(f"/files/{test_file_id}", json={
        "content": [
            {"Col1": "ColContent1"},
            {"Col2": "ColContent2"},
            {"Col3": "ColContent3"},
            {"Col4": "ColContent4"}
        ]
    })
    data = response.json

    assert response.status_code == 200
    assert data["success"] == True
    assert data["data"] == "File content updated successfully."

def test_update_file_file_operations(client, mock_set, test_db_files):
    test_file_id = test_db_files[0].id

    client.put(f"/files/{test_file_id}", json={
        "content": [
            {"Col1": "ColContent1"},
            {"Col2": "ColContent2"},
            {"Col3": "ColContent3"},
            {"Col4": "ColContent4"}
        ]
    })

    mock_set["mock_open"].assert_called_with('files/testFile1.csv', 'a')
    mock_set["writelines"].assert_called_once()