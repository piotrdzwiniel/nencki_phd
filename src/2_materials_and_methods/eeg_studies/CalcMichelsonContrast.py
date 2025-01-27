"""
Script: CalcMichelsonContrast.py

Description:
------------
This script calculates the Michelson contrast, which is a measure of the contrast between the
maximum and minimum luminance values in a visual pattern. The contrast is expressed as a
percentage.
"""

def michelson_contrast(Lmax, Lmin):
   """
   Calculate Michelson contrast in percent.

   Args:
       Lmax (float): Maximum luminance in cd/m^2.
       Lmin (float): Minimum luminance in cd/m^2.

   Returns:
       float: Michelson contrast expressed in percent.
   """
   Cm = ((Lmax - Lmin) / (Lmax + Lmin)) * 100
   return Cm

"""
IMP and PACK studies luminance values:

* Dark fields: 17.5 cd/m^2
* Bright fields: 100.4 cd/m^2
* Fixation point: 207.5 cd/m^2
"""

# Example usage:
Lmax = 100.4  # Maximum luminance in cd/m^2
Lmin = 17.5  # Minimum luminance in cd/m^2

contrast_percentage = michelson_contrast(Lmax, Lmin)
print(f"Michelson contrast: {contrast_percentage:.2f}%")