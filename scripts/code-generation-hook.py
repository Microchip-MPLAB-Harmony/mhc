from harmony3 import project
"""
Called before the code generatio process starts
"""
def preGenerateEvent():
    print('preGenerateEvent')

"""
Called before validating file list
"""
def interfaceValidationEvent():
    print('interfaceValidationEvent')

"""
called before processing data model
"""
def processDataModel(state):
    print('processDataModel')

"""
Called before file processing
"""
def preFilePreprocessEvent(state):
    print('preFilePreprocessEvent')

"""
Called before removing any generate item
"""
def preItemRemovalEvent(state):
    print('preItemRemovalEvent')

"""
Called before final file processing
"""
def preFinalProcessing(state):
    print('preFinalProcessing')

"""
Called after file processing
"""
def postFinalProcessing(state):
    print('postFinalProcessing')
    project.generate_project(FOLDER_NAME, PROJECT_NAME, state)
