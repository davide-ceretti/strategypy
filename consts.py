CAPTION = "StrategyPY"
SCREEN_SIZE = (800, 600)
UNIT_SIZE = (10, 10)
GRID_SIZE = tuple(x/y for x, y in zip(SCREEN_SIZE, UNIT_SIZE))

GRID_COLOR = (50, 50, 50)

u_x, u_y = UNIT_SIZE
cell = lambda x, y: (u_x*x, u_y*y, u_x, u_y)
