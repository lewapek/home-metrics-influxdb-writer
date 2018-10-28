from types import SimpleNamespace
from pyhocon import ConfigFactory
import os

try:
    config_file = os.environ["APP_CONFIG_PATH"]
    print("Using custom config file: " + config_file)
except KeyError:
    config_file = "config/application.conf"
    print("Using default config file: " + config_file)

config = ConfigFactory().parse_file(config_file)

influx = SimpleNamespace(
    host=config.get_string("influx.host"),
    port=config.get_int("influx.port"),
    user=config.get_string("influx.user"),
    password=config.get_string("influx.password"),
    database=config.get_string("influx.database")
)

collector = SimpleNamespace(
    host=config.get_string("collector.host"),
    port=config.get_int("collector.port")
)
