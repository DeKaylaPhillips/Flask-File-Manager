import pytest
from app import create_app, db
from app.models import Files
from datetime import datetime
from sqlalchemy import select


@pytest.fixture()
def app():
    app = create_app(config_name='TestingConfig')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()


@pytest.fixture(scope="function")
def client(app: create_app):
    return app.test_client()


@pytest.fixture(scope="function")
def db_session():
    db.session.begin_nested()
    yield db.session
    db.session.rollback()


@pytest.fixture(scope="function")
def mock_set(mocker):
    file_headers = "Col1,Col2,Col3,Col4\n"
    content = "Test1,Test2,Test3,Test4\n"
    mock_open = mocker.mock_open(read_data=f"{file_headers}{content}")
    write = mock_open.return_value.write
    writelines = mock_open.return_value.writelines
    mocker.patch('builtins.open', mock_open)
    mocker.patch('os.path.exists', return_value=True)

    mock = {
        "content": content,
        "file_headers": file_headers,
        "mock_open": mock_open,
        "write": write,
        "writelines": writelines
    }
    return mock


@pytest.fixture(scope="function")
def test_db_files(db_session):
    Files.query.delete()
    db_session.commit()
    files = [
        Files(
            name="testFile1",
            date_created=datetime(2023, 8, 21, 14, 29, 34, 126718),
            date_modified=datetime(2023, 8, 22, 14, 29, 34, 126727),
            extension="csv",
            path="files/testFile1.csv",
            headers='Col1,Col2,Col3,Col4\n'
        ),
        Files(
            name="testFile2",
            date_created=datetime(2023, 9, 23, 14, 29, 34, 126718),
            date_modified=datetime(2023, 9, 24, 14, 29, 34, 126727),
            extension="csv",
            path="files/testFile2.csv",
            headers='Col1.0,Col2.0,Col3.0,Col4.0\n'
        ),
        Files(
            name="testFile3",
            date_created=datetime(2023, 10, 25, 14, 29, 34, 126718),
            date_modified=datetime(2023, 10, 26, 14, 29, 34, 126727),
            extension="csv",
            path="files/testFile3.csv",
            headers='Col1.0,Col2.0,Col3.0,Col4.0\n'
        ),
    ]
    db_session.add_all(files)
    db_session.commit()
    return files


@pytest.fixture(scope="function")
def db_file_counter(db_session):
    return len(db_session.execute(select(Files)).scalars().all())
