import math

def circle_area(radius):
    return math.pi * radius ** 2

def cube_volume(side):
    return side ** 3

radius = float(input("Enter the radius of the circle: "))
print(f"The area of the circle is: {circle_area(radius):.2f}")

side = float(input("Enter the side length of the cube: "))
print(f"The volume of the cube is: {cube_volume(side):.2f}")