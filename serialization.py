import json
import sys

import xml.etree.ElementTree as ET


class SerializingManager:
    def serialize_json(self, obj: object, name: str = "", way: str = "") -> dict:
        f_name = name if not name == "" else obj.id
        f_path = way if not way == "" else "data/"
        try:
            with open(f"{f_path}{f_name}{obj.type}", "w", encoding='utf-8') as s_json:
                json.dump(obj.__dict__, s_json, ensure_ascii=False)
            return json.loads(json.dumps(obj.__dict__, ensure_ascii=False))
        except FileNotFoundError:
            print(f"{obj} has not required fields for serializing.\n Check if argument is correct!",
                  file=sys.stderr)
            return {"message": "Found error with serializing files. Check argument!"}

    def serialize_xml(self, obj: object, name: str = "", way: str = "") -> str:
        data = ET.Element('data')
        for field, value in obj.__dict__.items():
            item = ET.SubElement(data, field)
            if type(value) == list and not len(value) == 0:
                for i in value:
                    subitem = ET.SubElement(item, "item")
                    subitem.text = str(i)

            else:
                item.text = str(value)

        s_data = str(ET.tostring(data, encoding='unicode'))

        f_name = name if not name == "" else obj.id
        f_path = way if not way == "" else "data/"

        with open(f"{f_path}{f_name}{obj.type}", 'w', encoding='utf-8') as f:
            f.write(s_data)

        return s_data

    def deserialize_json(self, obj: object, name: str) -> object:
        try:
            r_obj = obj()
            with open(f"data/{name}", "r", encoding='utf-8') as ds_json:
                ds_dict = json.load(ds_json)  # Deserialized dictionary

                # Using dictionary presentaton of class to parse json
                try:
                    for key in ds_dict.keys():
                        r_obj.__dict__[key] = ds_dict[key]

                    return r_obj
                except KeyError as err:
                    print(f"{err}\nFailed to deserialize JSON. Maybe some keys weren't found in file.",
                          file=sys.stderr)
        except FileNotFoundError as err:
            print(f"{err}\nDidn't find a serialized file with name {name}. "
                  f"Try to change name or serialize object before.",
                  file=sys.stderr)
            return None

    def deserialize_xml(self, obj: object, name: str) -> object:
        try:
            r_obj = obj()
            ds_file = ET.parse(f"data/{name}")
            
            root = ds_file.getroot()

            for elem in root:
                if elem.tag in r_obj.__dict__.keys():
                    try:
                        tmp = int(elem.text)
                        r_obj.__dict__[elem.tag] = tmp
                    except ValueError:
                        if not elem.text[0] == "[":
                            r_obj.__dict__[elem.tag] = elem.text
                        else:
                            r_obj.__dict__[elem.tag] = []
                    except TypeError:
                        arr = []
                        for subelem in elem:
                            try:
                                arr.append(int(subelem.text))
                            except ValueError:
                                arr.append(subelem.text)
                        r_obj.__dict__[elem.tag] = arr
            return r_obj

        except FileNotFoundError as err:
            print(f"{err}\nDidn't find a serialized file with name {name}. "
                  f"Try to change name or serialize object before.",
                  file=sys.stderr)
            return None
