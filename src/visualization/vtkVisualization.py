import vtk

def show_point(point_list:list):
    vtkPolyData = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    vtkCells = vtk.vtkCellArray()
    
    vtkPolyData.SetPoints(points)
    vtkPolyData.SetVerts(vtkCells)
 
    for k in point_list:
        pointId = points.InsertNextPoint(k)
        vtkCells.InsertNextCell(1)
        vtkCells.InsertCellPoint(pointId)
        vtkCells.Modified()
        points.Modified()
 
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(vtkPolyData)

    mapper.SetScalarVisibility(1)


    actor=vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetPointSize(4)
    
    axes=vtk.vtkAxesActor()
    
    # Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.AddActor(axes)
    renderer.SetBackground(.5, .5, .5)
    renderer.ResetCamera()
    
    # Render Window
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(600,600)
    renderWindow.AddRenderer(renderer)
    
    # Interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    
    # Begin Interaction
    renderWindow.Render()
    renderWindow.SetWindowName('Point Cloud')
    renderWindowInteractor.Start()

if __name__=='__main__':
    kp=[[0,0,0],[5,2,6],[0,1,0],[6.5,8,6]]
    show_point(kp)
    
    
    