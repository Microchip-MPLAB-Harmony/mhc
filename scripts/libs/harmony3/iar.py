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
""" This module is used for creating IAR project files from an harmony configuration
"""
import os
from os import path
import xml.etree.ElementTree as ET
import json
from jinja2 import Environment, FileSystemLoader
from harmony3.state import H3ProjectState

def _prepend_project_path(path_list):
    proj_path_list = []
    for rel_path in path_list:
        proj_path_list.append(path.join("$PROJ_DIR$", rel_path))
    return proj_path_list


class IARProjectXML(object):
    """ Represents an IAR project XML file """

    def __init__(self, project_file):
        self.project_file_tree = ET.parse(project_file)

    @staticmethod
    def _create_named_node(parent, tag, name):
        node = ET.SubElement(parent, tag)
        ET.SubElement(node, "name").text = name
        return node


    @staticmethod
    def _get_named_child_node(parent, tag, name):
        for child in parent.findall("./{}".format(tag)):
            if child.find("./name").text == name:
                return child
        return None

    @staticmethod
    def _get_option_states(option_node):
        states = []
        for state in option_node.findall("./state"):
            if state.text:
                states.append(state.text)
        return states

    @classmethod
    def _indent_element(cls, element, level=0):
        i = "\n" + level*"    "
        if element is not None:
            if not element.text or not element.text.strip():
                element.text = i + "    "
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
    def _find_group_node(cls, root, group_path_list):
        # We are the maximum depth, i.e found the parent, return it
        if not group_path_list or group_path_list[0] == "":
            return root, None
        parent = None
        for group in root.findall('group'):
            if group.find("name").text == group_path_list[0]:
                parent = group
                break
        # Go to the next depth level
        if parent is not None:
            return cls._find_group_node(parent, group_path_list[1:])

        # No subelement at this level, return current level and remaining depth
        return root, group_path_list


    @classmethod
    def _create_group_node_tree(cls, parent, group_path_list):
        if not group_path_list or group_path_list[0] == "":
            return parent
        child = cls._create_named_node(parent, "group", group_path_list[0])
        return cls._create_group_node_tree(child, group_path_list[1:])


    @classmethod
    def _add_file_node(cls, root, h3_file):
        parent, remaining_path_list = cls._find_group_node(root,
                                                           cls._splitpath(h3_file.logical_path))
        if remaining_path_list:
            parent = cls._create_group_node_tree(parent, remaining_path_list)
        IARProjectXML._create_named_node(parent,
                                         "file",
                                         path.join("$PROJ_DIR$", h3_file.relative_path))


    @classmethod
    def _create_file_groups(cls, project_state, root_node=None):
        #Root Node
        if root_node is None:
            root_node = ET.Element("group")
        else:
            root_node.clear()
        ET.SubElement(root_node, "name").text = "Harmony3"

        #Header Files
        header_node = IARProjectXML._create_named_node(root_node, "group", "Header Files")
        for header_file in project_state.get_header_files():
            cls._add_file_node(header_node, header_file)

        #Source Node
        source_node = IARProjectXML._create_named_node(root_node, "group", "Source Files")
        for source_file in project_state.get_source_files():
            cls._add_file_node(source_node, source_file)

        #linker script
        linker_script = project_state.get_current_config()["linker"]["script"]
        if linker_script:
            linker_node = IARProjectXML._create_named_node(root_node, "group", "Linker File")
            IARProjectXML._create_named_node(linker_node,
                                             "file",
                                             path.join("$PROJ_DIR$", linker_script))

        #Libraries to be linked, if any
        libraries = project_state.get_libraries()
        if libraries:
            library_node = IARProjectXML._create_named_node(root_node, "group", "Libraries")
            for library in libraries:
                IARProjectXML._create_named_node(library_node,
                                                 "file",
                                                 path.join("$PROJ_DIR$", library))

        cls._indent_element(root_node, 1)
        return root_node

    @classmethod
    def _splitpath(cls, full_path):
        path_comp = []
        while 1:
            parts = os.path.split(full_path)
            if parts[0] == full_path:  # sentinel for absolute paths
                path_comp.insert(0, parts[0])
                break
            elif parts[1] == full_path: # sentinel for relative paths
                path_comp.insert(0, parts[1])
                break
            else:
                full_path = parts[0]
                path_comp.insert(0, parts[1])
        return path_comp

    @classmethod
    def get_formatted_file_groups(cls, project_state):
        """ Returns a XML formatted string of the project file groups """
        return ET.tostring(cls._create_file_groups(project_state, None))

    @classmethod
    def update_workspace(cls, project_file_path):
        """ Creates/Updates an IAR workspace file  """
        workspace_file_path = project_file_path.replace(".ewp", ".eww")
        project_path_text = path.join("$WS_DIR$", path.basename(project_file_path))
        if path.isfile(workspace_file_path):
            workspace_tree = ET.parse(workspace_file_path)
            workspace_root = workspace_tree.getroot()
            for project in workspace_root.findall("./project"):
                if project.find("./path").text == project_path_text:
                #Project already exists in the workspace, no update required
                    return
        else:
            workspace_root = ET.Element("workspace")
            workspace_tree = ET.ElementTree(workspace_root)

        project_node = ET.SubElement(workspace_root, "project")
        ET.SubElement(project_node, "path").text = project_path_text
        cls._indent_element(workspace_root)
        workspace_tree.write(workspace_file_path, xml_declaration=True, encoding="utf-8")


    def _set_option_states(self, option_node, states):
        name = option_node.find("./name").text
        option_node.clear()
        ET.SubElement(option_node, "name").text = name
        for state in states:
            state_node = ET.SubElement(option_node, "state")
            state_node.text = state
        self._indent_element(option_node, 4)


    def _update_option_states(self, option_node, new_states, old_states):
        final_states = []
        for state in new_states:
            if state not in final_states:
                final_states.append(state)

        iar_states = self._get_option_states(option_node)

        #include any user state into the harmony state
        # user state is any iar state not found in old harmony state
        for iar_state in iar_states:
            if iar_state not in old_states:
                final_states.append(iar_state)

        self._set_option_states(option_node, final_states)


    def _update_config(self, config_node, project_state):
        old_config = project_state.get_saved_config()
        new_config = project_state.get_current_config()

        ##########                 Compiler settings           ##########
        data_node = self._get_named_child_node(config_node, "settings", "ICCARM").find("./data")

        #macros
        option_node = self._get_named_child_node(data_node, "option", "CCDefines")
        self._update_option_states(option_node,
                                   new_config["compiler"]["macros"],
                                   old_config["compiler"]["macros"])

        #includes
        option_node = self._get_named_child_node(data_node, "option", "CCIncludePath2")
        #we need to prepend $PROJ_DIR$ to each individual paths
        self._update_option_states(option_node,
                                   _prepend_project_path(new_config["compiler"]["includes"]),
                                   _prepend_project_path(old_config["compiler"]["includes"]))

        ##########                 Assembler settings           ##########
        data_node = self._get_named_child_node(config_node, "settings", "AARM").find("./data")

        #macros
        option_node = self._get_named_child_node(data_node, "option", "ADefines")
        self._update_option_states(option_node,
                                   new_config["assembler"]["macros"],
                                   old_config["assembler"]["macros"])

        #includes
        option_node = self._get_named_child_node(data_node, "option", "AUserIncludes")
        #we need to prepend $PROJ_DIR$ to each individual paths
        self._update_option_states(option_node,
                                   _prepend_project_path(new_config["assembler"]["includes"]),
                                   _prepend_project_path(old_config["assembler"]["includes"]))

        ##########                 Linker settings           ##########
        data_node = self._get_named_child_node(config_node, "settings", "ILINK").find("./data")

        #Linker script
        linker_script = new_config["linker"]["script"]
        if linker_script:
            linker_script = path.join("$PROJ_DIR$", linker_script)
        #Enable/disable linker script override
        linker_script_override = "1" if linker_script else "0"
        self._get_named_child_node(data_node,
                                   "option",
                                   "IlinkIcfOverride"
                                  ).find("./state").text = linker_script_override

        #Set/Clear new linker script
        linker_script_file = linker_script if linker_script else "lnk0t.icf"
        self._get_named_child_node(data_node,
                                   "option",
                                   "IlinkIcfFile"
                                  ).find("./state").text = linker_script_file


    def _clean_ipcf_entries(self, root, config_name):
        ipcf_node = self._get_named_child_node(root, "group", "IAR Project Connection File")
        if ipcf_node is not None:
            root.remove(ipcf_node)
        file_path_base = "$PROJ_DIR$\\..\\src\\config\\" + config_name
        file_nodes = root.findall("file")
        for file_node in file_nodes:
            if file_node.find("name").text.startswith(file_path_base):
                root.remove(file_node)


    def update(self, project_state):
        """ Updates and existing IAR project xml with a new project state """
        project_root = self.project_file_tree.getroot()

        for config_node in project_root.findall("./configuration"):
            self._update_config(config_node, project_state)

        #Clean existing IPCF entries
        config_name = project_state.get_current_config()["general"]["name"]
        self._clean_ipcf_entries(project_root, config_name)

        # Update project file group
        group_node = self._get_named_child_node(project_root,
                                                "group",
                                                "Harmony3")
        if group_node is None:
            group_node = ET.SubElement(project_root, "group")
        self._create_file_groups(project_state, group_node)


    def save(self, project_file_path):
        """Save the updated project file """
        self.project_file_tree.write(project_file_path,
                                     xml_declaration=True,
                                     encoding="utf-8")


