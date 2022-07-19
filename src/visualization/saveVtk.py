#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vtk.vtkIOXML import vtkXMLDataSetWriter
from vtk.vtkCommonCore import vtkPoints
from vtk.vtkCommonDataModel import (
    vtkHexagonalPrism,
    vtkHexahedron,
    vtkLine,
    vtkPentagonalPrism,
    vtkPixel,
    vtkPolyLine,
    vtkPolyVertex,
    vtkPolygon,
    vtkPyramid,
    vtkQuad,
    vtkTetra,
    vtkTriangle,
    vtkTriangleStrip,
    vtkUnstructuredGrid,
    vtkVertex,
    vtkVoxel,
    vtkWedge
)


p=[[0,0,0],
   [1,1,1],
   [1,0,0],
   [0,1,0],
   [0,0,1]]
def MakePolyVertex(p:list):
    
    # A polyvertex is a cell represents a set of 0D vertices
    numberOfVertices = len(p)

    points = vtkPoints()
    for item in p:
        points.InsertNextPoint(item)


    polyVertex = vtkPolyVertex()
    polyVertex.GetPointIds().SetNumberOfIds(numberOfVertices)

    for i in range(0, numberOfVertices):
        polyVertex.GetPointIds().SetId(i, i)

    ug = vtkUnstructuredGrid()
    ug.SetPoints(points)
    ug.InsertNextCell(polyVertex.GetCellType(), polyVertex.GetPointIds())

    return ug


def write_vtk(file_name:str):
    u=MakePolyVertex(p)
    
    writer = vtkXMLDataSetWriter()
    writer.SetFileName(file_name+'.vtu')
        
    writer.SetInputData(u)
    writer.Write()
write_vtk('0')
