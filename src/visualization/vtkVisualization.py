import numpy as np
import vtk

class VtkPointCloud:

    def __init__(self, zMin=-10.0, zMax=10.0, maxNumPoints=1e6):
        self.maxNumPoints = maxNumPoints
        self.vtkPolyData = vtk.vtkPolyData()
        self.clearPoints()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.vtkPolyData)
        mapper.SetColorModeToDefault()
        mapper.SetScalarRange(zMin, zMax)
        mapper.SetScalarVisibility(1)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(mapper)

    def addPoint(self, point):
        if self.vtkPoints.GetNumberOfPoints() < self.maxNumPoints:
            pointId = self.vtkPoints.InsertNextPoint(point[:])
            self.vtkDepth.InsertNextValue(point[2])
            self.vtkCells.InsertNextCell(1)
            self.vtkCells.InsertCellPoint(pointId)
        else:
            print("Warning! The number of point is more than 1e6!")
            self.vtkPoints.SetPoint(self.maxNumPoints, point[:])
        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.vtkDepth.Modified()

    def clearPoints(self):
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkDepth = vtk.vtkDoubleArray()
        self.vtkDepth.SetName('DepthArray')
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkDepth)
        self.vtkPolyData.GetPointData().SetActiveScalars('DepthArray')


def show_point(point_list:list):
    z_min=np.min(np.array(point_list),axis=0)[2]
    z_max=np.max(np.array(point_list),axis=0)[2]
    print(z_max)
    print(z_min)
    pointCloud = VtkPointCloud(zMin=z_min,zMax=z_max)

    for k in point_list:
        pointCloud.addPoint(k)
    
    # Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(pointCloud.vtkActor)
    renderer.SetBackground(.2, .1, .1)
    renderer.ResetCamera()
    
    # Render Window
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    
    # Interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    
    # Begin Interaction
    renderWindow.Render()
    renderWindowInteractor.Start()

def save_vtk(point:list,element:list,out_name:str):
    Points = vtk.vtkPoints()
    Cells = vtk.vtkCellArray()
    one_tri = vtk.vtkTriangle()
    one_quad=vtk.vtkPolygon()
    one_quad.GetPointIds().SetNumberOfIds(4)  # make a quad
    # print(point)
    for each in point:
        print(each)
        Points.InsertNextPoint(each)
    # generate triangles or quad
    for each in element:
        # print(each)
        if len(each)==3:
            one_tri.GetPointIds().SetId(0,each[0])
            one_tri.GetPointIds().SetId(1,each[1])
            one_tri.GetPointIds().SetId(2,each[2])
        Cells.InsertNextCell(one_tri)  
        if len(each)==4:
            one_quad.GetPointIds().SetId(0,each[0])
            one_quad.GetPointIds().SetId(1,each[1])
            one_quad.GetPointIds().SetId(2,each[3])
            one_quad.GetPointIds().SetId(3,each[2])
        Cells.InsertNextCell(one_quad)
        
    # # out put data
    out_data = vtk.vtkPolyData()
    out_data.SetPoints(Points)
    out_data.SetPolys(Cells)
    out_data.Modified()
    writer = vtk.vtkXMLPolyDataWriter();
    writer.SetFileName(str(out_name)+".vtp")
    if vtk.VTK_MAJOR_VERSION <= 5:
        out_data.Update()
        writer.SetInput(out_data)
    else:
        writer.SetInputData(out_data)
    writer.Write()
