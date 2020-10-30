# coding: utf-8
#*****************************************************************************
# Copyright (C) 2020 Microchip Technology Inc. and its subsidiaries.
#
# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.
#
# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
# PARTICULAR PURPOSE.
#
# IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
# INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND
# WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS
# BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
# FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
# ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
# THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
#****************************************************************************
"""harmony3.state
Bundled in Harmony 3 package
"""

from os import path
from xml.etree import ElementTree as ET
import json
from collections import namedtuple

H3File = namedtuple('H3File', 'relative_path logical_path')

class H3ProjectState(object):
    """ Represents a Harmony 3 project generation state """

    def __init__(self, folder_name, project_name, state):
        self.project_state = state
        base_path = state.variables["__PROJECT_FIRMWARE_PATH"]
        if folder_name:
            self.project_path = path.normpath(path.join(base_path, folder_name))
        else:
            folder_name = state.variables["__CONFIGURATION_NAME"] + "." + \
                          state.values["core"]["COMPILER_CHOICE"]
            self.project_path = path.normpath(path.join(base_path, folder_name))

        self.state_file = path.join(self.project_path,
                                    project_name + ".h3state")
        self.current_config = {"general":{}, "compiler":{}, "assembler":{}, "linker":{}}

        self.current_config["general"]["name"] = state.variables["__CONFIGURATION_NAME"]
        self.current_config["general"]["device"] = state.variables["__PROCESSOR"]

        compiler_includes = []
        self._get_setting_list(compiler_includes, "C32", "extra-include-directories")
        self._get_setting_list(compiler_includes, "C32CPP", "extra-include-directories")
        self._normalize_path_list(compiler_includes)
        self.current_config["compiler"]["includes"] = compiler_includes

        compiler_macros = []
        self._get_setting_list(compiler_macros, "C32", "preprocessor-macros")
        self._get_setting_list(compiler_macros, "C32CPP", "preprocessor-macros")
        self.current_config["compiler"]["macros"] = compiler_macros

        assembler_includes = []
        self._get_setting_list(assembler_includes,
                               "C32-AS",
                               "extra-include-directories-for-assembler")
        self._normalize_path_list(assembler_includes)
        self.current_config["assembler"]["includes"] = assembler_includes

        assembler_macros = []
        self._get_setting_list(assembler_macros,
                               "C32-AS",
                               "preprocessor-macros")
        self.current_config["assembler"]["macros"] = assembler_macros
        self.current_config["linker"]["script"] = self._get_linker_script()
        self._get_saved_project_config()

    @staticmethod
    def _normalize_path_list(path_list):
        for index, value in enumerate(path_list):
            path_list[index] = path.normpath(value)


    def _get_setting_list(self, value_list, category, key):
        for setting in self.project_state.settings:
            if setting.category == category and setting.key == key:
                for value in setting.value.split(setting.delimiter):
                    if value not in value_list:
                        value_list.append(value)


    def _get_project_relative_file_path(self, file_object):
        file_abs_path = path.normpath(path.join(str(file_object.actualDestPath),
                                                file_object.outputName))
        return path.relpath(file_abs_path, self.project_path)


    def _get_file_list(self, file_type):
        file_list = []
        for project_file in self.project_state.files:
            if project_file.type == file_type:
                file_list.append(H3File(
                    self._get_project_relative_file_path(project_file),
                    str(project_file.projectPath)))
        return file_list

    def _get_linker_script(self):
        linker = ""
        for file_object in self.project_state.files:
            if file_object.type == self.project_state.LogicalType.LINKER:
                linker = self._get_project_relative_file_path(file_object)
                break
        return linker


    def _get_saved_project_config(self):
        #if a project state exists, load it
        if path.isdir(self.project_path) and path.isfile(self.state_file):
            with open(self.state_file) as project_state:
                self.saved_config = json.load(project_state)
        else:
            self.saved_config = {
                "general":{
                    "name":"",
                    "device":"",
                },
                "compiler":{
                    "includes": [],
                    "macros": []
                },
                "assembler":{
                    "includes": [],
                    "macros": []
                },
                "linker":{
                    "script":""
                }
                }


    def get_current_config(self):
        """ Returns the current configuration of the project generation state as
            dictionary. The dictionary has the following key,value pairs:
            general:(name: string,
                     device: string},
            compiler: {includes:string_list,
                       macros: string_list},
            assembler: {includes:string_list,
                        macros: string_list}
            linker: {script: string}
        """
        return self.current_config


    def get_saved_config(self):
        """ Returns the saved configuration of the project state
        If the project saved state is not found, it will return a dictionary
        with empty values for all keys
        """
        return self.saved_config


    def get_mhc_path(self):
        """ Returns the absolute path of the mhc folder """
        return path.join(self.project_state.variables["__FRAMEWORK_DIR"], "mhc")


    def get_project_path(self):
        """ Returns the absolute path of the project folder """
        return self.project_path


    def get_device_architecture(self):
        """ Returns the processor architecture of the device """
        atdf_path = path.join(self.project_state.variables["__DFP_PACK_DIR"],
                              "atdf",
                              self.current_config["general"]["device"] + ".atdf")
        atdf_root = ET.parse(atdf_path).getroot()
        return atdf_root.find("./devices/device").attrib["architecture"]


    def get_header_files(self):
        """ Returns a list of header file tuples
        Each tuple has two fields named relative_path and logical_path
        """
        return self._get_file_list(self.project_state.LogicalType.HEADER)


    def get_source_files(self):
        """ Returns a list of source file tuples
        Each tuple has two fields named relative_path and logical_path
        """
        return self._get_file_list(self.project_state.LogicalType.SOURCE)


    def get_libraries(self):
        """ Returns a list of libraries """
        #Library file paths are relative to the project configuration path
        # We need to make the path relative to the project path
        libraries = set()
        base_path = str(self.project_state.files[0].actualDestPath).split("src")[0]
        config_path = path.join(base_path,
                                "src",
                                "config",
                                self.project_state.variables["__CONFIGURATION_NAME"])

        for library_entry in self.project_state.libraries:
            library_abs_path = path.normpath(path.join(config_path,
                                                       library_entry.dest,
                                                       library_entry.name))
            libraries.add(path.relpath(library_abs_path, self.project_path))
        return list(libraries)


    def save_current_config(self):
        """Save the current project configuration """
        with open(self.state_file, 'w') as state_file:
            json.dump(self.current_config, state_file, indent=4)
