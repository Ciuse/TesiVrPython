import json
from types import SimpleNamespace
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import random

data = []
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
j = 0
limits = []

def plot_linear_cube(x, y, z, dx, dy, dz, color='red'):

    global ax

    xx = [x, x, x+dx, x+dx, x]
    yy = [y, y+dy, y+dy, y, y]
    kwargs = {'alpha': 1, 'color': color}
    ax.plot3D(xx, yy, [z]*5, **kwargs)
    ax.plot3D(xx, yy, [z+dz]*5, **kwargs)
    ax.plot3D([x, x], [y, y], [z, z+dz], **kwargs)
    ax.plot3D([x, x], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y, y], [z, z+dz], **kwargs)
    plt.title('Cube')


def dataToNumpy(x, y, z, length, dims=2):
    """
    Create a line using a random walk algorithm

    length is the number of points for the line.
    dims is the number of dimensions the line has.
    """
    lineData2 = np.zeros((dims, length))

    lineData2[0, :] = x
    lineData2[1, :] = y
    lineData2[2, :] = z
    return lineData2


def update_lines(i, lines):
    global j, limits

    if(i>limits[j]):
        lines.append(ax.plot(data[j][0], data[j][1], data[j][2]))
        j = j + 1

    if j>0:
        currentValue = i - limits[j-1]
    else:
        currentValue = i

    lines[j][0].set_data(data[j][0, :currentValue], data[j][1, :currentValue])
    lines[j][0].set_3d_properties(data[j][2, :currentValue])

    return lines


def readJson():

    with open('C:/Users/Giuseppe/PycharmProjects/pythonProject/JsonFile3.json') as json_file:
        jsonFile = json.load(json_file, object_hook=lambda d: SimpleNamespace(**d))
    json_file.close()

    objectList = []
    tweezersErrors = []
    objectsErrors = []

    for objectKey in jsonFile.ListOfObject.__dict__:
        trajectoryList =[]
        tweezersErrors.append(jsonFile.ListOfObject.__dict__[objectKey].numberOfErrorPinza)
        objectsErrors.append(jsonFile.ListOfObject.__dict__[objectKey].numberOfErrorObject)

        for trajectory in jsonFile.ListOfObject.__dict__[objectKey].trajectoryList:
            positionList = []
            for position in trajectory.positionList:
                positionList.append([position.x, position.y, position.z])
            trajectoryList.append(positionList)
        objectList.append(trajectoryList)

    f = open("grafici/experimentData.txt", "w+")
    f.write(
        "average tweezers error: "+str(np.average(tweezersErrors))
        + "\n"
        + "average touching container error: "+ str(np.average(objectsErrors)))

    f.close()
    print(np.average(tweezersErrors))
    print(np.average(objectsErrors))

    i = 0
    for objectKey in jsonFile.ListOfObject.__dict__:
        calculateAndDrawTrajectoryOfAnObject(objectList[i], jsonFile.ListOfObject.__dict__[objectKey].idObject)
        i = i+1



def calculateAndDrawTrajectoryOfAnObject(obj, objId):
    print("entrato")
    objectChoosen = obj

    totalFrame = 0

    lines = []

    global ax, data, limits, j

    data = []
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    j = 0
    limits = []

    fig.add_axes(ax)

    for trajectory in objectChoosen:

        totalFrame= totalFrame + len(trajectory)

        xList = [x[0] for x in trajectory]
        yList = [x[2] for x in trajectory]
        zList = [x[1] for x in trajectory]


        data.append(dataToNumpy(xList, yList, zList, len(trajectory), 3))

    limitToAdd = 0

    maxX = data[0][0][0]
    minX = data[0][0][0]
    maxY = data[0][1][0]
    minY = data[0][1][0]
    maxZ = data[0][2][0]
    minZ = data[0][2][0]

    for trajectoryData in data:
        if(np.amax(trajectoryData[0]) > maxX):
            maxX = np.amax(trajectoryData[0])
        if (np.amax(trajectoryData[1]) > maxY):
            maxY = np.amax(trajectoryData[1])
        if (np.amax(trajectoryData[2]) > maxZ):
            maxZ = np.amax(trajectoryData[2])

        if(np.amin(trajectoryData[0]) < minX):
            minX = np.amin(trajectoryData[0])
        if (np.amin(trajectoryData[1]) < minY):
            minY = np.amin(trajectoryData[1])
        if (np.amin(trajectoryData[2]) < minZ):
            minZ = np.amin(trajectoryData[2])

        limitToAdd=limitToAdd + len(trajectoryData[0])
        limits.append(limitToAdd)


    lines.append(ax.plot(data[0][0], data[0][1], data[0][2]))
    # call the animator
    line_ani = animation.FuncAnimation(fig, update_lines, totalFrame, fargs=[lines],
                                       interval=100, blit=False)


    # Setting the axes properties
    ax.set_xlim3d([minX, maxX])
    ax.set_xlabel('X')
    ax.set_ylim3d([minY,maxY])
    ax.set_ylabel('Y')
    ax.set_zlim3d([minZ, maxZ])
    ax.set_zlabel('Z')
    ax.set_title('3D Test')

    for ax in plt.gcf().axes:
        for line in ax.get_lines():
            line.set_color((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))

    plot_linear_cube(-0.005, -0.005, -0.005, 0.01, 0.01, 0.01)


    plt.show()
    line_ani.save("grafici/test"+str(objId)+".gif", writer='pillow')



if __name__ == '__main__':
    readJson()

