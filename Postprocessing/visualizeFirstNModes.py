"""Abaqus script to create N viewports & tile accordingly to visualize the first N modes of a frequency analysis

ASSUMPTIONS:
    - Only one step is present in the .odb results
    - The first step is of type FREQUENCY

INTERACTIVE USAGE:
    
    Within Abaqus/CAE or Abaqus/Viewer utilize the "File > Run Script" command with this script as the argument
    
VERSION SUPPORT:
    - Abaqus/CAE 2024 +

Thomas Schlitt, March 2025
"""

from abaqus import *
from abaqusConstants import *

N_MODES = [2,4,6][1] #control for how many viewports/modes to view simultaneously
                     #  change the index of the previous list to change total # of viewports

def setup_N_modes():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import job
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    
    vp = session.viewports[session.currentViewportName]
    
    
    if len(session.viewports.keys() )  < N_modes:
        
    