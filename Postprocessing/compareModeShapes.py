"""Abaqus script used to compare the first N-mode shapes of two similar models

- First N-mode shapes are plotted using the deformed shape & color-coded by Material Assignment
- Resulting mode shapes are animated using the Full-Amplitude Scale Factor method and saved to a 
    subdirectory of the current working directory of Abaqus/CAE

ASSUMPTIONS:
    - Only one step is present in the .odb results
    - The first step is of type FREQUENCY
    - Assumed view of User-1 has been provided:
        - recommended that user aligns view interactively in Abq/CAE, saves the user-defined view, then
          copies the resulting User-1 definition from the .rpy file into this script

INPUTS:
    odb_a_fname:    absolute filepath of first odb (String)
    odb_b_fname:    absolute filepath of second odb (String)

INTERACTIVE USAGE:
    
    Within Abaqus/CAE or Abaqus/Viewer utilize the "File > Run Script" command with this script as the argument
    
VERSION SUPPORT:
    - Abaqus/CAE 2025.HF1 +

Thomas Schlitt, March 2025
"""
from abaqus import *
from abaqusConstants import *


N_MODES = 12  #control for how many comparative modes to post-process

# following should be Absolute Filepaths for two odbs
odb_a_fname = 'C:/TEMP/model_A.odb'
odb_b_fname = 'C:/TEMP/model_B.odb'

# Interactively save the User-1 view as desired position, then copy the resulting code from the .rpy file here:
session.View(name='User-1', nearPlane=3055.6, farPlane=5360.8, width=2264.5,
                 height=2152.5, projection=PARALLEL,
                 cameraPosition=(-2762.6, 2300.1, -3161.6),
                 cameraUpVector=(0.45972, 0.77601, 0.43183),
                 cameraTarget=(468.39, 697.41, -38.545),
                 viewOffsetX=0,viewOffsetY=0, autoFit=OFF)

def compare_modeShapes():
    """
    iteratively plots first 12-modes for two models A + B and saves result to animation directory
        assumes only one step in odb; first step is freq-extraction"
    """
    odb_a = session.odbs[odb_a_fname]
    odb_b = session.odbs[odb_b_fname]

    # setup code for 2-viewport vertical tile comparison
    h = session.drawingArea.height
    w = session.drawingArea.width
    ori = session.drawingArea.origin

    # Left View
    vp_left = session.Viewport(name='Left', origin=(ori[0], ori[1]),
                     width=w / 2, height=h)
    vp_left.setValues(displayedObject=odb_a)

    # Right View
    vp_right = session.Viewport(name='Right', origin=(ori[0] + w / 2, ori[1]),
                     width=w / 2, height=h)
    vp_right.setValues(displayedObject=odb_b)
    vps = [vp_left, vp_right]

    # link our viewports
    session.linkedViewportCommands.setValues(linkViewports=True)
    session.linkedViewportCommands.setValues(frameSelection=True,
                                             frameAdvancement=False)
    vp_right.viewportAnnotationOptions.setValues(title=OFF, state=OFF,
                                                 triad=ON,legend=OFF,
                                                 annotations=ON, compass=OFF)

    # setup vp coloring and initial view
    for vp in vps:
        vp.view.setValues(session.views['User-1'])
        vp.view.setProjection(projection=PARALLEL)

        vp.enableMultipleColors()
        vp.setColor(initialColor='#BDBDBD')
        cmap = vp_left.colorMappings['Material']
        vp.setColor(colorMapping=cmap)
        vp.disableMultipleColors()

    # setup animation output dir
    import os
    fdir = os.getcwd()
    anim_dir = os.path.join(fdir, 'animations')
    os.makedirs(anim_dir, exist_ok=True)

    # modify animation parameters
    vp_left.animationController.setValues(animationType=SCALE_FACTOR)
    session.animationOptions.setValues(mode=SWING,
                                       relativeScaling=FULL_CYCLE,
                                       numScaleFactorFrames=16)
    session.mp4Options.setValues(compressionQuality=90)
    session.imageAnimationOptions.setValues(vpDecorations=OFF,
                                            vpBackground=OFF,
                                            compass=OFF, timeScale=1, frameRate=32)
    # move to next frame
    vp_left.odbDisplay.setFrame(step=0, frame=1)
    # Turn animation on
    vp_left.animationController.play(duration=UNLIMITED)
    for i in range(1, N_MODES+1):
        # move to next frame
        vp_left.odbDisplay.setFrame(step=0, frame=i)

        # get odb_a current freq value
        w_a = float( odb_a.steps.values()[0].frames[i].description.split()[-2]  )
        # write left text-annotation
        comp = 'xyz'[np.argmax(EM_A[i - 1, :])]
        tA = odb_a.userData.Text(name='Text-A',
                                 text=f'Mode #{i} \nFreq = {w_a:.1f} Hz',
                                 offset=(9.96667, 56.9333))
        vp_left.plotAnnotation(annotation=tA)


        w_b = float(  odb_b.steps.values()[0].frames[i].description.split()[-2] )
        # write right text-annotation
        comp = 'xyz'[np.argmax(EM_B[i-1, :])]
        tB = odb_b.userData.Text(name='Text-B',
                                 text=f'Mode #{i} \nFreq = {w_b:.1f} Hz',
                                 offset=(9.96667, 56.9333))
        vp_right.plotAnnotation(annotation=tB)

        # write animation to file
        session.writeImageAnimation(
            fileName=os.path.join(anim_dir, f'mode-{i}'),
            format=MP4, canvasObjects=(*vps,))
    # Turn animation off
    vp_left.animationController.setValues(animationType=NONE)
    
if __name__ == '__main__':
    compare_modeShapes()