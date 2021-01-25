import math

def circumference(r):
    """Calculate the surface of a circle of radius r
    This does not compute the surface though :D"""
    return 2*math.pi*r

def area(r):
    """
    Function calculating area of circle of radius r
    """
    return math.pi*r**2

def area_triangle(base, height):
    """
    Calculate the area of a triangle.
    
    param "base": width of the triangle base
    param "height": height of the trianble
    """
    return base*height/2

def circumference_triangle(a, b, c):
    """
    Calculate the circumference of a triangle.
    
    param a: one side of the triangle
    param b: other side of the triangle
    param c: third side of the triangle
    return: circumference of the triangle
    """
    return a + b + c
    

print("Hello world")
