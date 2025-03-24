"""Abaqus script to reaction forces from a nodal history output request

- script pulls RF & U at a single node (e.g. the control point of a rigid body)
- multiplies RF by SF, which can account for planar symmetry
- results per step saved to individual .csv files in sub-directory "xy-res"

Usage:

    abaqus python pullForceDisp.py Job-1.odb [Job-2.odb ...]

Thomas Schlitt, February 2025
"""

from __future__ import print_function, with_statement
import os.path
import numpy as np

# flip based on pre-processor preference (Default for Abaqus/CAE == False)
flat_inp = True
# determine substring by investigating the Filter function of the XY Data Manager
s = 'Nodal Probe4' # substring used to locate the output history request 
SF = 2.0 #scale factor for forces, if desired

def fromOdb(odbName):
    from odbAccess import openOdb
    from contextlib import closing

    
    with closing(openOdb(odbName)) as odb:
        fdir = os.getcwd()
        xy_dir = os.path.join(fdir, 'xy-res')
        os.makedirs(xy_dir, exist_ok=True)
        
        for _ , step in odb.steps.items():
            for rKey, rVal in step.historyRegions.items():
                if s.upper() in rVal.description.upper():
                    print(rVal.description)
                    time = np.array( rVal.historyOutputs['RF1'].data )[:,0] 
                    F1 =   np.array( rVal.historyOutputs['RF1'].data )[:,1]
                    F2 =   np.array( rVal.historyOutputs['RF2'].data )[:,1]
                    F3 =   np.array( rVal.historyOutputs['RF3'].data )[:,1]
                    U1 =   np.array( rVal.historyOutputs['U1' ].data )[:,1]
                    U2 =   np.array( rVal.historyOutputs['U2' ].data )[:,1]
                    U3 =   np.array( rVal.historyOutputs['U3' ].data )[:,1]
                    break #no need to loop over additional history regions if we've found this step's results
            
            
            A = np.zeros( (len(F1), 7)  )
            A[:,0] = time
            A[:,1] = F1 * SF
            A[:,2] = F2 * SF
            A[:,3] = F3 * SF
            A[:,4] = U1
            A[:,5] = U2
            A[:,6] = U3
            
            fname = os.path.join(xy_dir, f'{step.name}.csv')
            headers = ['time', 'RF1','RF2','RF3','U1','U2','U3',]
            np.savetxt(fname, A, delimiter=",", header=",".join(  headers ) , comments="", fmt="%.6f")
            
      
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

        fromOdb(odbName = os.path.basename(arg))
