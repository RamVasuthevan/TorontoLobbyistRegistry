import os
import xml.etree.ElementTree as ET

# List of XML files to process
xml_files = ["lobbyactivity-active.xml", "lobbyactivity-closed.xml"]
REPORTS_FOLDER = "reports"

if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)


def save_rows_to_files(xml_files):
    seen_smnumbers = set()

    for xml_file in xml_files:
        context = ET.iterparse(xml_file, events=("end",))

        for event, elem in context:
            if event == "end" and elem.tag == "ROW":
                # Find the SMNumber within the ROW element
                sm_number = elem.find(".//SMNumber")
                if sm_number is not None and sm_number.text:
                    # Check if SMNumber has been processed before
                    if sm_number.text in seen_smnumbers:
                        raise Exception(
                            f"SMNumber {sm_number.text} has already been processed"
                        )
                    else:
                        seen_smnumbers.add(sm_number.text)
                        file_name = f"{sm_number.text}.xml"
                else:
                    raise Exception("SMNumber not found in the ROW element")

                # Construct the path including the 'reports' folder
                file_path = os.path.join(REPORTS_FOLDER, file_name)

                # Create a new file with the SMNumber as the name
                with open(file_path, "wb") as file:
                    file.write(ET.tostring(elem, encoding="utf-8"))

                # Clear the processed element from memory
                elem.clear()


# Process all XML files
save_rows_to_files(xml_files)