class IARProject(object):
    """ Represents an IAR project """

    _TEMPLATE_FILE_NAME = "ewp.xml.jinja"
    _DATABASE_FILE_NAME = "device_db.json"

    def __init__(self, folder_name, project_name, project_state):
        self.project_state = H3ProjectState(folder_name, project_name, project_state)

        #Set paths
        self.project_file_abs_path = path.join(
            self.project_state.get_project_path(),
            project_name + ".ewp")


    def _get_device_database(self):
        device_db = {}
        database_file_path = path.join(self.project_state.get_mhc_path(),
                                       "databases",
                                       "iar",
                                       self._DATABASE_FILE_NAME)
        with open(database_file_path) as db_file:
            device_db = json.load(db_file)
        return device_db


    def _create_new_project(self):
        #####Configure the project ####
        project_config = self.project_state.get_current_config()
        iar_config = {}
        iar_config["config_name"] = project_config["general"]["name"]

        #Update device specific configuration
        device_db = self._get_device_database()

        # Check if IAR uses an alternate name for the device, use it
        device_name = project_config["general"]["device"]
        iar_device_name = device_db["device_alt_name"].get(device_name)
        iar_config["device_name"] = iar_device_name or device_name

        #Copy the family specific configuration
        arch = self.project_state.get_device_architecture()
        iar_config.update(device_db["device_arch"].get(arch))

        #copy compiler includes and defines
        iar_config["compiler_macros"] = list(project_config["compiler"]["macros"])
        iar_config["compiler_includes"] = _prepend_project_path(
            project_config["compiler"]["includes"])

        #copy assembler includes and defines
        iar_config["assembler_macros"] = list(project_config["assembler"]["macros"])
        iar_config["assembler_includes"] = _prepend_project_path(
            project_config["assembler"]["includes"])

        #copy linker script
        linker_script = project_config["linker"]["script"]
        if linker_script:
            linker_script = path.join("$PROJ_DIR$", linker_script)
        iar_config["linker_script"] = linker_script

        #file groups
        iar_config["file_groups"] = IARProjectXML.get_formatted_file_groups(self.project_state)

        #Output the configuration into the project file using a template
        template_loader = FileSystemLoader(path.join(self.project_state.get_mhc_path(),
                                                     "np_templates",
                                                     "iar_template"))
        template_environment = Environment(loader=template_loader)
        project_template = template_environment.get_template(self._TEMPLATE_FILE_NAME)
        with open(self.project_file_abs_path, "w") as output:
            output.write(project_template.render(iar_config))

        print  "IAR project " + path.basename(self.project_file_abs_path) + " created successfully"


    def _update_existing_project(self):
        project_xml = IARProjectXML(self.project_file_abs_path)
        project_xml.update(self.project_state)
        project_xml.save(self.project_file_abs_path)
        print "IAR project " + path.basename(self.project_file_abs_path) + " updated successfully"


    def generate_project(self):
        """ Creates an IAR project """

        dir_exists = True
        # create the project folder, if it doesnt exist
        if not path.isdir(self.project_state.get_project_path()):
            dir_exists = False
            os.mkdir(self.project_state.get_project_path())

        #If project directory or file does not exist, create a new one
        if not dir_exists or not path.isfile(self.project_file_abs_path):
            print "Creating a new IAR project..."
            self._create_new_project()
        # else update the existing one
        else:
            print "Updating existing IAR project ..."
            self._update_existing_project()

        #Update workspace file
        IARProjectXML.update_workspace(self.project_file_abs_path)

        #Save the current project state
        self.project_state.save_current_config()
        print "Successfully saved project state"
