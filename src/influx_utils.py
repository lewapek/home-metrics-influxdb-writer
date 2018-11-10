from datetime import timedelta, datetime


def create_point(name, location_tag, time, value):
    return {
        "measurement": name,
        "tags": {
            "location": location_tag
        },
        "time": time.isoformat(),
        "fields": {
            "value": value
        }
    }


def times_from(now, request_uptime, measurements_uptimes):
    def calculate_time(measurement_uptime):
        milliseconds_difference = request_uptime - measurement_uptime
        return now - timedelta(milliseconds=milliseconds_difference)
    return [calculate_time(t) for t in measurements_uptimes]


def sds_points(sds_json, location_tag, now, sensor_board_uptime):
    measurements_uptimes = [int(t) for t in sds_json["times"]]
    times = times_from(now, sensor_board_uptime, measurements_uptimes)
    pm25_list = [float(pm) for pm in sds_json["pm25"]]
    pm10_list = [float(pm) for pm in sds_json["pm10"]]
    zipped = zip(times, pm25_list, pm10_list)

    points = []
    for time, pm25, pm10 in zipped:
        points.append(create_point("pm25", location_tag, time, pm25))
        points.append(create_point("pm10", location_tag, time, pm10))

    return points


def dht_points(dht_json, location_tag, now, sensor_board_uptime):
    measurements_uptimes = [int(t) for t in dht_json["times"]]
    times = times_from(now, sensor_board_uptime, measurements_uptimes)
    temperature_list = [float(t) for t in dht_json["temp"]]
    humidity_list = [float(h) for h in dht_json["hum"]]
    zipped = zip(times, temperature_list, humidity_list)

    points = []
    for time, temperature, humidity in zipped:
        points.append(create_point("temperature", location_tag, time, temperature))
        points.append(create_point("relative_humidity", location_tag, time, humidity))

    return points


def influx_points(json_body):
    now = datetime.utcnow()
    uptime = int(json_body["uptime"])

    location_tag = json_body["tag"]

    dht = dht_points(json_body["dht"], location_tag, now, uptime) if "dht" in json_body else []
    sds = sds_points(json_body["sds"], location_tag, now, uptime) if "sds" in json_body else []

    return dht + sds
