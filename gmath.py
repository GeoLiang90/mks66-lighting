import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)
#Indices
AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
    #Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    nhat = normal[:]
    vhat = view[:]
    lhat = [light[LOCATION][:],light[COLOR]]
    normalize(lhat[LOCATION])
    normalize(vhat)
    normalize(nhat)
    ambience = calculate_ambient(ambient,areflect)
    diffuse = calculate_diffuse(lhat,dreflect,nhat)
    specular = calculate_specular(lhat,sreflect,vhat,nhat)
    limit_color(ambience)
    limit_color(diffuse)
    limit_color(specular)
    result = []
    for x in range(3):
        result.append(int(ambience[x]) + int(diffuse[x]) + int(specular[x]))
    limit_color(result)
    return result

def calculate_ambient(alight, areflect):
    result = []
    for x in range(3):
        result.append(alight[x] * areflect[x])
    return result

def calculate_diffuse(light, dreflect, normal):
    result = []
    for x in range(3):
        result.append(light[COLOR][x] * dreflect[x] * (dot_product(normal,light[LOCATION])))
    return result

def calculate_specular(light, sreflect, view, normal):
    eq0 = dot_product(normal,light[LOCATION])
    combo = []
    for val in range(3):
        combo.append((2 * eq0 * (normal[val] - light[LOCATION][val])))
    dotCombo = dot_product(combo,view)
    dotCombo = dotCombo ** SPECULAR_EXP
    finResult = []
    for y in range(3):
        finResult.append(dotCombo * (light[COLOR][y] * sreflect[y]))
    return finResult

def limit_color(color):
    for x in range(3):
        if color[x] < 0:
            color[x] = 0
        elif color[x] > 255:
            color[x] = 255
        color[x] = int(color[x])

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
