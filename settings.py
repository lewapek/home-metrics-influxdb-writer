from types import SimpleNamespace
from pyhocon import ConfigFactory

config = ConfigFactory().parse_file("config/application.conf")

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
