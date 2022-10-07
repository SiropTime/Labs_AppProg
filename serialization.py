import json
import sys

import xml.etree.ElementTree as ET


class SerializingManager:
    def serialize_json(self, obj: object) -> dict:
        try:
            with open(f"data/{obj.id}{obj.type}", "w", encoding='utf-8') as s_json:
                json.dump(obj.__dict__, s_json, ensure_ascii=False)
            return json.loads(json.dumps(obj.__dict__, ensure_ascii=False))
        except FileNotFoundError:
            print(f"{obj} has not required fields for serializing.\n Check if argument is correct!",
                  file=sys.stderr)
            return {"message": "Found error with serializing files. Check argument!"}

    def serialize_xml(self, obj: object) -> str:
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
        with open(f"data/{obj.id}{obj.type}", 'w', encoding='utf-8') as f:
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

    def deserialize_xml(self, obj: object, name: str) -> object:
        pass