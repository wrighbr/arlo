import os
import shutil
import logging
from google.cloud import storage
import pyaarlo
from clients import *
 
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 
logging.basicConfig(format = log_format, level = logging.INFO)
logger = logging.getLogger()
 
def set_gcp_credentials(config):
    credentials = config['google']['gcp']['credentials']
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
 
def get_gsc_file(bucket_name, filename):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    return blob
 
def upload_file(bucket_name, source_file, dest_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(dest_name)
   
    logger.info('Uploading: {}'.format(dest_name))
    blob.upload_from_filename(source_file)

def download_and_upload_video(config, camera, video):
    video_name = f"{camera.name.lower().replace(' ', '_')}/{video.created_at_pretty()}.mp4"
    dest_file = video_name.replace('T', '/')

    gsc_file = get_gsc_file(config['google']['gcp']['bucket'], dest_file)

    if not gsc_file.exists():
        camera_name = camera.name.lower().replace(' ', '_')
        if not os.path.exists(camera_name):
            os.mkdir(camera_name)

        logger.info(f'Downloading: {video_name}')
        video.download_video(video_name)
        upload_file(config['google']['gcp']['bucket'], video_name, dest_file)
        os.remove(video_name)

def push_arlo_bat_notification(config, camera):
    push_bullet = pushbullet_client(config)
    message = "Camera {} (ID: {}) battery level: {}%"\
        .format(camera.name, camera.device_id, camera.battery_level)
    logging.info(message)
    if camera.battery_level < config['arlo']['battery_level']:
        push_bullet.push_note("Arlo Battery Level", message)

def push_arlo_offline_notification(config, camera):
    if camera.is_unavailable:
        push_bullet = pushbullet_client(config)
        message = "Camera {} (ID: {})"\
        .format(camera.name, camera.device_id, camera.battery_level)
        push_bullet.push_note("Arlo Camera offline", message)

def main():
    config = read_config()
    set_gcp_credentials(config)
    arlo = arlo_client(config)
    
    for camera in arlo.cameras:
        push_arlo_bat_notification(config, camera)
        push_arlo_offline_notification(config, camera)

        for video in camera.last_n_videos(-1):
            download_and_upload_video(config, camera, video)

if __name__ == '__main__':
    main()
