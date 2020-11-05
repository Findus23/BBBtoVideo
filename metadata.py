from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree


class Metadata:
    def __init__(self, xml_file: Path):
        tree = ElementTree.parse(xml_file)
        root = tree.getroot()

        self.meetingName = root.find("./meta/meetingName").text
        self.starttime = datetime.fromtimestamp(int(root.find("./start_time").text) / 1000)
        self.duration = int(int(root.find("./playback/duration").text)) / 1000

