import pyaarlo
from pushbullet import Pushbullet
import yaml

def read_config():
    with open('config.yaml', 'r') as yamlfile:
        config = yaml.safe_load(yamlfile)
    return config

def arlo_client(config):
    client = pyaarlo.PyArlo(
        username=config['arlo']['username'],
        password=config['arlo']['password'],
        backend='sse',
        mqtt_host='mqtt-cluster-z1.arloxcld.com',
        tfa_host='imap.gmail.com',
        tfa_source='imap',
        tfa_type='email',
        tfa_username=config['google']['gmail']['username'],
        tfa_password=config['google']['gmail']['password']
    )
    return client

def pushbullet_client(config):
    api_key = config['push_bullet']['api_key']
    client = Pushbullet(api_key)
    return client

