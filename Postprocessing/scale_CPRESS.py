"""Abaqus script to convert the CPRESS results in each from to one unit to another via a simple scaleFactor

- User must modify two inputs:
    - SF = scale factor to be used as a conversion on the CPRESS field
    - fieldTag = name that designates the converted field .... e.g. mmHg
- user may choose to perform operation on a copy of the odb, if desired

ASSUMPTIONS:
    - user must have requested CPRESS as an output variable for this analysis

USAGE:
    
    abaqus python scale_CPRESS.py Job-1.odb [Job-2.odb ...]

Thomas Schlitt, December 2025
"""

from __future__ import print_function, with_statement

from ctypes.wintypes import FLOAT
from abaqusConstants import NODAL, ELEMENT_NODAL
import os.path

import numpy as np

# --------------------------------------------------------------------------------------------------
# CONTROLS
# --------------------------------------------------------------------------------------------------
fieldTag = 'mmHg'  # fieldOutput tag to be added to CPRESS field name
SF = 7500.62  # conversion factor from MPa to mmHg
createOdbCopyBool=True  # switch this to true to modify a copy of the .odb rather than original

# --------------------------------------------------------------------------------------------------
# SUPPORTING FUNCTIONS
# --------------------------------------------------------------------------------------------------
foName = f"CPRESS_{fieldTag}"
def scale_CPRESS(outputFrame):
    """scale your CPRESS value by some SF provided above"""
    CPRESS = outputFrame.fieldOutputs['CPRESS']
    new_CPRESS = outputFrame.FieldOutput(
        name=foName,
        description="converted CPRESS",
        type=CPRESS.type
        )

    for ii, cblock in enumerate(CPRESS.bulkDataBlocks):
        data = np.asarray(cblock.data, dtype=np.float64) * SF
        options = dict(
            position=cblock.position,  #cblock.position, #should just be NODAL
            instance = cblock.instance,
            labels = cblock.nodeLabels, #cblock.nodeLabels
            data = data,
        )
        if np.any(cblock.sectionPoint):
            options["sectionPoint"] = cblock.sectionPoint
        new_CPRESS.addData(**options)


def fromOdb(odbName):
    """scale the results for the odb"""

    from odbAccess import openOdb
    from contextlib import closing

    with closing(openOdb(odbName)) as odb:
        for step in odb.steps.values():
            for frame in step.frames:
                if "CPRESS" in frame.fieldOutputs and not foName in frame.fieldOutputs:
                    print(step.name, frame.description)
                    scale_CPRESS(frame)

# --------------------------------------------------------------------------------------------------
# SCRIPT
# --------------------------------------------------------------------------------------------------
import sys
for arg in sys.argv[1:]:
    if "--help" == arg:
        print(__doc__)
    elif "--test" == arg:
        import doctest
        doctest.testmod(verbose=True)
    else:
        ln = 50
        print('-'*ln)
        print(arg, file=sys.stderr)

        if createOdbCopyBool:
            import shutil
            shutil.copy(arg, os.path.basename(arg)+'-copy.odb') 
            fromOdb(odbName = os.path.basename(arg)+'-copy.odb')
        else:
            fromOdb(odbName = os.path.basename(arg))

