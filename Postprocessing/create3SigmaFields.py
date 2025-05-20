"""Abaqus script used to create 3 Sigma Field response variable for RMISES and RTA and save to temporary session step

ASSUMPTIONS:
    - user has performed a random vibration analysis with the step name including the tag: '_x' or '_y' to indicate the excitation direction
        - e.g. step name = random_vibe_x

INPUTS:
    - user must have odb of interest currently open with Abaqus/CAE & listed as displayed object in the viewport

INTERACTIVE USAGE:
    
    Within Abaqus/CAE or Abaqus/Viewer utilize the "File > Run Script" command with this script as the argument
    
VERSION SUPPORT:
    - Abaqus/CAE 2024 +

Thomas Schlitt, March 2025
"""
from abaqus import *
from abaqusConstants import *


g = 9810 #[mm/s2] used to normalize the acceleration outputs
field_vars = ['RMISES', 'RTA']


def create_3sigma_fields():
    """
    Macro to create 3x sigma fields for RMISES & RTA1, RTA2, RTA3
    """
    vp = session.viewports[session.currentViewportName]
    odbName = vp.odbDisplay.name
    odb = session.odbs[odbName]
    steps = odb.steps

    scratchOdb = session.ScratchOdb(odb=odb)
    if len( scratchOdb.steps.keys() ) == 0: # if no session step, create one
        sessionStep = scratchOdb.Step(name='Session Step-1',
                                        description='Step for Viewer non-persistent fields',
                                        domain=TIME,
                                        timePeriod=1.0)
        sessionFrame = sessionStep.Frame(frameId=0,
                                         frameValue=0.0,
                                         description='Session Frame')
    else: #if session step already exists, create new session step with 1 higher counter
        #Abaqus by default doesn't have an iterable counter string on their session step
        ks =  scratchOdb.steps.keys()
        ks = [f'{k}-0' for k in ks if not k.split('-'[-1])[0].isnumeric()  ]
        itrs = [ int( n.split('-')[-1] ) for n in ks ]
        sessionStep = scratchOdb.Step(name=f'Session Step-{len(itrs)+1}',
                                      description='Step for Viewer non-persistent fields',
                                      domain=TIME,
                                      timePeriod=1.0)
        sessionFrame = sessionStep.Frame(frameId=0,
                                         frameValue=0.0,
                                         description='Session Frame')
                                         
    for stp in steps.values():
        if stp.procedure.upper() != '*RANDOM RESPONSE': # skip this step if not a random response step
            continue
        for i,f in enumerate(stp.frames): #loop over all frames except for base-frame
            if i == 0: continue # skip first frame
            load_direction = stp.name.split('_')[-1]
            if 'RMISES' in f.fieldOutputs.keys():
                scaled_RMISES = f.fieldOutputs['RMISES'] * 3
                sessionFrame.FieldOutput(name=f'RMISES_3Sigma_{load_direction}',
                                         description=f'3Sigma Scaled RMISES in {load_direction} direction excitation',
                                         field=scaled_RMISES)

            if 'RTA' in f.fieldOutputs.keys():
                component = {'x':'1',
                             'y':'2',
                             'z':'3'}[load_direction] #use to swap direction to abaqus global component
                scaled_RTA = f.fieldOutputs['RTA'].getScalarField(componentLabel=f"RTA{component}")
                scaled_RTA *= 3 / g
                sessionFrame.FieldOutput(name=f'RTA{component}_Gs_3Sigma_{load_direction}',
                                         description=f'3Sigma Scaled RTA (Gs) in {load_direction} direction excitation',
                                         field=scaled_RTA)


    vp.odbDisplay.setFrame(sessionFrame)
    print(f'Session Step creation completed! Use primary variable navigation to plot vars')
    

if __name__ == '__main__':
    create_3sigma_fields()