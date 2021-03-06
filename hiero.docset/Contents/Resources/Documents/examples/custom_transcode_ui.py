# Example of the user interface for a custom transcoder (goes with the custom_transcode.py code)

import os.path
import hiero.ui
import sys

import PySide.QtCore
import PySide.QtGui

from hiero.exporters import FnTranscodeExporter, FnTranscodeExporterUI

import custom_transcode

class CustomTranscodeUI(FnTranscodeExporterUI.TranscodeExporterUI):
  def __init__(self, preset):
    """Initialize"""
    FnTranscodeExporterUI.TranscodeExporterUI.__init__(self, preset)
    
    self._displayName = "Custom Transcode"
    self._taskType = custom_transcode.CustomTranscode
    
    
  def insertAudioCheckboxChanged(self, state):
    # Slot to handle change of checkbox state
    self._preset._properties["insertAudio"] = state == PySide.QtCore.Qt.Checked

  def populateUI (self, widget, exportTemplate):
    layout = PySide.QtGui.QFormLayout()
    layout.setContentsMargins(9, 0, 9, 0)
    self.buildCodecUI(layout)
    
    platformUsesQuicktime = sys.platform.startswith("win32") or sys.platform.startswith("darwin")

    # Hide option of platform doesnt use quicktime
    if platformUsesQuicktime:
      # Create Checkbox
      audioCheckbox = PySide.QtGui.QCheckBox()
      
      # Set checkstate according to preset value
      audioCheckbox.setCheckState(PySide.QtCore.Qt.Unchecked)
      if self._preset._properties["insertAudio"]:
        audioCheckbox.setCheckState(PySide.QtCore.Qt.Checked)    
      
      # Connect signal
      audioCheckbox.stateChanged.connect(self.insertAudioCheckboxChanged)
      
      # Set Tooltip
      audioCheckbox.setToolTip("If writing a mov it may be possible to inject audio from a single file. First audio file on first audio track will be used.")
      
      # Add Checkbox to layout
      layout.addRow("Insert Audio Where Possible:", audioCheckbox)
    
    widget.setLayout(layout)



hiero.ui.taskUIRegistry.registerTaskUI(custom_transcode.CustomTranscodePreset, CustomTranscodeUI)
