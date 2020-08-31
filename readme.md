---
title: Harmony 3 Configurator Package
nav_order: 1
has_children: true
---

# MPLAB® Harmony 3 Configurator

MPLAB® Harmony 3 is an extension of the MPLAB® ecosystem for creating
embedded firmware solutions for Microchip 32-bit SAM and PIC® microcontroller
and microprocessor devices.  Refer to the following links for more information.

- [Microchip 32-bit MCUs](https://www.microchip.com/design-centers/32-bit)
- [Microchip 32-bit MPUs](https://www.microchip.com/design-centers/32-bit-mpus)
- [Microchip MPLAB® X IDE](https://www.microchip.com/mplab/mplab-x-ide)
- [Microchip MPLAB® Harmony](https://www.microchip.com/mplab/mplab-harmony)
- [Microchip MPLAB® Harmony Pages](https://microchip-mplab-harmony.github.io/)

This repository contains the implementation of the MPLAB® Harmony 3 Configurator
(MHC) tool. The MHC is an easy to use development tool with a Graphical User
Interface (GUI) that simplifies device setup, library selection, and
configuration, and application development. The MHC is available as a plugin
that directly integrates with the MPLAB® X IDE or as a separate Java executable
for standalone use with other development environments.

MHC includes a downloader tool that reads an online catalog of MPLAB
Harmony 3 library packages so that the developers can select and download the
libraries in which the they are interested. The configurator functionality
provides a convenient, but powerful, development tool for choosing library
components from downloaded packages and configuring them for the developer’s
application. And, the built-in code generator produces the libraries and
application starter code (usually in source form), based on the options chosen.

- [Getting started with MHC](doc/readme.md)
- [Release Notes](release_notes.md)

# Contents Summary

| File/Folder           | Description                                               |
|-----------------------|-----------------------------------------------------------|
| doc                   | Help documentation and licenses for libraries used        |
| np_templates          | New Project templates for supported toolchains            |
| databases             | Device databases for supported toolchains                 |
| scripts               | Python scripts used for project generation                |
| *.jar                 | Java implementations of MHC modules.                      |
| mhc.jar               | Main Java executable (run: java -jar mhc.jar -h)          |
| harmony-database.jar  | internal sub module to hold all symbols                   |
| databaseUI.jar        | internal sub module to show database                      |
| mhc_utils.jar         | internal sub module for harmony utility                   |
| mplx_launcher.jar     | internal sub module used with MPLABX platform             |
| runmhc.bat            | Windows cmd batch file to run standalone MHC GUI          |

## Open source Libraries

Harmony 3 configurator and Content manager uses following open sources libraries:

| Library Name                                  | Version                    | License                                                                                               |
|-----------------------------------------------|---------------------------|-------------------------------------------------------------------------------------------------------|
| [cmdline.jar](https://mvnrepository.com/artifact/info.picocli/picocli)                                   |                     | Apache License 2.0 [https://github.com/remkop/picocli/blob/master/LICENSE](https://github.com/remkop/picocli/blob/master/LICENSE)                              |
| [docking-frames-common.jar](https://mvnrepository.com/artifact/org.dockingframes/docking-frames-common)                     |                     | GNU Lesser General Public License, version 2.1 [http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html) |
| [docking-frames-core.jar](https://mvnrepository.com/artifact/org.dockingframes/docking-frames-core)                       |                     | GNU Lesser General Public License, version 2.1 [http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html) |
| [freemarker-2.3.23.jar](https://mvnrepository.com/artifact/org.freemarker/freemarker/2.3.23)                                | 2.3.23              | Apache License Version 2.0 [https://freemarker.apache.org/docs/app_license.html](https://freemarker.apache.org/docs/app_license.html)                        |
| [jython-standalone-2.7.2.jar](https://mvnrepository.com/artifact/org.python/jython-standalone/2.7.2)                                    | 2.7.2               | PSF License v2 [https://github.com/jythontools/jython/blob/master/LICENSE.txt](https://github.com/jythontools/jython/blob/master/LICENSE.txt)                          |
| [simple-xml-2.7.1.jar](https://mvnrepository.com/artifact/org.simpleframework/simple-xml/2.7.1)                          | 2.7.1               | The Apache Software License, Version 2.0 [http://www.apache.org/licenses/LICENSE-2.0.txt](http://www.apache.org/licenses/LICENSE-2.0.txt)               |
| [jinja2](https://pypi.org/project/Jinja2/)                                        | 2.10.3              | BSD 3-Clause "New" or "Revised" License [https://github.com/pallets/jinja/blob/master/LICENSE.rst](https://github.com/pallets/jinja/blob/master/LICENSE.rst)      |
| [markupsafe](https://pypi.org/project/MarkupSafe/)                                    | 1.1.1               | BSD 3-Clause "New" or "Revised" License [https://github.com/pallets/markupsafe/blob/master/LICENSE.rst](https://github.com/pallets/markupsafe/blob/master/LICENSE.rst) |
| [jsch-0.1.54.jar](https://mvnrepository.com/artifact/com.jcraft/jsch/0.1.54)								| 0.1.54              | Revised BSD http://www.jcraft.com/jsch/LICENSE.txt                                        |
| [org.eclipse.jgit-4.11.0.201803080745-r.jar](https://mvnrepository.com/artifact/org.eclipse.jgit/org.eclipse.jgit/4.11.0.201803080745-r)   	| 4.11.0.201803080745-r | Eclipse Distribution License (New BSD License)                                            |
| [slf4j-api-1.7.25.jar](https://mvnrepository.com/artifact/org.slf4j/slf4j-api/1.7.2)                         	| 1.7.25              | MIT License http://www.opensource.org/licenses/mit-license.php                            |
| [slf4j-simple-1.7.25.jar](https://mvnrepository.com/artifact/org.slf4j/slf4j-simple/1.7.25)                      	| 1.7.25              | MIT License http://www.opensource.org/licenses/mit-license.php                            |
____

[![License](https://img.shields.io/badge/license-Harmony%20license-orange.svg)](https://github.com/Microchip-MPLAB-Harmony/mhc/blob/master/mplab_harmony_license.md)
[![Latest release](https://img.shields.io/github/release/Microchip-MPLAB-Harmony/mhc.svg)](https://github.com/Microchip-MPLAB-Harmony/mhc/releases/latest)
[![Latest release date](https://img.shields.io/github/release-date/Microchip-MPLAB-Harmony/mhc.svg)](https://github.com/Microchip-MPLAB-Harmony/mhc/releases/latest)
[![Commit activity](https://img.shields.io/github/commit-activity/y/Microchip-MPLAB-Harmony/mhc.svg)](https://github.com/Microchip-MPLAB-Harmony/mhc/graphs/commit-activity)
[![Contributors](https://img.shields.io/github/contributors-anon/Microchip-MPLAB-Harmony/mhc.svg)]()
____

[![Follow us on Youtube](https://img.shields.io/badge/Youtube-Follow%20us%20on%20Youtube-red.svg)](https://www.youtube.com/user/MicrochipTechnology)
[![Follow us on LinkedIn](https://img.shields.io/badge/LinkedIn-Follow%20us%20on%20LinkedIn-blue.svg)](https://www.linkedin.com/company/microchip-technology)
[![Follow us on Facebook](https://img.shields.io/badge/Facebook-Follow%20us%20on%20Facebook-blue.svg)](https://www.facebook.com/microchiptechnology/)
[![Follow us on Twitter](https://img.shields.io/twitter/follow/MicrochipTech.svg?style=social)](https://twitter.com/MicrochipTech)

[![](https://img.shields.io/github/stars/Microchip-MPLAB-Harmony/mhc.svg?style=social)]()
[![](https://img.shields.io/github/watchers/Microchip-MPLAB-Harmony/mhc.svg?style=social)]()
