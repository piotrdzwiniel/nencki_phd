"""
Script: CalculateFOV.py

Description:
------------
This script calculates the field of view angle θ in degrees based on a participant's
distance from the screen and the width or height of the screen. The calculation uses
the provided formula to determine the angle.
"""

import math


def calculate_theta(x, y):
  """
  Calculate the angle θ in degrees using the provided formula.

  Args:
      x (float): Participant's distance from the screen in mm.
      y (float): Width or height of the screen in mm.

  Returns:
      float: The calculated angle θ in degrees.
  """

  # Calculate the value of θ using the formula
  theta = 2 * math.atan(y / (2 * x)) * 180 / math.pi
  return theta


"""
LEDES, IMP and PACK procedural computer screen size:

* Height: 340 mm
* Width: 190 mm
* Participant distance from the screen: 800 mm
"""

x = 800  # Participant's distance from the screen in mm
y = [340, 190]  # Width and height of the screen in mm

result = [calculate_theta(x, y) for y in y]
print(f"θ = {result[0]:.2f}° / {result[1]:.2f}°")