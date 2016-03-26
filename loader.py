from pprint import pprint
from pymongo import MongoClient


def small_hyphenated(string):
    string = str(string)
    string = string.lower()
    string = string.replace(" ", "-")
    return string


def image_path_maker(image_host, name, image_format):
    name = str(name)
    name = small_hyphenated(name)
    return image_host + "/" + name + "." + image_format


def inject_image_key(nominee_list, image_host, key, image_format):
    desired_nominee_list = [dict(name=name) for name in nominee_list]
    for nominee in desired_nominee_list:
        nominee.setdefault("images", dict(
            phone=image_path_maker(
                image_host + "/phone/" + key,
                nominee["name"],
                image_format
            ),
            desktop=image_path_maker(
                image_host + "/desktop/" + key,
                nominee["name"],
                image_format
            )
        ))
    return desired_nominee_list


def get_data(configuration_file_path):
    with open(configuration_file_path, "r") as f:
        data = f.read()
        category_wise = data.split("\n\n")
        desired_data = dict()
        for datum in category_wise:
            if datum[0] == "#":
                continue
            if len(datum) == 0:
                continue
            datum_list = datum.split("\n")
            if len(datum_list) == 2:
                desired_data.setdefault(datum_list[0], datum_list[1])
            else:
                key = datum_list[0]
                nominee_list = datum_list[1:]
                if key.find("Male") != -1:
                    key = small_hyphenated(key[:key.find(": Male")])
                    desired_data.setdefault(key, dict())
                    desired_nominee_list = inject_image_key(
                        nominee_list,
                        desired_data["image-host"],
                        key,
                        desired_data["image-format"]
                    )
                    desired_data[key].setdefault("male", desired_nominee_list)
                elif key.find("Female") != -1:
                    key = small_hyphenated(key[:key.find(": Female")])
                    desired_data.setdefault(key, dict())
                    desired_nominee_list = inject_image_key(
                        nominee_list,
                        desired_data["image-host"],
                        key,
                        desired_data["image-format"]
                    )
                    desired_data[key].setdefault("female", desired_nominee_list)
                else:
                    key = small_hyphenated(key)
                    desired_nominee_list = inject_image_key(
                        nominee_list,
                        desired_data["image-host"],
                        key,
                        desired_data["image-format"]
                    )
                    desired_data.setdefault(small_hyphenated(key), desired_nominee_list)

        ip = desired_data["api-ip"]
        port = desired_data["api-port"]
        protocol = "http:"
        desired_data.setdefault("urls", dict(
            login=protocol + "//" + ip + ":" + str(port) + "/api/login",
            feedback=protocol + "//" + ip + ":" + str(port) + "/api/feedback",
            vote=protocol + "//" + ip + ":" + str(port) + "/api/vote",
            test=protocol + "//" + ip + ":" + str(port) + "/api/test",
        ))
        desired_data.setdefault("banner", )
        desired_data["banner"] = image_path_maker(
            desired_data["image-host"],
            desired_data["banner"],
            desired_data["image-format"]
        )
        with open(desired_data["about"], "r") as about_file:
            desired_data["about"] = about_file.read()
        client = MongoClient()
        db = client.udaanRedCarpet
        db.config.drop()
        db.config.insert(desired_data)
        return ip, port, desired_data["web-host"]
