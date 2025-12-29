import gdsfactory as gf
import pandas as pd
import sys 


if len(sys.argv) > 1:
    input_file = str(sys.argv[1])
    print(f'Reading ' + input_file)
else:
    input_file = 'wheel_example.csv'
    print(f'Reading ' + input_file)

input = pd.read_csv(input_file, comment='#')

x = input['x']
y = input['y']
positions = [(xi, yi) for xi, yi in zip(x,y)]

# Create a new component
c = gf.Component()

# wheel drawing function
def wheel(chip: gf.Component, 
          pos: tuple, 
          linewidth: float, 
          diameter: float):
    """
    Draws a wheel in chip
        
    :param chip: gf.Component
    :param pos: Dict, (x,y) in micrometer
    :param linewidth: linewidth in micrometer
    :param diameter: inner diameter of the wheel in micrometer
    """
    elements = []
    
    circ_outer = gf.components.circle(radius=diameter / 2 + linewidth, angle_resolution=.5, layer=(1,0))
    circ_inner = gf.components.circle(radius=diameter / 2, angle_resolution=.5, layer=(1,0))

    ring = gf.boolean(A=circ_outer, B=circ_inner,
                      operation="not",
                      layer=(1,0))

    ring = chip << ring
    elements.append(ring)

    # arms
    for angle in [0,45,90,135]:
        arm = gf.components.rectangle(size=(diameter, linewidth), layer=(1,0))
        arm = chip << arm
        arm.move((-diameter/2, -linewidth / 2))
        arm.rotate(angle)
        elements.append(arm)


    for e in elements:
        e.move(pos)



for posi, li, di in zip(positions, input['linewidth'], input['diameter']):
    wheel(c, posi, li, di)


c.flatten()


c.write_gds(f"output.gds")
