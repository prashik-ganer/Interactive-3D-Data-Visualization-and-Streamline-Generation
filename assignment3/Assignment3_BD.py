# IMPORT VTK
import vtk

# FUNCTION FOR FINDING INTERPOLAED VELOCITY AT GIVEN POINT
def vel_at(point):
    points = vtk.vtkPoints()
    points.InsertNextPoint(point[0], point[1], point[2])
    pointsPolydata = vtk.vtkPolyData()
    pointsPolydata.SetPoints(points)
    probeFilter = vtk.vtkProbeFilter()
    probeFilter.SetInputData(pointsPolydata) 
    probeFilter.SetSourceData(data)
    probeFilter.Update()
    output = probeFilter.GetOutput()
    velocityArray = output.GetPointData().GetArray("vectors")
    if velocityArray: velocity = velocityArray.GetTuple(0)
    return velocity

# RK4 FUNCTION FOR GENERATING STREAMLINE
def rk4_integration(start_point, step_size, max_steps):
    stream = [start_point]
    curr = start_point
    for i in range(max_steps):
        k1 = vel_at(curr)
        k1 = [step_size*i for i in k1]
        k2 = vel_at([curr[i]+0.5*k1[i] for i in range(0,3)])
        k2 = [step_size*i for i in k2]
        k3 = vel_at([curr[i]+0.5*k2[i] for i in range(0,3)])
        k3 = [step_size*i for i in k3]
        k4 = vel_at([curr[i]+k3[i] for i in range(0,3)])
        k4 = [step_size*i for i in k4]
        next = [curr[i]+(k1[i] + 2*k2[i] + 2*k3[i] + k4[i])/6 for i in range(0,3)]
        if not (min_x<=next[0]<=max_x and min_y<=next[1]<=max_y and min_z<=next[2]<=max_z):
            break
        stream.append(next)
        curr = next
    return stream

# LOAD INPUT FILE
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("tornado3d_vector.vti")
reader.Update()
data = reader.GetOutput()

# FIND BOUNDS
bound = data.GetBounds()
min_x, max_x, min_y, max_y, min_z, max_z = bound

# ENTER SEED VALUE
x = float(input("Enter value of x for seed location:"))
y = float(input("Enter value of y for seed location:"))
z = float(input("Enter value of z for seed location:"))
seed_point = [x, y, z]

# FIND FORWARD AND BACKWARD STREAMLINE
streamline = []
streamline += rk4_integration(seed_point, 0.05, 1000)
backward_streamline = rk4_integration(seed_point, -0.05, 1000)
backward_streamline.reverse()

# CONCATENATE BOTH STREAMLINE
streamline = backward_streamline[:-1] + streamline

# CREATE VTP FILE FOR STREAMLINE POINTS
points = vtk.vtkPoints()
for point in streamline:
    points.InsertNextPoint(point[0], point[1], point[2])
stream_line = vtk.vtkCellArray()
stream_line.InsertNextCell(len(streamline)) 
for i in range(len(streamline)):
    stream_line.InsertCellPoint(i)
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetLines(stream_line)
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName("streamline_output.vtp")
writer.SetInputData(polydata)
writer.Write()
print("Output file created successfully as streamline_output.vtp!!")