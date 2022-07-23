#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vtk.vtkIOXML import vtkXMLDataSetWriter
import vtk


point=[[0,0,0],
   [1,1,1],
   [1,0,0],
   [0,1,0],
   [0,0,1]]

line=[[0,1],
   [0,2],
   [0,3],
   [0,4]]

face=[[0,2,3],
   [0,2,4],
   [0,3,4]]


def __MakeMultiPoint(point_list:list):
    ug = vtk.vtkUnstructuredGrid()
    # A polyvertex is a cell represents a set of 0D vertices
    numberOfVertices = len(point_list)

    points = vtk.vtkPoints()
    polyVertex = vtk.vtkPolyVertex()
    polyVertex.GetPointIds().SetNumberOfIds(numberOfVertices)

    for index, item in enumerate(point_list):
        points.InsertNextPoint(item)
        polyVertex.GetPointIds().SetId(index, index)

    
    ug.SetPoints(points)
    ug.InsertNextCell(polyVertex.GetCellType(), polyVertex.GetPointIds())

    return ug



def __MakeMultiLine(point_list:list,line_list:list):
    ug = vtk.vtkUnstructuredGrid()

    points = vtk.vtkPoints()
    multiline = vtk.vtkLine()
    
    for item in point_list:
        points.InsertNextPoint(item)
    ug.SetPoints(points)
        
    for item in line_list:
        for i in range(2):
            multiline.GetPointIds().SetId(i, item[i])
        ug.InsertNextCell(multiline.GetCellType(), multiline.GetPointIds())
    return ug


def __MakeMultiFace(point_list:list,triangle_list:list):
    ug = vtk.vtkUnstructuredGrid()
    points = vtk.vtkPoints()
    triangles = vtk.vtkTriangle()  # 3-point elements
    pixel=vtk.vtkPixel() # 4-point elements
    
    # add points   
    for i in range(len(point_list)):
        points.InsertNextPoint(point_list[i])
    ug.SetPoints(points)
    
    # add elements
    for item in triangle_list:
        if len(item)==3: # add 3-point elements
            for i in range(3): 
                triangles.GetPointIds().SetId(i, item[i])
            ug.InsertNextCell(triangles.GetCellType(), triangles.GetPointIds())    
        elif len(item)==4:  # add 4-point elements
            for i in range(4): 
                pixel.GetPointIds().SetId(i,item[i])
            ug.InsertNextCell(pixel.GetCellType(), pixel.GetPointIds())    
    return ug

def write_vtk(file_name:str):
    u1=__MakeMultiPoint(point)
    u2=__MakeMultiLine(point,line)
    u3=__MakeMultiFace(point,face)
    
    writer = vtkXMLDataSetWriter()
    #u1
    writer.SetInputData(u1)
    writer.SetFileName(file_name+'.point.vtu')
    writer.Write()
    
    writer.SetInputData(u2)
    writer.SetFileName(file_name+'.line.vtu')
    writer.Write()
    
    writer.SetInputData(u3)
    writer.SetFileName(file_name+'.face.vtu')
    writer.Write()    
    
    
write_vtk('0')
