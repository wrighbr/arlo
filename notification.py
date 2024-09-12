import logging
from clients import read_config, arlo_client,pushbullet_client
 
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 
logging.basicConfig(format = log_format, level = logging.INFO)
logger = logging.getLogger()
 

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
        message = "Camera {} (ID: {}) battery level: {}%"\
            .format(camera.name, camera.device_id, camera.battery_level)
        
        logger.warning("Arlo camera {} is offline".format(message))
        push_bullet.push_note("Arlo Camera offline", message)
    else:
        logger.info("Arlo camera {} is online".format(camera.name))   


def main():
    config = read_config()
    arlo = arlo_client(config)
    
    for camera in arlo.cameras:
        push_arlo_bat_notification(config, camera)
        push_arlo_offline_notification(config, camera)

if __name__ == '__main__':
    main()
