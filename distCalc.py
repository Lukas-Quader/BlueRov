from numpy import sin, cos, arccos, pi, round

def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees

def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians

def getDistanceBetweenPointsNew(latitude1, longitude1, latitude2, longitude2, unit = 'kilometers'):
    
    theta = longitude1 - longitude2
    
    distance = 60 * 1.1515 * rad2deg(
        arccos(
            (sin(deg2rad(latitude1)) * sin(deg2rad(latitude2))) + 
            (cos(deg2rad(latitude1)) * cos(deg2rad(latitude2)) * cos(deg2rad(theta)))
        )
    )
    
    if unit == 'miles':
        return round(distance, 5)
    if unit == 'kilometers':
        return round(distance * 1609.344, 3) 


def main(args=None):
    lat1 = 49.9917
    lat2 = 50.0049
    lon1 = 8.41321
    lon2 = 8.42182
    dist = getDistanceBetweenPointsNew(lat1, lon1, lat2, lon2)

    print(str(dist) + ' m')

if __name__ == '__main__':
    main()
