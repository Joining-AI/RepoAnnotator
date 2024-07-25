# 引入操作系统相关的功能，比如读取环境变量。
import os
# 引入unittest库中的mock工具，用于模拟对象的行为。
from unittest.mock import MagicMock
# 引入pytest库，这是一个用于编写测试的库。
import pytest
# 引入dropbox库中与文件元数据相关的类。
from dropbox.files import FileMetadata
# 引入我们自己定义的DropboxLoader类，它负责处理Dropbox上的文件加载。
from embedchain.loaders.dropbox import DropboxLoader

# 定义一个pytest的fixture，用于设置测试环境。
@pytest.fixture
def setup_dropbox_loader(mocker):
    # 模拟dropbox库中的Dropbox类，这样我们可以在测试中控制它的行为。
    mock_dropbox = mocker.patch("dropbox.Dropbox")
    # 创建一个MagicMock对象，用来模拟Dropbox实例。
    mock_dbx = mocker.MagicMock()
    # 设置模拟的Dropbox返回值为我们创建的模拟实例。
    mock_dropbox.return_value = mock_dbx

    # 设置环境变量，用于存储Dropbox的访问令牌，这在实际应用中是用来认证的。
    os.environ["DROPBOX_ACCESS_TOKEN"] = "test_token"
    # 创建一个DropboxLoader实例。
    loader = DropboxLoader()

    # 使用yield关键字，fixture可以提供一个临时的对象给测试函数使用。
    yield loader, mock_dbx

    # 测试结束后，清理环境变量，避免影响其他测试或程序。
    if "DROPBOX_ACCESS_TOKEN" in os.environ:
        del os.environ["DROPBOX_ACCESS_TOKEN"]

# 这个测试函数检查DropboxLoader是否能正确初始化。
def test_initialization(setup_dropbox_loader):
    # 从setup_dropbox_loader获取loader对象。
    loader, _ = setup_dropbox_loader
    # 检查loader对象是否非空，即是否成功创建。
    assert loader is not None

# 这个测试函数检查是否能正确下载文件夹。
def test_download_folder(setup_dropbox_loader, mocker):
    # 从setup_dropbox_loader获取loader对象和模拟的Dropbox实例。
    loader, mock_dbx = setup_dropbox_loader
    # 模拟创建目录的操作。
    mocker.patch("os.makedirs")
    # 模拟路径连接操作，返回一个模拟的路径字符串。
    mocker.patch("os.path.join", return_value="mock/path")

    # 创建一个模拟的文件元数据对象。
    mock_file_metadata = mocker.MagicMock(spec=FileMetadata)
    # 设置模拟的Dropbox实例返回一个包含模拟文件元数据的列表。
    mock_dbx.files_list_folder.return_value.entries = [mock_file_metadata]

    # 调用下载文件夹的方法，并检查返回值是否非空。
    entries = loader._download_folder("path/to/folder", "local_root")
    assert entries is not None

# 这个测试函数检查是否能正确生成目录ID。
def test_generate_dir_id_from_all_paths(setup_dropbox_loader, mocker):
    # 从setup_dropbox_loader获取loader对象和模拟的Dropbox实例。
    loader, mock_dbx = setup_dropbox_loader
    # 创建一个模拟的文件元数据对象。
    mock_file_metadata = mocker.MagicMock(spec=FileMetadata, name="file.txt")
    # 设置模拟的Dropbox实例返回一个包含模拟文件元数据的列表。
    mock_dbx.files_list_folder.return_value.entries = [mock_file_metadata]

    # 调用生成目录ID的方法，并检查返回值是否非空，以及长度是否为64。
    dir_id = loader._generate_dir_id_from_all_paths("path/to/folder")
    assert dir_id is not None
    assert len(dir_id) == 64

# 这个测试函数检查是否能正确清理目录。
def test_clean_directory(setup_dropbox_loader, mocker):
    # 从setup_dropbox_loader获取loader对象。
    loader, _ = setup_dropbox_loader
    # 模拟列出目录内容的操作。
    mocker.patch("os.listdir", return_value=["file1", "file2"])
    # 模拟删除文件的操作。
    mocker.patch("os.remove")
    # 模拟删除目录的操作。
    mocker.patch("os.rmdir")

    # 调用清理目录的方法。
    loader._clean_directory("path/to/folder")

# 这个测试函数检查是否能正确加载数据。
def test_load_data(mocker, setup_dropbox_loader, tmp_path):
    # 从setup_dropbox_loader获取loader对象。
    loader = setup_dropbox_loader[0]

    # 创建一个模拟的文件元数据对象。
    mock_file_metadata = MagicMock(spec=FileMetadata, name="file.txt")
    # 设置模拟的Dropbox实例返回一个包含模拟文件元数据的列表。
    mocker.patch.object(loader.dbx, "files_list_folder", return_value=MagicMock(entries=[mock_file_metadata]))
    # 模拟下载文件到本地的操作。
    mocker.patch.object(loader.dbx, "files_download_to_file")

    # 模拟DirectoryLoader类的load_data方法。
    mock_data = {"data": "test_data"}
    mocker.patch("embedchain.loaders.directory_loader.DirectoryLoader.load_data", return_value=mock_data)

    # 创建一个临时目录用于测试。
    test_dir = tmp_path / "dropbox_test"
    test_dir.mkdir()
    test_file = test_dir / "file.txt"
    test_file.write_text("dummy content")
    # 模拟生成目录ID的方法。
    mocker.patch.object(loader, "_generate_dir_id_from_all_paths", return_value=str(test_dir))

    # 调用加载数据的方法，并检查返回值是否符合预期。
    result = loader.load_data("path/to/folder")

    assert result == {"doc_id": mocker.ANY, "data": "test_data"}
    # 检查是否调用了list_folder方法。
    loader.dbx.files_list_folder.assert_called_once_with("path/to/folder")

