import unittest
from unittest.mock import patch, MagicMock
from backup import upload_file, download_and_upload_video

class TestBackup(unittest.TestCase):

    @patch('backup.storage.Client')
    @patch('backup.logger')
    def test_upload_file(self, mock_logger, mock_storage_client):
        # Arrange
        bucket_name = 'test-bucket'
        source_file = 'test_source_file.mp4'
        dest_name = 'test_dest_file.mp4'

        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_storage_client.return_value.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob

        # Act
        upload_file(bucket_name, source_file, dest_name)

        # Assert
        mock_storage_client.assert_called_once()
        mock_storage_client.return_value.bucket.assert_called_once_with(bucket_name)
        mock_bucket.blob.assert_called_once_with(dest_name)
        mock_blob.upload_from_filename.assert_called_once_with(source_file)
        mock_logger.info.assert_called_with('Uploading: {}'.format(dest_name))
        @patch('backup.get_gsc_file')
        @patch('backup.upload_file')
        @patch('backup.logger')
        @patch('backup.os')
        def test_download_and_upload_video(self, mock_os, mock_logger, mock_upload_file, mock_get_gsc_file):
            # Arrange
            config = {
                'google': {
                    'gcp': {
                        'bucket': 'test-bucket'
                    }
                }
            }
            camera = MagicMock()
            camera.name = 'Test Camera'
            video = MagicMock()
            video.created_at_pretty.return_value = '2023-10-01T12:00:00'
            video_name = 'test_camera/2023-10-01T12:00:00.mp4'
            dest_file = 'test_camera/2023-10-01/12:00:00.mp4'

            mock_blob = MagicMock()
            mock_get_gsc_file.return_value = mock_blob
            mock_blob.exists.return_value = False
            mock_os.path.exists.return_value = False

            # Act
            download_and_upload_video(config, camera, video)

            # Assert
            mock_get_gsc_file.assert_called_once_with('test-bucket', dest_file)
            mock_logger.info.assert_any_call(f'Checking: {dest_file}')
            mock_os.path.exists.assert_called_once_with('test_camera')
            mock_os.mkdir.assert_called_once_with('test_camera')
            mock_logger.info.assert_any_call(f'Downloading: {video_name}')
            video.download_video.assert_called_once_with(video_name)
            mock_upload_file.assert_called_once_with('test-bucket', video_name, dest_file)
            mock_os.remove.assert_called_once_with(video_name)

        @patch('backup.get_gsc_file')
        @patch('backup.logger')
        def test_download_and_upload_video_already_exists(self, mock_logger, mock_get_gsc_file):
            # Arrange
            config = {
                'google': {
                    'gcp': {
                        'bucket': 'test-bucket'
                    }
                }
            }
            camera = MagicMock()
            camera.name = 'Test Camera'
            video = MagicMock()
            video.created_at_pretty.return_value = '2023-10-01T12:00:00'
            dest_file = 'test_camera/2023-10-01/12:00:00.mp4'

            mock_blob = MagicMock()
            mock_get_gsc_file.return_value = mock_blob
            mock_blob.exists.return_value = True

            # Act
            download_and_upload_video(config, camera, video)

            # Assert
            mock_get_gsc_file.assert_called_once_with('test-bucket', dest_file)
            mock_logger.info.assert_any_call(f'Checking: {dest_file}')
            mock_logger.info.assert_any_call(f'Already exists: {dest_file}')
            video.download_video.assert_not_called()
if __name__ == '__main__':
    @patch('backup.get_gsc_file')
    @patch('backup.upload_file')
    @patch('backup.logger')
    @patch('backup.os')
    def test_download_and_upload_video(self, mock_os, mock_logger, mock_upload_file, mock_get_gsc_file):
        # Arrange
        config = {
            'google': {
                'gcp': {
                    'bucket': 'test-bucket'
                }
            }
        }
        camera = MagicMock()
        camera.name = 'Test Camera'
        video = MagicMock()
        video.created_at_pretty.return_value = '2023-10-01T12:00:00'
        video_name = 'test_camera/2023-10-01T12:00:00.mp4'
        dest_file = 'test_camera/2023-10-01/12:00:00.mp4'

        mock_blob = MagicMock()
        mock_get_gsc_file.return_value = mock_blob
        mock_blob.exists.return_value = False
        mock_os.path.exists.return_value = False

        # Act
        download_and_upload_video(config, camera, video)

        # Assert
        mock_get_gsc_file.assert_called_once_with('test-bucket', dest_file)
        mock_logger.info.assert_any_call(f'Checking: {dest_file}')
        mock_os.path.exists.assert_called_once_with('test_camera')
        mock_os.mkdir.assert_called_once_with('test_camera')
        mock_logger.info.assert_any_call(f'Downloading: {video_name}')
        video.download_video.assert_called_once_with(video_name)
        mock_upload_file.assert_called_once_with('test-bucket', video_name, dest_file)
        mock_os.remove.assert_called_once_with(video_name)

    @patch('backup.get_gsc_file')
    @patch('backup.logger')
    def test_download_and_upload_video_already_exists(self, mock_logger, mock_get_gsc_file):
        # Arrange
        config = {
            'google': {
                'gcp': {
                    'bucket': 'test-bucket'
                }
            }
        }
        camera = MagicMock()
        camera.name = 'Test Camera'
        video = MagicMock()
        video.created_at_pretty.return_value = '2023-10-01T12:00:00'
        dest_file = 'test_camera/2023-10-01/12:00:00.mp4'

        mock_blob = MagicMock()
        mock_get_gsc_file.return_value = mock_blob
        mock_blob.exists.return_value = True

        # Act
        download_and_upload_video(config, camera, video)

        # Assert
        mock_get_gsc_file.assert_called_once_with('test-bucket', dest_file)
        mock_logger.info.assert_any_call(f'Checking: {dest_file}')
        mock_logger.info.assert_any_call(f'Already exists: {dest_file}')
        video.download_video.assert_not_called()
    unittest.main()
