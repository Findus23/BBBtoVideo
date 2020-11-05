from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from scipy.interpolate import interp1d

from config import interpolation_method, hide_pointer_if_offscreen


class Cursor:
    def __init__(self, xml_file: Path):
        tree = ElementTree.parse(xml_file)
        root = tree.getroot()
        self.timestamps = []
        self.xs = []
        self.ys = []
        child: Element
        for child in root:
            self.timestamps.append(float(child.attrib["timestamp"]))
            cursor_text = child.find("cursor").text
            x, y = list(map(float, cursor_text.split()))
            if hide_pointer_if_offscreen:
                if x < 0:
                    x = None
                if y < 0:
                    y = None
            self.xs.append(x)
            self.ys.append(y)

        self.xspline = interp1d(self.timestamps, self.xs, kind=interpolation_method)
        self.yspline = interp1d(self.timestamps, self.ys, kind=interpolation_method)
