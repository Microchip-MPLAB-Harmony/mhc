---
title: Release notes
nav_order: 99
---

# MPLAB® Harmony 3 Release Notes

See the following links and release notes for additional information.
 - [Read-me File](./readme.md)
 - [Welcome to MPLAB Harmony 3](https://github.com/Microchip-MPLAB-Harmony/Microchip-MPLAB-Harmony.github.io/wiki)
 - [www.microchip.com/harmony](https://www.microchip.com/harmony)

## MPLAB® Harmony 3 Configurator Release v3.7.2

### New Features and Fixes
- Fixed issue of churning in harmony configuration yml files when configuration is saved without any change.
- Fixed issue of inconsistent use of forward and backslash in path in project.yml file.


## MPLAB® Harmony 3 Configurator Release v3.7.1

### New Features and Fixes
- Fixed build issue of trustzone project for continuous integration build job.

## MPLAB® Harmony 3 Configurator Release v3.7.0

### New Features and Fixes
- MPLAB® Harmony 3 Launcher has been updated to v3.6.3 (MPLAB X Plugin)
- Optimized MHC startup time.
- Fixed export button enable issue in export dialog when path is selected first.
- Fixed issue of Incorrect Library path in MHC Headless mode code generation.
- Fixed Setting key duplication issue in MHC Headless mode code generation.
- Fixed issue of user value update in read only string symbol when string panel lost the focus.
- Prefix and trailing delimiters from setting values have been removed and sorted to maintain a single order in setting symbols.
- In Project Manifest, adding "unknown" as version for packages not cloned as git repositories
- Fixed other minor issues.

## MPLAB® Harmony 3 Configurator Release v3.6.5

### New Features and Fixes
- Fixed MPLAB X project issues related to MHC code generation.

## MPLAB® Harmony 3 Configurator Release v3.6.4

### New Features and Fixes
- Fixed compilation issue happening after code generation by adding new component.
- Minor bug fixes.

## MPLAB® Harmony 3 Configurator Release v3.6.3

Internal release fixing a bug related to Continous Integration build jobs.

## MPLAB® Harmony 3 Configurator Release v3.6.2

### New Features and Fixes
- Harmony MPLAB X plugin has been renamed to MPLAB® Harmony 3 Launcher.
- MPLAB® Harmony 3 Launcher plugin has been updated to version 3.6.2.
- Fixed issues related to new project creation wizard.
- Removed MHC version from module dependecy in project manifest file. 
- MHC headless mode code generation command has been updated.
- Added dialog informing user about the migration to new project configuration structure.

### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.45](https://www.microchip.com/mplab/mplab-x-ide)

## MPLAB® Harmony 3 Configurator Release v3.6.1

### New Features and Fixes
- Fixed IAR EWARM and Keil uVision project generation.

### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.40](https://www.microchip.com/mplab/mplab-x-ide)

## MPLAB® Harmony 3 Configurator Release v3.6.0

### New Features and Fixes
- Added component import and export capability in MHC
- MHC project file structure has been updated to <configuration>.mhc folder.
- Added migration support from harmony.prj to new project structure for old projects.
- Optimized MHC code generation to reduce toolchain build time.
- Added support to display auto scrollbars in project graph view.
- MPLAB Harmony Configurator plugin has been updated to version 3.6.1.
- Bug fixes.

### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.40](https://www.microchip.com/mplab/mplab-x-ide)

## MPLAB® Harmony 3 Configurator Release v3.5.1

### New Features and Fixes
- Added project manifest file to MPLAB X Project.
- Added warning dialog if incompatible version of  MPLAB Harmony Configurator plugin is installed.
- Bug fixes.

### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.40](https://www.microchip.com/mplab/mplab-x-ide)

## MPLAB® Harmony 3 Configurator Release v3.5.0

### New Features and Fixes
- Added support to report MPLAB X analytics.
- TrustZone-M enhancements and bug fixes.
- Added project group feature to support TrustZone-M project.
- Added support to display compiler information in the manifest file.
- Added support to warn user about differences between Manifest and local Packages copies.
- Added support to list only used modules of a project in manifest file.
- Fixed Preprocessor macro update issue for TrustZone-M projects.
- Updated MHC NBM v3.6.0 to support new MHC changes.
- Bug fixes.


### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.40](https://www.microchip.com/mplab/mplab-x-ide)

## MPLAB® Harmony 3 Configurator Release v3.4.1

### New Features and Fixes
- Fixed duplicate file entries in MPLABX mode code generation
- Fixed issue of code generation in  headless mode if the project name is empty.
- Fixed issue in resolving file path in Linux OS.
- Fixed issue of MHC not launching when user name contains accented or Chinese characters

### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.40](https://www.microchip.com/mplab/mplab-x-ide)

## MPLAB® Harmony 3 Configurator Release v3.4.0

### New Features and Fixes
- Added support for TrustZone to create secure and non-secure project
- Added support to generate manifest file containing the harmony packages and its version information
- Added support to generate IAR Embedded Workbench and Keil uVision project
- Added support to include harmony configuration files as part of packaging project into a zip file
- Updated project group icon for easier identification


### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.40](https://www.microchip.com/mplab/mplab-x-ide)

## MPLAB® Harmony 3 Configurator Release v3.3.5

### New Features and Fixes
- Now Customers are notified for latest MHC updates and news feeds
- IPCF file generation issue has been fixed and creates correct xml define tag

### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.30](https://www.microchip.com/mplab/mplab-x-ide)

## MPLAB® Harmony 3 Configurator Release v3.3.4

### New Features and Fixes
- Removed Git management of Harmony 3 modules.
- Release synchronized with [MPLAB® Harmony Content Manager v1.1.0](https://github.com/Microchip-MPLAB-Harmony/contentmanager/releases/tag/v1.1.0).
- Removed now obsoleted Harmony Framework Downloader.
- Removed temporary beta Content Manager

### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.30](https://www.microchip.com/mplab/mplab-x-ide)

## MPLAB Harmony 3 Configurator Release v3.3.3

### New Features and Fixes
- Dot release to bring Content Manager beta updates

### Known Issues
- None

### Development Tools
- [MPLAB® X IDE v5.20](https://www.microchip.com/mplab/mplab-x-ide)

## MPLAB Harmony 3 Configurator Release v3.3.2

### New Features and Fixes
- Dot release to bring Content Manager beta

### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.20](https://www.microchip.com/mplab/mplab-x-ide)


## MPLAB Harmony 3 Configurator Release v3.3.1

### New Features and Fixes
- Fixed conflict in include directories upon changing device.
- Fixed exception throwned if no diff tool was configured in standalone mode.

### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.20](https://www.microchip.com/mplab/mplab-x-ide)

## MPLAB Harmony 3 Configurator Release v3.3.0

### New Features and Fixes
- Internal database management improved.
- Added support of SAM9X60.
- Fixed hardcoded links in Launcher.
- Improved IAR project generator.
- Fixed headless generator, used for continuous integration.

### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.15](https://www.microchip.com/mplab/mplab-x-ide)

## MPLAB Harmony 3 Configurator Release v3.2

### New Features and Fixes
- Added PIC32MK Family Support
- [Make warnings into errors] and [additional warnings] XC32 options are selected for all new Harmony projects
- Enabled Ifo button functionality for downloaded repos
- Fixed html links capability in MHC help

### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.15](https://www.microchip.com/mplab/mplab-x-ide)

## MPLAB Harmony 3 Configurator Release v3.1

### New Features and Fixes
- Initial release

### Known Issues
- None

### Development Tools
- [MPLAB X IDE v5.10](https://www.microchip.com/mplab/mplab-x-ide)
