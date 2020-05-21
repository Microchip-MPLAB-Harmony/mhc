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
""" This module is used for creating Keil -UVision project files from an harmony
    configuration
"""
import os
from os import path
import xml.etree.ElementTree as ET
import json
from jinja2 import Environment, FileSystemLoader
from harmony3.state import H3ProjectState


class UVProjXML(object):
    """ Represents an IAR project XML file """

    def __init__(self, project_file):
        self.project_file_tree = ET.parse(project_file)


    @staticmethod
    def _add_file_node(group_node, file_path):
        file_name = path.basename(file_path)
        if file_name.endswith(('.c', '.C')):
            file_type = '1'
        elif file_name.endswith(('.h', ".H")):
            file_type = '5'
        elif file_name.endswith(('.s', '.S')):
            file_type = '2'
        elif file_name.endswith(('.lib', '.LIB')):
            file_type = '4'
        else:
            #invalid type
            file_type = '0'
        file_node = ET.SubElement(group_node, "File")
        ET.SubElement(file_node, "FileName").text = file_name
        ET.SubElement(file_node, "FileType").text = file_type
        ET.SubElement(file_node, "FilePath").text = file_path


    @classmethod
    def _indent_element(cls, element, level=0):
        i = "\n" + level*"  "
        if element is not None:
            if not element.text or not element.text.strip():
                element.text = i + "  "
            if not element.tail or not element.tail.strip():
                element.tail = i
            for element in element:
                cls._indent_element(element, level+1)
            if not element.tail or not element.tail.strip():
                element.tail = i
        else:
            if level and (not element.tail or not element.tail.strip()):
                element.tail = i

    @classmethod
    def _create_file_groups(cls, project_state, root_node=None):
        #Root Node
        if root_node is None:
            root_node = ET.Element("Group")
        else:
            root_node.clear()
        ET.SubElement(root_node, "GroupName").text = "Harmony3"
        files_node = ET.SubElement(root_node, "Files")

        #Header Files
        for header_file in project_state.get_header_files():
            cls._add_file_node(files_node, header_file.relative_path)

        #Source Files
        for source_file in project_state.get_source_files():
            cls._add_file_node(files_node, source_file.relative_path)

        #Library files
        for library_file in project_state.get_libraries():
            cls._add_file_node(files_node, library_file)

        cls._indent_element(root_node, 3)
        return root_node

    @classmethod
    def get_formatted_file_groups(cls, project_state):
        """ Returns a XML formatted string of the project file groups """
        return ET.tostring(cls._create_file_groups(project_state, None))


    def _update_delimited_text_node(self, node, delimiter, new_values, old_values):
        final_values = []
        for value in new_values:
            if value not in final_values:
                final_values.append(value)

        current_values = node.text.split(delimiter) if node.text is not None else []
        for current_value in current_values:
            if current_value not in old_values:
                final_values.append(current_value)

        #Append all values to a string using ";" as delimiter
        final_node_text = ""
        if final_values:
            final_node_text = final_values.pop(0)
            for final_value in final_values:
                final_node_text = final_node_text + delimiter + final_value

        node.text = final_node_text


    def _update_config(self, target_arm_node, project_state):
        old_config = project_state.get_saved_config()
        new_config = project_state.get_current_config()

        ##########                 Compiler settings           ##########
        compiler_node = target_arm_node.find("./Cads/VariousControls")

        #Update the include paths
        self._update_delimited_text_node(compiler_node.find("IncludePath"),
                                         ";",
                                         new_config["compiler"]["includes"],
                                         old_config["compiler"]["includes"])

        #update macros
        self._update_delimited_text_node(compiler_node.find("Define"),
                                         " ",
                                         new_config["compiler"]["macros"],
                                         old_config["compiler"]["macros"])

        ##########                Assembler settings           ##########
        assembler_node = target_arm_node.find("./Aads/VariousControls")

        #Update the include paths
        self._update_delimited_text_node(assembler_node.find("IncludePath"),
                                         ";",
                                         new_config["assembler"]["includes"],
                                         old_config["assembler"]["includes"])

        #update macros
        self._update_delimited_text_node(assembler_node.find("Define"),
                                         " ",
                                         new_config["assembler"]["macros"],
                                         old_config["assembler"]["macros"])

        ##########               Linker settings               ##########
        linker_node = target_arm_node.find("./LDads")

        #Update linker file
        linker_node.find("ScatterFile").text = new_config["linker"]["script"]


    def update(self, project_state):
        """ Updates and existing KEIL project xml with a new project state """
        project_root = self.project_file_tree.getroot()
        target_name = project_state.get_current_config()["general"]["name"]

        for target_node in project_root.findall("Targets/Target"):
            if target_node.find("TargetName").text == target_name:
                #Update toolchain settings
                self._update_config(target_node.find("TargetOption/TargetArmAds"), project_state)

                #Update project file group
                group_nodes = target_node.findall("Groups/Group")
                for group_node in group_nodes:
                    if group_node.find("GroupName").text == "Harmony3":
                        self._create_file_groups(project_state, group_node)
                        break

                break


    def save(self, project_file_path):
        """Save the updated project file """
        self.project_file_tree.write(project_file_path,
                                     xml_declaration=True,
                                     encoding="utf-8")



