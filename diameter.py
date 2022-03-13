import math

def calculate_minimum_diameter(number, width , height, coord):

    minimum_distance = []
    final_points = []
    edges = width

    for i in range(number):
        # change initial x states (0 or width) 
        edges = width - edges
        # receives the coordinates of a particular fin 
        y_initial, x_final, y_final = coord[i]
        if i != 0:
            # adds the distance between the end point of a fin and the edge of the circuit 
            minimum_distance.append(abs(final_points[i-1][0]-edges))
            # calculates the slope of the current line
            mr = (y_final - y_initial) / (x_final - edges)
            # calculates the linear coefficient of the current line
            c_1 = mr * (-x_final) + (y_final)
            # calculates the slope of the perpendicular line with respect to the current line 
            ms = -1 / mr
            # calculates the linear coefficient of the perpendicular line with respect to the current line 
            c_2 = ms * (-final_points[i-1][0]) + (final_points[i-1][1]) # utiliza as coordendas do ponto final da aleta anterior
            # calculates the coordinates of the meeting point between the two lines 
            x = (c_1 - c_2) / (ms - mr)
            y = (ms * x) + c_2
            # checks whether the found point (x, y) touches the current straight line 
            if (not edges and x >= edges and x <= x_final) or (edges and x <= edges and x >= x_final):
                # add the distance from the ending point of the previous fin to the found point
                minimum_distance.append(math.sqrt((final_points[i-1][0]-x)**2+(final_points[i-1][1]-y)**2))
            else:
                # add the distance between the end point of the previous fin with the current fin 
                minimum_distance.append(math.sqrt((final_points[i-1][0]-x_final)**2+(final_points[i-1][1]-y_final)**2))

        # adiciona as coordendas do ponto final da aleta atual
        final_points.append([x_final, y_final])
    edges = width - edges
    # add the distance from the endpoint with the edge to the last fin 
    minimum_distance.append(abs(final_points[-1][0]-edges))
    # returns the shortest distance necessary for the ball to pass through the circuit 
    return min(minimum_distance)
