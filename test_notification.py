import unittest
from unittest.mock import patch, MagicMock
from notification import push_arlo_offline_notification

class TestNotification(unittest.TestCase):

    @patch('notification.pushbullet_client')
    def test_push_arlo_offline_notification_camera_offline(self, mock_pushbullet_client):
        mock_pushbullet = MagicMock()
        mock_pushbullet_client.return_value = mock_pushbullet

        config = {
            'arlo': {
                'battery_level': 20
            }
        }
        camera = MagicMock()
        camera.is_unavailable = True
        camera.name = "Front Door"
        camera.device_id = "12345"
        camera.battery_level = 15

        push_arlo_offline_notification(config, camera)

        mock_pushbullet.push_note.assert_called_once_with(
            "Arlo Camera offline",
            "Camera Front Door (ID: 12345) battery level: 15%"
        )

    @patch('notification.pushbullet_client')
    def test_push_arlo_offline_notification_camera_online(self, mock_pushbullet_client):
        mock_pushbullet = MagicMock()
        mock_pushbullet_client.return_value = mock_pushbullet

        config = {
            'arlo': {
                'battery_level': 20
            }
        }
        camera = MagicMock()
        camera.is_unavailable = False
        camera.name = "Front Door"
        camera.device_id = "12345"
        camera.battery_level = 15

        push_arlo_offline_notification(config, camera)

        mock_pushbullet.push_note.assert_not_called()

if __name__ == '__main__':
    unittest.main()
