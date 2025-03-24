"""Abaqus script used create a simple cube assembly in Abaqus CAE. Useful when trying to quickly test/investigate setup workflows

INTERACTIVE USAGE:
    
    Within Abaqus/CAE or Abaqus/Viewer utilize the "File > Run Script" command with this script as the argument
    
VERSION SUPPORT:
    - Abaqus/CAE 2024 +

Thomas Schlitt, October 2024
"""

def TestCube():
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
    
    
    vps = session.viewports.keys()   						#get all active viewport names
    #vp = session.viewports[session.currentViewportName] 	#get activeviewport object
    vp = session.currentViewportName

    m1 = mdb.Model(name='TestCube', modelType=STANDARD_EXPLICIT)
    a = mdb.models['TestCube'].rootAssembly
    
    session.viewports[vp].setValues(displayedObject=a)
    session.viewports[vp].partDisplay.setValues(mesh=OFF)
    session.viewports[vp].partDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    session.viewports[vp].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)

    session.viewports[vp].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF)
    session.viewports[vp].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)
    session.viewports[vp].setValues(displayedObject=None)
    print('a')
    s1 = m1.ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.rectangle(point1=(-25.0, -25.0), point2=(25.0, 25.0))
    p = m1.Part(name='Part-1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = m1.parts['Part-1']
    p.BaseSolidExtrude(sketch=s1, depth=50.0)
    s1.unsetPrimaryObject()
    p = m1.parts['Part-1']
    session.viewports[vp].setValues(displayedObject=p)
    del m1.sketches['__profile__']
    session.viewports[vp].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports[vp].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    session.viewports[vp].view.setValues(nearPlane=130.059, 
        farPlane=235.777, width=123.294, height=61.032, cameraPosition=(
        106.335, 104.166, 131.335), cameraUpVector=(-0.579126, 0.573782, 
        -0.579126), cameraTarget=(1.04897, -2.09791, 26.049))
    m1.Material(name='steel')
    m1.materials['steel'].Density(table=((7.8e-09, ), ))
    m1.materials['steel'].Elastic(table=((200000.0, 0.3), ))
    m1.HomogeneousSolidSection(name='steel-section', 
        material='steel', thickness=None)
    p = m1.parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(cells=cells, name='steel-cube')
    p = m1.parts['Part-1']
    p.SectionAssignment(region=region, sectionName='steel-section', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    session.viewports[vp].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF, mesh=ON)
    session.viewports[vp].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    p = m1.parts['Part-1']
    p.seedPart(size=5.0, deviationFactor=0.1, minSizeFactor=0.1)
    p = m1.parts['Part-1']
    p.generateMesh()
    a = m1.rootAssembly
    session.viewports[vp].setValues(displayedObject=a)
    a1 = m1.rootAssembly
    a1.DatumCsysByDefault(CARTESIAN)
    p = m1.parts['Part-1']
    a1.Instance(name='Part-1-1', part=p, dependent=ON)
    
    session.viewports[vp].view.fitView()
    session.viewports[vp].assemblyDisplay.setValues(mesh=ON)
    
    
if __name__ == '__main__':
    TestCube()