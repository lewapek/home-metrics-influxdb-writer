from datetime import timedelta, datetime


def create_point(name, tags_dict, time, value):
    return {
        "measurement": name,
        "tags": tags_dict,
        "time": time.isoformat(),
        "fields": {
            "value": value
        }
    }


def create_point_list(name, tags_dict, time, interval_ms, values):
    interval = timedelta(milliseconds=interval_ms)
    start_time = time - interval * (len(values) - 1)
    points = []
    for index, value in enumerate(values):
        points.append(create_point(name, tags_dict, start_time + index * interval, value))

    return points


def influx_points(json_body):
    time = datetime.utcnow()

    measurements_interval_ms = json_body["interval"]
    pm25 = json_body["pm25"]
    pm10 = json_body["pm10"]
    temperatures = json_body["temp"]
    relative_humidities = json_body["hum"]

    pm25_point = create_point("pm25", {}, time, pm25)
    pm10_point = create_point("pm10", {}, time, pm10)
    temperature_points = create_point_list("temperature", {}, time, measurements_interval_ms, temperatures)
    relative_humidity_points = create_point_list("relative_humidity", {}, time, measurements_interval_ms,
                                                 relative_humidities)

    return [pm25_point] + [pm10_point] + temperature_points + relative_humidity_points