class UVisionProject(object):
    """ Represents a uVision project """

    _TEMPLATE_FILE_NAME = "uvprojx.xml.jinja"
    _DATABASE_FILE_NAME = "device_db.json"

    def __init__(self, folder_name, project_name, project_state):
        self.project_state = H3ProjectState(folder_name, project_name, project_state)

        #Set paths
        self.project_file_abs_path = path.join(
            self.project_state.get_project_path(),
            project_name + ".uvprojx")

    def _get_includes(self, key):
        includes_value = ""
        include_list = self.project_state.get_current_config()[key]["includes"]
        if include_list:
            includes_value = include_list[0]
            for include in include_list[1:]:
                includes_value = includes_value + ";" + include
        return includes_value


    def _get_defines(self, key):
        defines_value = ""
        defines_list = self.project_state.get_current_config()[key]["macros"]
        if defines_list:
            defines_value = defines_list[0]
            for define in defines_list[1:]:
                defines_value = defines_value + " " + define
        return defines_value


    def _get_device_database(self):
        device_db = {}
        database_file_path = path.join(self.project_state.get_mhc_path(),
                                       "databases",
                                       "keil",
                                       self._DATABASE_FILE_NAME)
        with open(database_file_path) as db_file:
            device_db = json.load(db_file)
        return device_db


    def _create_new_project(self):
        #####Configure the project ####
        project_config = self.project_state.get_current_config()
        keil_config = {}
        keil_config["config_name"] = project_config["general"]["name"]
        keil_config["device_name"] = project_config["general"]["device"]

        #Update device specific configuration
        device_db = self._get_device_database()

        #Copy the family specific configuration
        arch = self.project_state.get_device_architecture()
        keil_config.update(device_db["device_arch"].get(arch))

        #copy compiler includes and defines
        keil_config["compiler_macros"] = self._get_defines("compiler")
        keil_config["compiler_includes"] = self._get_includes("compiler")

        #copy assembler includes and defines
        keil_config["assembler_macros"] = self._get_defines("assembler")
        keil_config["assembler_includes"] = self._get_includes("assembler")

        #copy linker script
        keil_config["linker_script"] = project_config["linker"]["script"]

        #file groups
        keil_config["file_groups"] = UVProjXML.get_formatted_file_groups(self.project_state)

        #Output the configuration into the project file using a template
        template_loader = FileSystemLoader(path.join(self.project_state.get_mhc_path(),
                                                     "np_templates",
                                                     "keil_template"))
        template_environment = Environment(loader=template_loader)
        project_template = template_environment.get_template(self._TEMPLATE_FILE_NAME)
        with open(self.project_file_abs_path, "w") as output:
            output.write(project_template.render(keil_config))


        print  "KEIL project " + path.basename(self.project_file_abs_path) + " created successfully"

    def _update_existing_project(self):
        project_xml = UVProjXML(self.project_file_abs_path)
        project_xml.update(self.project_state)
        project_xml.save(self.project_file_abs_path)
        print "KEIL project " + path.basename(self.project_file_abs_path) + " updated successfully"

    def generate_project(self):
        """ Creates a Keil uVision project """

        dir_exists = True
        # create the project folder, if it doesnt exist
        if not path.isdir(self.project_state.get_project_path()):
            dir_exists = False
            os.mkdir(self.project_state.get_project_path())

        #If project directory or file does not exist, create a new one
        if not dir_exists or not path.isfile(self.project_file_abs_path):
            print "Creating a new KEIL project..."
            self._create_new_project()
        # else update the existing one
        else:
            print "Updating existing KEIL project ..."
            self._update_existing_project()

        #Save the current project state
        self.project_state.save_current_config()
        print "Successfully saved project state"
