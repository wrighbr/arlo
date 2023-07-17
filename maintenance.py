import logging
from clients import *
from notification import push_arlo_bat_notification, push_arlo_offline_notification
from backup import *

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 
logging.basicConfig(format = log_format, level = logging.INFO)
logger = logging.getLogger()

def main():
    config = read_config()
    arlo = arlo_client(config)
    set_gcp_credentials(config)

    for camera in arlo.cameras:
        # backing video's
        logger.info(f'Backing up camera {camera.name}')
        for video in camera.last_n_videos(-1):
            download_and_upload_video(config, camera, video)

        # pushing notifications
        push_arlo_bat_notification(config, camera)
        push_arlo_offline_notification(config, camera)

if __name__ == '__main__':
    main()