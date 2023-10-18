##### DESCRIPTION #####
# This Python script is able to translate UUID fields of NoSQL documents.


import base64
import json

from bson.binary import Binary, UuidRepresentation
from uuid import UUID


def translate_document(document: dict):
    # Iterate over all fields in the document
    for key, value in document.items():
        # Check if the field is a UUID field
        if isinstance(value, dict) and "$binary" in value:
            # Check if the UUID is in BinData with subtype 3
            if value["$binary"]["subType"] == "03":
                # Convert the base64 string back to a UUID object
                uuid_bytes = base64.b64decode(value["$binary"]["base64"])
                uuid_obj = UUID(bytes=uuid_bytes)

                # Convert the UUID object to a binary representation with subtype 4
                binary_uuid = Binary.from_uuid(
                    uuid_obj, UuidRepresentation.PYTHON_LEGACY
                )

                # Replace the original UUID field with the new UUID field
                document[key] = {
                    "$binary": {
                        "base64": base64.b64encode(binary_uuid).decode(),
                        "subType": "04",
                    }
                }


if __name__ == "__main__":
    collection = []  # Import your collection as a JSON list
    for document in collection:
        translate_document(document)

    with open("name_of_output_file.json", "w") as f:
        json.dump(set, f, ensure_ascii=False, indent=4)
