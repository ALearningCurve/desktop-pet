import tkinter as tk
from xml.etree.ElementTree import XML
from screeninfo import get_monitors
from xml.dom import minidom
import distutils.util
from src import logger
import pathlib
import os
from typing import Tuple


class PetConfiguration:
    offset: int
    bg_color: str
    target_resolution: Tuple[int, int]

    def __init__(self, offset, bg_color, target_resolution):
        self.offset = offset
        self.bg_color = bg_color
        self.target_resolution = target_resolution


class XMLReader:
    path: str
    """
    Path to the xml data store
    """
    dom: minidom

    def __init__(self, path=None, dom=None):
        if dom is None:
            if path is None:
                path = os.path.join(pathlib.Path().resolve(), "config.xml")
            self.path = path
            self.dom = minidom.parse(path)
        else:
            self.path = path
            self.dom = dom

    def getDefaultPet(self):
        return self.getFirstTagValue("defualt_pet")

    def getForceTopMostWindow(self):
        return self.getFirstTagValueAsBool("force_topmost")

    def getShouldRunAnimationPreprocessing(self):
        return self.getFirstTagValueAsBool("should_run_preprocessing")

    def getMatchingPetConfigurationAsDom(self, pet: str) -> minidom:
        pets = self.dom.getElementsByTagName("pet")
        pet_config = None
        for i in range(len(pets)):
            if pets[i].getAttribute("name") == pet:
                pet_config = pets[i]
        if pet_config is None:
            raise Exception(
                "Could not find the current pet as one of \
                the supported pets in the config.xml. 'current_pet' must \
                match one of the 'pet' element's 'name' attribute"
            )
        return pet_config

    def getMatchingPetConfigurationClean(self, pet: str) -> PetConfiguration:
        pet_config = self.getMatchingPetConfigurationAsDom(pet)
        pet_reader = XMLReader(dom=pet_config)
        offset = int(pet_reader.getFirstTagValue("offset"))
        bg_color = pet_reader.getFirstTagValue("bg_color")
        resolution = XMLReader(dom=pet_config.getElementsByTagName("resolution")[0])
        target_resolution = (
            int(resolution.getFirstTagValue("x")),
            int(resolution.getFirstTagValue("y")),
        )

        return PetConfiguration(offset, bg_color, target_resolution)

    def getFirstTagValueAsBool(self, tag_name: str) -> bool:
        return XMLReader.xml_bool(self.getFirstTagValue(tag_name))

    def getFirstTagValue(self, tag_name: str) -> str:
        return self.dom.getElementsByTagName(tag_name)[0].firstChild.nodeValue

    def setFirstTagValue(self, tag_name: str, val: any):
        self.dom.getElementsByTagName(tag_name)[0].firstChild.replaceWholeText(val)

    def save(self, path: str = None):
        if path is None:
            path = self.path

        with open(self.path, "w") as f:
            f.write(self.dom.toxml())

    @staticmethod
    def xml_bool(val: str) -> bool:
        return bool(distutils.util.strtobool(val))
