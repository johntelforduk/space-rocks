# Functions for manipulating cartesian coordinates expressed as [x, y] lists.

import math


# Convert vertex with float co-oridinates into integer coordinates.
# Needed because some pygame functions need integer coords.
def integer_coord(vertex):
    int_x = round(vertex[0])
    int_y = round(vertex[1])
    return [int_x, int_y]


# Move, or slide, a coordincate in 2d space.
def translation(vertex, delta):
    [vertex_x, vertex_y] = vertex
    [delta_x, delta_y] = delta
    return [vertex_x + delta_x, vertex_y + delta_y]


# Move a coordinate closer / further from origin.
# If done for all vertices in a 2d shape, it has the effect of changing the size of the whole shape.
def scale(vertex, scale_factor):
    [vertex_x, vertex_y] = vertex
    return [vertex_x * scale_factor, vertex_y * scale_factor]


# Scale a vertex away from a point, which is other than the origin.
#
# Method has 3 steps,
# 1. Move the vertex so that centre of rotations is now the origin.
# 2. Scale away from the origin.
# 3. Do the opposite of move in Step 1.
def scale_from_a_point(vertex, point, scale_factor):
    [point_x, point_y] = point

    moved_vertex = translation(vertex, [-point_x, -point_y])                    # Step 1.
    scaled_vertex = scale(moved_vertex, scale_factor)                           # Step 2.
    re_moved_vertex = translation(scaled_vertex, point)                        # Step 3.

    return re_moved_vertex



# https://en.wikipedia.org/wiki/Rotation_of_axes#Derivation
def rotate_around_origin(vertex, rotation_degrees):
    [vertex_x, vertex_y] = vertex
    rotation_radians = math.radians(rotation_degrees)

    return[vertex_x * math.cos(rotation_radians) + vertex_y * math.sin(rotation_radians),
           - vertex_x * math.sin(rotation_radians) + vertex_y * math.cos(rotation_radians)
           ]

# Rotate a vertex around a point (pivot vertex), which is other than the origin.
#
# Method has 3 steps,
# 1. Move the vertex so that centre of rotations is now the origin.
# 2. Rotate around origin.
# 3. Do the opposite of move in Step 1.
def rotate_around_a_point(vertex, pivot, rotation_degrees):
    [pivot_x, pivot_y] = pivot

    moved_vertex = translation(vertex, [-pivot_x, -pivot_y])                    # Step 1.
    rotated_vertex = rotate_around_origin(moved_vertex, rotation_degrees)       # Step 2.
    re_moved_vertex = translation(rotated_vertex, pivot)                        # Step 3.

    return re_moved_vertex

# Refactored from,
# https://www.geeksforgeeks.org/check-whether-a-given-point-lies-inside-a-triangle-or-not/

# A utility function to calculate area
# of triangle formed by (x1, y1),
# (x2, y2) and (x3, y3)

# def area(x1, y1, x2, y2, x3, y3):
#     return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
#                 + x3 * (y1 - y2)) / 2.0)

def area_triangle(v1, v2, v3):
    # x1=v1[0]
    # y1=v1[1]
    # x2=v2[0]
    # y2=v2[1]
    # x3=v3[0]
    # y3=v3[1]
    return (abs((v1[0] * (v2[1] - v3[1]) + v2[0] * (v3[1] - v1[1])
                + v3[0] * (v1[1] - v2[1])) / 2.0))



# A function to check whether point P(x, y)
# lies inside the triangle formed by
# A(x1, y1), B(x2, y2) and C(x3, y3)


# def isInside(x1, y1, x2, y2, x3, y3, x, y):
#     # Calculate area of triangle ABC
#     A = area(x1, y1, x2, y2, x3, y3)
#
#     # Calculate area of triangle PBC
#     A1 = area(x, y, x2, y2, x3, y3)
#
#     # Calculate area of triangle PAC
#     A2 = area(x1, y1, x, y, x3, y3)
#
#     # Calculate area of triangle PAB
#     A3 = area(x1, y1, x2, y2, x, y)
#
#     # Check if sum of A1, A2 and A3
#     # is same as A
#     if (A == A1 + A2 + A3):
#         return True
#     else:
#         return False

# Is vertex v inside the triangle v1, v2, v3?
def is_inside_triangle(v, v1, v2, v3):
    # x=v[0]
    # y=v[1]
    # x1=v1[0]
    # y1=v1[1]
    # x2=v2[0]
    # y2=v2[1]
    # x3=v3[0]
    # y3=v3[1]

    # Calculate area of triangle ABC
    a = area_triangle(v1, v2, v3)

    # Calculate area of triangle PBC
    a1 = area_triangle(v, v2, v3)

    # Calculate area of triangle PAC
    a2 = area_triangle(v, v1, v3)

    # Calculate area of triangle PAB
    a3 = area_triangle(v, v1, v2)

    # If a == a1 + a2 + a3 then v is inside the triangle.
    # This test is done approximately due to float maths inaccuracies.
    if abs(a1 + a2 + a3 - a) < 1:
        return True
    else:
        return False
