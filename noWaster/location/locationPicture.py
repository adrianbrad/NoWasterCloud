
from motionless import DecoratedMap, LatLonMarker

def handlePictureUrl(url, newEncodedPolyline):
    return url.replace("sgl%7CGqaxnC_xA_%60H", newEncodedPolyline.replace("\\\\","\\"))

def pictureUrlForRoute(polyLine, markerList):
    road_styles = [{
        'feature': 'road.highway',
        'element': 'geomoetry',
        'rules': {
            'visibility': 'simplified',
            'color': '#c280e9'
        }
    }, {
        'feature': 'transit.line',
        'rules': {
            'visibility': 'simplified',
            'color': '#bababa'
        }
    }]
    dmap = DecoratedMap(style=road_styles)
    for index, point in enumerate(markerList):
        if(len(point) == 3):
            dmap.add_marker(LatLonMarker(point[0], point[1], size = "tiny", icon_url = "http:" + str(point[2])))
        else:
            if index == len(markerList) - 1:
                dmap.add_marker(LatLonMarker(point[0], point[1],label='B'))
            elif index == 0:
                dmap.add_marker(LatLonMarker(point[0], point[1],label='A'))
            else:
                dmap.add_marker(LatLonMarker(point[0], point[1], size = "small", label=str(index)))
    # dmap.add_marker(LatLonMarker(origin[0], origin[1],label='A'))
    # dmap.add_marker(LatLonMarker(destination[0], destination[1],label='B'))
    dmap.add_path_latlon(46.7623430,23.5575370)
    dmap.add_path_latlon(46.7765820,23.6037750)
    return handlePictureUrl(dmap.generate_url(), polyLine)