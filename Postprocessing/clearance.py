"""Abaqus script to compute user defined clearance (uCL) between two parts

- uCL is calculated at i-th node of "A-Nodes" & can display vector distance between i-th node and closest B-Node
- user may choose to perform operation on a copy of the odb, if desired

ASSUMPTIONS:
    - user must have requested COOR as an output variable for this analysis
    - user must have defined two, and only two, node sets "A-NODES" and "B-NODES" defined within the model
    
USAGE:

    abaqus python clearance.py Job-1.odb [Job-2.odb ...]

Thomas Schlitt, January 2025
"""

from __future__ import print_function, with_statement
import os.path

import numpy as np

foName = 'uCL'  # fieldOutput name for results
createOdbCopyBool=False  # switch this to true to modify a copy of the .odb rather than original


def nearest_neighbor(aBlock, COOR_B):
    '''
    function to loop through displacement data & find nearest node
    '''

    data = []
    b_nodes_table = [ np.array(  v.data ) for v in COOR_B.values ]
    for pt_a in aBlock.data:
        dist = np.sum((b_nodes_table - pt_a) ** 2, axis=1) #squared euclidean for speed
        nearest_idx = np.argmin(dist)

        pt_b = b_nodes_table[nearest_idx]
        v = pt_b - pt_a # b relative to a
        data.append( (*v,) )
    return data

def calculate(outputFrame, a_nodes, b_nodes):
    """Calculate uCL fieldOutput and store in outputFrame"""
    import abaqusConstants

    globalCOORD = outputFrame.fieldOutputs["COORD"]
    COORD_A = globalCOORD.getSubset(region=a_nodes)
    COORD_B = globalCOORD.getSubset(region=b_nodes)
    CLEARANCE = outputFrame.FieldOutput(
        name=foName,
        description="local clearance value",
        type=globalCOORD.type,
    )

    from abaqusConstants import MAGNITUDE
    CLEARANCE.setValidInvariants((MAGNITUDE,))

    for aBlock in COORD_A.bulkDataBlocks:
        options = dict(
            position=aBlock.position,
            instance=aBlock.instance,
            labels=np.unique(aBlock.nodeLabels),
            data=nearest_neighbor(aBlock, COORD_B)
            )
        CLEARANCE.addData(**options)


def fromOdb(odbName):
    """Add signed uCL fieldOutput to each odb frame which contain COORDS"""

    from odbAccess import openOdb
    from contextlib import closing
    flat_inp = True
    
    with closing(openOdb(odbName)) as odb:
        if flat_inp:
            ka = [kk for kk in odb.rootAssembly.instances['PART-1-1'].nodeSets.keys() if kk.upper() == 'A-NODES'][0]
            kb = [kk for kk in odb.rootAssembly.instances['PART-1-1'].nodeSets.keys() if kk.upper() == 'B-NODES'][0]
            a_nodes = odb.rootAssembly.instances['PART-1-1'].nodeSets[ka]
            b_nodes = odb.rootAssembly.instances['PART-1-1'].nodeSets[kb]
        else:
            ka = [kk for kk in odb.rootAssembly.nodeSets.keys() if kk.upper() == 'A-NODES'][0]
            kb = [kk for kk in odb.rootAssembly.nodeSets.keys() if kk.upper() == 'B-NODES'][0]
            a_nodes = odb.rootAssembly.nodeSets[ka]
            b_nodes = odb.rootAssembly.nodeSets[kb]


        for step in odb.steps.values():
            for frame in step.frames:
                if "COORD" in frame.fieldOutputs and not foName in frame.fieldOutputs:
                    print(step.name, frame.description)
                    calculate(frame, a_nodes, b_nodes)


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

