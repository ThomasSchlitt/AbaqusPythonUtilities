"""Abaqus script used create a simple 2-part assembly to test analytical connectors

INTERACTIVE USAGE:
    
    Within Abaqus/CAE or Abaqus/Viewer utilize the "File > Run Script" command with this script as the argument
    
VERSION SUPPORT:
    - Abaqus/CAE 2024 +

Thomas Schlitt, October 2024
"""
from abaqus import *
from abaqusConstants import *
import __main__


def bolted_joint_test_model():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import optimization
    import step
    import interaction
    import load
    import mesh
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    
    
    vp = session.viewports[session.currentViewportName] #get currently active viewport

    m1 = mdb.Model(name='TestJoint', modelType=STANDARD_EXPLICIT)
    a = mdb.models['TestJoint'].rootAssembly
    vp.setValues(displayedObject=a)
    
    s = m1.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(0.0, -5.0), point2=(35.0, 10.0))
    s.CircleByCenterPerimeter(center=(35.0, 2.5), point1=(35.0, 10.0))
    s.CoincidentConstraint(entity1=v[4], entity2=g[4], addUndoState=False)
    s.EqualDistanceConstraint(entity1=v[2], entity2=v[3], midpoint=v[4], 
        addUndoState=False)
        
    vp.view.setValues(nearPlane=176.098, 
        farPlane=201.025, width=89.3895, height=42.6698, cameraPosition=(15.3748, 
        0.897657, 188.562), cameraTarget=(15.3748, 0.897657, 0))
    s.CircleByCenterPerimeter(center=(35.0, 2.5), point1=(40.0, 2.5))
    s.autoTrimCurve(curve1=g[6], point1=(28.2529239654541, -1.58796572685242))
    s.autoTrimCurve(curve1=g[4], point1=(34.9330368041992, 5.38558101654053))
    s.autoTrimCurve(curve1=g[9], point1=(35.3462371826172, 8.69974231719971))
    s.autoTrimCurve(curve1=g[10], point1=(35.1396408081055, -3.59026980400085))

    p = m1.Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = m1.parts['Part-1']
    p.BaseSolidExtrude(sketch=s, depth=20.0)
    s.unsetPrimaryObject()
    p = m1.parts['Part-1']
    vp.setValues(displayedObject=p)
    del m1.sketches['__profile__']
    p = m1.parts['Part-1']
    p.features['Solid extrude-1'].setValues(depth=10.0)
    p = m1.parts['Part-1']
    p.regenerate()
    p = m1.parts['Part-1']
    p.regenerate()
    vp.partDisplay.setValues(mesh=ON)
    vp.partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    vp.partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    p = m1.parts['Part-1']
    p.seedPart(size=2.0, deviationFactor=0.05, minSizeFactor=0.1)
    p = m1.parts['Part-1']
    p.features['Solid extrude-1'].setValues(depth=5.0)
    p = m1.parts['Part-1']
    p.regenerate()
    p = m1.parts['Part-1']
    p.generateMesh()
    p = m1.parts['Part-1']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.deleteMesh(regions=pickedRegions)
    p = m1.parts['Part-1']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=HEX_DOMINATED, 
        algorithm=MEDIAL_AXIS)
    p = m1.parts['Part-1']
    p.generateMesh()
    p = m1.parts['Part-1']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.deleteMesh(regions=pickedRegions)
    p = m1.parts['Part-1']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=HEX)
    p = m1.parts['Part-1']
    p.generateMesh()
    a = m1.rootAssembly
    vp.setValues(displayedObject=a)
    a = m1.rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = m1.parts['Part-1']
    a.Instance(name='Part-1-1', part=p, dependent=ON)
    a = m1.rootAssembly
    p = m1.parts['Part-1']
    a.Instance(name='Part-1-2', part=p, dependent=ON)
    p1 = a.instances['Part-1-2']
    p1.translate(vector=(46.75, 0.0, 0.0))
    vp.view.fitView()
    vp.view.setValues(nearPlane=175.228, 
        farPlane=303.393, width=145.413, height=72.5424, viewOffsetX=-1.46994, 
        viewOffsetY=1.80671)
    vp.view.setValues(nearPlane=174.266, 
        farPlane=304.355, width=144.615, height=72.1443, viewOffsetX=-5.30432, 
        viewOffsetY=8.56762)
    a = m1.rootAssembly
    a.rotate(instanceList=('Part-1-2', ), axisPoint=(0.0, 0.0, 0.0), 
        axisDirection=(0.0, 0.0, 1.0), angle=180.0)
    #: The instance Part-1-2 was rotated by 180. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 0., 1.
    vp.view.setValues(nearPlane=164.205, 
        farPlane=244.439, width=136.266, height=67.9791, cameraPosition=(-21.2869, 
        115.02, 176.649), cameraUpVector=(-0.145843, 0.537457, -0.830584), 
        cameraTarget=(16.8303, 2.53711, 17.4644), viewOffsetX=-4.99808, 
        viewOffsetY=8.07297)
    vp.view.setValues(nearPlane=158.863, 
        farPlane=249.782, width=191.88, height=95.7232, viewOffsetX=6.54159, 
        viewOffsetY=7.66609)
    a = m1.rootAssembly
    a.translate(instanceList=('Part-1-2', ), vector=(116.75, 5.0, 5.0))
    #: The instance Part-1-2 was translated by 116.75, 5., 5. with respect to the assembly coordinate system
    vp.view.setValues(nearPlane=159.255, 
        farPlane=254.988, width=192.353, height=95.9594, cameraPosition=(90.9657, 
        109.93, 173.761), cameraUpVector=(-0.339012, 0.6178, -0.709503), 
        cameraTarget=(24.5208, 3.67708, 19.6812), viewOffsetX=6.55772, 
        viewOffsetY=7.685)
    vp.view.setValues(nearPlane=160.306, 
        farPlane=254.003, width=193.622, height=96.5924, cameraPosition=(94.1046, 
        115.871, 168.775), cameraUpVector=(-0.349401, 0.592369, -0.72596), 
        cameraTarget=(24.7638, 4.23652, 19.8632), viewOffsetX=6.60098, 
        viewOffsetY=7.7357)
    vp.view.setValues(nearPlane=169.932, 
        farPlane=244.377, width=117.606, height=58.6702, viewOffsetX=9.97449, 
        viewOffsetY=5.59862)
    vp.enableMultipleColors()
    vp.setColor(initialColor='#BDBDBD')
    cmap=vp.colorMappings['Part instance']
    vp.setColor(colorMapping=cmap)
    vp.disableMultipleColors()
    vp.view.setValues(nearPlane=182.385, 
        farPlane=232.12, width=126.225, height=62.97, cameraPosition=(-0.513361, 
        -10.2461, 209.433), cameraUpVector=(-0.0692794, 0.948848, -0.308038), 
        cameraTarget=(18.955, -3.17798, 11.9076), viewOffsetX=10.7055, 
        viewOffsetY=6.00893)
    vp.view.setValues(nearPlane=175.095, 
        farPlane=242.291, width=121.18, height=60.4532, cameraPosition=(-40.3736, 
        41.9325, 196.259), cameraUpVector=(0.0697939, 0.844939, -0.530289), 
        cameraTarget=(17.1502, -0.728495, 11.0128), viewOffsetX=10.2776, 
        viewOffsetY=5.76876)
    vp.assemblyDisplay.setValues(mesh=ON)
    vp.view.setValues(nearPlane=175.189, 
        farPlane=245.167, width=121.245, height=60.4855, cameraPosition=(-40.3624, 
        139.742, 146.21), cameraUpVector=(0.332123, 0.475974, -0.814336), 
        cameraTarget=(15.6762, 6.57543, 9.93331), viewOffsetX=10.2831, 
        viewOffsetY=5.77185)
        
    vp.partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON, mesh=OFF)
    vp.partDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    p1 = mdb.models['TestJoint'].parts['Part-1']
    vp.setValues(displayedObject=p1)
    mdb.models['TestJoint'].Material(name='steel')
    mdb.models['TestJoint'].materials['steel'].Density(table=((7.89e-09, ), ))
    mdb.models['TestJoint'].materials['steel'].Elastic(table=((200000.0, 0.3), ))
    mdb.models['TestJoint'].HomogeneousSolidSection(name='steel_solidSection', 
        material='steel', thickness=None)
    p = mdb.models['TestJoint'].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(cells=cells, name='steel_section')
    p = mdb.models['TestJoint'].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='steel_solidSection', 
        offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    vp.partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF, mesh=ON)
    vp.partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    elemType1 = mesh.ElemType(elemCode=C3D8, elemLibrary=STANDARD, 
        secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
    p = mdb.models['TestJoint'].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    
    a = mdb.models['TestJoint'].rootAssembly
    a.regenerate()
    vp.setValues(displayedObject=a)
    vp.assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
            
        
if __name__ == '__main__':
    bolted_joint_test_model()