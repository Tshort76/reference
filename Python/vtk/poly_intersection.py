#!/usr/bin/env python

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle  # DO not remove or UI is non-interactive

# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkCleanPolyData, vtkTriangleFilter
from vtkmodules.vtkFiltersGeneral import vtkBooleanOperationPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

ATRIA_VTK_FILE = "resources/CHU406original.Atria.vtk"


def main():
    colors = vtkNamedColors()

    operation = "intersection"
    reader = vtkUnstructuredGridReader()
    reader.SetFileName(ATRIA_VTK_FILE)
    geo_filter = vtkGeometryFilter()
    geo_filter.SetInputConnection(reader.GetOutputPort())
    geo_filter.Update()
    poly1 = geo_filter.GetOutput()

    tri1 = vtkTriangleFilter()
    tri1.SetInputData(poly1)
    clean1 = vtkCleanPolyData()
    clean1.SetInputConnection(tri1.GetOutputPort())
    clean1.Update()
    input1 = clean1.GetOutput()

    sphereSource1 = vtkSphereSource()
    sphereSource1.SetCenter(20.43808060942321, 18.333007878470767, 34.5753857481471)
    sphereSource1.SetRadius(0.5)
    # sphereSource1.SetPhiResolution(21)
    # sphereSource1.SetThetaResolution(21)
    sphereSource1.Update()
    input2 = sphereSource1.GetOutput()

    input1Mapper = vtkPolyDataMapper()
    input1Mapper.SetInputData(input1)
    input1Mapper.ScalarVisibilityOff()
    input1Actor = vtkActor()
    input1Actor.SetMapper(input1Mapper)
    input1Actor.GetProperty().SetDiffuseColor(colors.GetColor3d("Tomato"))
    input1Actor.GetProperty().SetSpecular(0.6)
    input1Actor.GetProperty().SetSpecularPower(20)
    # input1Actor.SetPosition(input1.GetBounds()[1] - input1.GetBounds()[0], 0, 0)

    input2Mapper = vtkPolyDataMapper()
    input2Mapper.SetInputData(input2)
    input2Mapper.ScalarVisibilityOff()
    input2Actor = vtkActor()
    input2Actor.SetMapper(input2Mapper)
    input2Actor.GetProperty().SetDiffuseColor(colors.GetColor3d("Mint"))
    input2Actor.GetProperty().SetSpecular(0.6)
    input2Actor.GetProperty().SetSpecularPower(20)
    # input2Actor.SetPosition(-(input1.GetBounds()[1] - input1.GetBounds()[0]), 0, 0)

    booleanOperation = vtkBooleanOperationPolyDataFilter()
    if operation.lower() == "union":
        booleanOperation.SetOperationToUnion()
    elif operation.lower() == "intersection":
        booleanOperation.SetOperationToIntersection()
    elif operation.lower() == "difference":
        booleanOperation.SetOperationToDifference()
    else:
        print("Unknown operation:", operation)
        return

    booleanOperation.SetInputData(0, input1)
    booleanOperation.SetInputData(1, input2)

    booleanOperationMapper = vtkPolyDataMapper()
    booleanOperationMapper.SetInputConnection(booleanOperation.GetOutputPort())
    booleanOperationMapper.ScalarVisibilityOff()

    booleanOperationActor = vtkActor()
    booleanOperationActor.SetMapper(booleanOperationMapper)
    booleanOperationActor.GetProperty().SetDiffuseColor(colors.GetColor3d("Banana"))
    booleanOperationActor.GetProperty().SetSpecular(0.6)
    booleanOperationActor.GetProperty().SetSpecularPower(20)

    renderer = vtkRenderer()
    renderer.AddViewProp(input1Actor)
    renderer.AddViewProp(input2Actor)
    renderer.AddViewProp(booleanOperationActor)
    renderer.SetBackground(colors.GetColor3d("Silver"))
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(640, 480)
    renderWindow.SetWindowName("BooleanOperationPolyDataFilter")

    viewUp = [0.0, 0.0, 1.0]
    position = [0.0, -1.0, 0.0]
    PositionCamera(renderer, viewUp, position)
    renderer.GetActiveCamera().Dolly(1.4)
    renderer.ResetCameraClippingRange()

    renWinInteractor = vtkRenderWindowInteractor()
    renWinInteractor.SetRenderWindow(renderWindow)

    renderWindow.Render()
    renWinInteractor.Start()


def PositionCamera(renderer, viewUp, position):
    renderer.GetActiveCamera().SetViewUp(viewUp)
    renderer.GetActiveCamera().SetPosition(position)
    renderer.ResetCamera()


if __name__ == "__main__":
    main()
