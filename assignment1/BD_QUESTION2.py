from vtk import *

# READING DATA FILE
reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_3D.vti')
reader.Update()
data = reader.GetOutput()

# FINDING NUMBER OF CELLS
numCells = data.GetNumberOfCells()

# CREATING COLOR TRANSFER FUNTION
c_t_f= vtkColorTransferFunction()

# CREATING OPACITY TRANSFER FUNTION
o_t_f= vtkPiecewiseFunction()

# ADDING RGB COLOR SPECIFICATIONS FOR COLOR TRANSFER FUNCTION
color_points = [
        (-4931.54,0.0, 1.0, 1.0),  
        (-2508.95, 0.0, 0.0, 1.0),  
        (-1873.9, 0.0, 0.0, 0.5),
        (-1027.16 , 1.0, 0.0, 0.0),
        (-298.031, 1.0, 0.4, 0.0),
        (2594.97, 1.0, 1.0, 0.0)   
    ]
for s,r,g,b in color_points:
    c_t_f.AddRGBPoint(s,r,g,b)

# ADDING OPACITY SPECIFICATIONS FOR OPACITY TRANSFER FUNCTION
o_t_f.AddPoint(-4931.54 , 1.0)
o_t_f.AddPoint(101.815, 0.002)
o_t_f.AddPoint(2594.97, 0.0)

# PERFORMING VOLUME RENDERING BY SETTING VOLUME PROPERTIES 
mapper=vtkSmartVolumeMapper()
mapper.SetInputData(data)
volume_property=vtkVolumeProperty()
volume_property.SetColor(c_t_f)
volume_property.SetScalarOpacity(o_t_f)
actor=vtkVolume()
actor.SetMapper(mapper)
actor.SetProperty(volume_property)

# CREATING RENDERER WITH RENDER WINDOW SIZE 1000*1000
renderer = vtkRenderer()
render_window = vtkRenderWindow()
renderer.SetBackground(1.0, 1.0, 1.0)
render_window.SetSize(1000,1000)
render_window.AddRenderer(renderer)
renderer.AddVolume(actor)
render_windowInteractor = vtkRenderWindowInteractor()
render_windowInteractor.SetRenderWindow(render_window)

# TAKING USER INPUT FOR PHONG SHADING EFFECT ON / OFF
ans=input("Do you want to add Phong shading ? Press y/n: ")

# IF PHONG SHADING IS ON ADD PARAMETERS FOR THE SAME
if ans=='y':
    volume_property.ShadeOn()
    volume_property.SetAmbient(0.5)
    volume_property.SetDiffuse(0.5)
    volume_property.SetSpecular(0.5)

# CREATINNG OUTLINE FILTER
o_f=vtkOutlineFilter()
o_f.SetInputConnection(reader.GetOutputPort())
outline_mapper =vtkPolyDataMapper()
outline_mapper.SetInputConnection(o_f.GetOutputPort())
outline_actor=vtkActor()
outline_actor.GetProperty().SetColor(0, 0, 0)
outline_actor.SetMapper(outline_mapper)
renderer.AddActor(outline_actor)

# START RENDERING AND INTERACTION
render_window.Render()
render_windowInteractor.Start()