from dataclasses import dataclass
from pathlib import Path
from typing import List
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from download import fetch_file


@dataclass
class Slide:
    id: str
    start: float
    end: float
    filename: str
    width: float
    height: float

    @property
    def file(self):
        return fetch_file(self.filename)


class Shapes:
    def __init__(self, xml_file: Path):
        tree = ElementTree.parse(xml_file)
        root = tree.getroot()
        image: Element
        self.slides: List[Slide] = []
        self.maxwidth = 0
        self.maxheight = 0
        for image in root:
            data = image.attrib
            slide = Slide(
                id=data["id"],
                start=float(data["in"]),
                end=float(data["out"]),
                filename=data["{http://www.w3.org/1999/xlink}href"],
                width=int(data["width"]),
                height=int(data["height"]),
            )
            if slide.width > self.maxwidth:
                self.maxwidth = slide.width
            if slide.height > self.maxheight:
                self.maxheight = slide.height
            self.slides.append(slide)
