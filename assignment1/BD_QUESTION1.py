import vtk

# FUNCTION FOR FINDING INTERSECTION POINT
def intersection(c, v1, v2, p1, p2):
    p = (v1 - c) / (v1 - v2) * (p2 - p1) + p1
    return p

# READING DATA FILE
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("Data/Isabel_2D.vti")
reader.Update()
data = reader.GetOutput()

# TAKING USER INPUT FOR COUNTOR VALUE
pressure = int(input("Enter Countour Pressure Value: "))

# CREATING DATA STRUCTURE FOR STORING INTERSECTION POINTS FOR EACH LINE
contours = vtk.vtkPoints()
lines = vtk.vtkCellArray()

# ITERATE OVER EACH LOOP
numCells = data.GetNumberOfCells()
for i in range(numCells):

    # FINDING ALL FOUR CORNER POINTS OF A CELL
    cell = data.GetCell(i)
    pid1 = cell.GetPointId(0)
    pid2 = cell.GetPointId(1)
    pid3 = cell.GetPointId(3)
    pid4 = cell.GetPointId(2)

    # FINDING PRESSURE VALUE FOR EACH CORNER POINT OF THAT CELL
    dataArr = data.GetPointData().GetArray('Pressure')
    val1 = dataArr.GetTuple1(pid1)
    val2 = dataArr.GetTuple1(pid2)
    val3 = dataArr.GetTuple1(pid3)
    val4 = dataArr.GetTuple1(pid4)

    # FINDING CO-ORDINATES OF EACH CORNER POINT [X, Y, Z]
    cord1 = data.GetPoint(pid1)
    cord2 = data.GetPoint(pid2)
    cord3 = data.GetPoint(pid3)
    cord4 = data.GetPoint(pid4)

    # FINDING CASE NUMBER BASED ON PRESSURE VALUE COMPARISION WITH INPUT CONTOUR VALUE
    # TAKING BINARY TO DECIMAL CONVERSION IN ANTI-CLOCKWISE DIRECTION STARTING THE COUNT FROM BOTTOM LEFT
    index = 0
    if(val1<pressure): index += 1
    if(val2<pressure): index += 2
    if(val3<pressure): index += 4
    if(val4<pressure): index += 8
    
    # CASE WHERE NO INTERSECTION POINT IS POSSIBLE 
    if(index==0 or index==15):
        continue
            
    elif(index==1 or index==14):
        shift_x = intersection(pressure, val1, val2, cord1[0], cord2[0])
        shift_y = intersection(pressure, val4, val1, cord4[1], cord1[1])
        pt1_x, pt1_y = shift_x , cord1[1]
        pt2_x, pt2_y = cord1[0] , shift_y
        
        
    elif(index==2 or index==13):
        shift_x = intersection(pressure, val1, val2, cord1[0], cord2[0])
        shift_y = intersection(pressure, val2, val3, cord2[1], cord3[1])
        pt1_x, pt1_y = shift_x , cord1[1]
        pt2_x, pt2_y = cord2[0] , shift_y

    elif(index==3 or index==12):
        shift_y1 = intersection(pressure, val4, val1, cord4[1], cord1[1])
        shift_y2 = intersection(pressure, val2, val3, cord2[1], cord3[1])
        pt1_x, pt1_y = cord1[0] , shift_y1
        pt2_x, pt2_y = cord2[0] , shift_y2
        
    elif(index==4 or index==11):
        shift_x = intersection(pressure, val3, val4, cord3[0], cord4[0])
        shift_y = intersection(pressure, val2, val3, cord2[1], cord3[1])
        pt1_x, pt1_y = cord2[0] , shift_y
        pt2_x, pt2_y = shift_x , cord3[1]

    # CASE FOR TWO COUNTOR LINES
    # TAKING LINES IN ANTI-CLOCK WISE DIRECTION
    elif(index==5 or index==10):
        shift_x = intersection(pressure, val1, val2, cord1[0], cord2[0])
        shift_y = intersection(pressure, val2, val3, cord2[1], cord3[1])
        pt1_x, pt1_y = shift_x , cord1[1]
        pt2_x, pt2_y = cord2[0] , shift_y
        pt1 = [pt1_x, pt1_y, 25]
        pt2 = [pt2_x, pt2_y, 25]
        pt_id1 = contours.InsertNextPoint(pt1)
        pt_id2 = contours.InsertNextPoint(pt2)
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, pt_id1)
        line.GetPointIds().SetId(1, pt_id2)
        lines.InsertNextCell(line)
        shift_x = intersection(pressure, val3, val4, cord3[0], cord4[0])
        shift_y = intersection(pressure, val4, val1, cord4[1], cord1[1])
        pt1_x, pt1_y = cord1[0]  , shift_y
        pt2_x, pt2_y = shift_x , cord3[1]

        
    elif(index==6 or index==9):
        shift_x1 = intersection(pressure, val1, val2, cord1[0], cord2[0])
        shift_x2 = intersection(pressure, val3, val4, cord3[0], cord4[0])
        pt1_x, pt1_y = shift_x1 , cord1[1]
        pt2_x, pt2_y = shift_x2 , cord3[1]
        
    elif(index==7 or index==8):
        shift_x = intersection(pressure, val3, val4, cord3[0], cord4[0])
        shift_y = intersection(pressure, val4, val1, cord4[1], cord1[1])
        pt1_x, pt1_y = cord1[0]  , shift_y
        pt2_x, pt2_y = shift_x , cord3[1]

    # ADDING THE POINTS IN DATA STRUCTURE
    pt1 = [pt1_x, pt1_y, 25]
    pt2 = [pt2_x, pt2_y, 25]
    pt_id1 = contours.InsertNextPoint(pt1)
    pt_id2 = contours.InsertNextPoint(pt2)
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0, pt_id1)
    line.GetPointIds().SetId(1, pt_id2)
    lines.InsertNextCell(line)

# CREATING POLYDATA FOR LINES
polydata = vtk.vtkPolyData()
polydata.SetPoints(contours)
polydata.SetLines(lines)

# WRITING BACK FILE SO THAT IT CAN BE OPENED IN PARAVIEW
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName("output.vtp")
writer.SetInputData(polydata)
writer.Write()