from pprint import pprint
from pymongo import MongoClient



def small_hyphenated(string):
    string = str(string)
    string = string.lower()
    string = string.replace(" ", "-")
    return string


def image_path_maker(host, port, path, name, image_format):
    name = str(name)
    name = small_hyphenated(name)
    return "http://" + host + ":" + port + "/" + path + "/" + name + "." + image_format


def inject_image_key(nominee_list, host, port, image_path, key, image_format):
    desired_nominee_list = [dict(name=name) for name in nominee_list]
    for nominee in desired_nominee_list:
        nominee.setdefault("images", dict(
            phone=image_path_maker(
                host,
                port,
                image_path + "/phone/" + key,
                nominee["name"],
                image_format
            ),
            desktop=image_path_maker(
                host,
                port,
                image_path + "/desktop/" + key,
                nominee["name"],
                image_format
            )
        ))
    return desired_nominee_list


def get_data():
    with open("api.config", "r") as f:
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
                    key = small_hyphenated(key.rstrip(": Male"))
                    desired_data.setdefault(key, dict())
                    desired_nominee_list = inject_image_key(
                        nominee_list,
                        desired_data["static-host"],
                        desired_data["static-port"],
                        desired_data["images"],
                        key,
                        desired_data["format"]
                    )
                    desired_data[key].setdefault("male", desired_nominee_list)
                elif key.find("Female") != -1:
                    key = small_hyphenated(key.rstrip(": Female"))
                    desired_data.setdefault(key, dict())
                    desired_nominee_list = inject_image_key(
                        nominee_list,
                        desired_data["static-host"],
                        desired_data["static-port"],
                        desired_data["images"],
                        key,
                        desired_data["format"]
                    )
                    desired_data[key].setdefault("female", desired_nominee_list)
                else:
                    key = small_hyphenated(key)
                    desired_nominee_list = inject_image_key(
                        nominee_list,
                        desired_data["static-host"],
                        desired_data["static-port"],
                        desired_data["images"],
                        key,
                        desired_data["format"]
                    )
                    desired_data.setdefault(small_hyphenated(key), desired_nominee_list)
                # if "person" in desired_data:

        desired_data["persona"] = desired_data["person"]
        del desired_data["person"]
        host = desired_data["api-host"]
        port = desired_data["api-port"]
        protocol = "http:"
        desired_data.setdefault("urls", dict(
            login=protocol + "//" + host + ":" + str(port) + "/api/login",
            feedback=protocol + "//" + host + ":" + str(port) + "/api/feedback",
            vote=protocol + "//" + host + ":" + str(port) + "/api/vote",
            test=protocol + "//" + host + ":" + str(port) + "/api/test",
        ))
        desired_data.setdefault("banner", )
        desired_data["banner"] = image_path_maker(
            desired_data["static-host"],
            desired_data["static-port"],
            "images",
            desired_data["banner"],
            desired_data["format"]
        )
        with open(desired_data["about"], "r") as about_file:
            desired_data["about"] = about_file.read()
        # pprint(desired_data)
        client = MongoClient()
        db = client.udaanRedCarpet
        db.config.drop()
        doc = db.config.insert(desired_data)
        print(doc)
        return desired_data["api-host"], desired_data["api-port"], desired_data["web-host"]
