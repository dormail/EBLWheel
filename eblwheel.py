import gdsfactory as gf
import pandas as pd

input = pd.read_csv('wheel_example.csv', comment='#')

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



# Add a rectangle
# r = gf.components.rectangle(size=(10, 10), layer=(1, 0))
# rect = c.add_ref(r)

# # 
# wheel(c, (1e-2,1e-2), 1e-6, 100e-6,)
for posi, li, di in zip(positions, input['linewidth'], input['diameter']):
    wheel(c, posi, li, di)

# wheel(c, (1,1), 50e-3, 2)
# wheel(c, (-1,-1), 80e-3, 2)

# circ = gf.components.circle(radius=1e-2 / 2, angle_resolution=2.5, layer=(1,0))
# circ = c << circ

# wheel(c, (-1e-2,-1e-2), 1e-6, 1e-5)
# Add text elements
# t1 = gf.components.text("Hello", size=10, layer=(2, 0))
# t2 = gf.components.text("world", size=10, layer=(2, 0))

# text1 = c.add_ref(t1)
# text2 = c.add_ref(t2)

# # Position elements
# text1.xmin = rect.xmax + 5
# text2.xmin = text1.xmax + 2
# text2.rotate(30)

# Show the result
# c.show()
c.flatten()


c.write_gds(f"output.gds")



