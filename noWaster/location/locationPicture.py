
from motionless import DecoratedMap, AddressMarker

def handlePictureUrl(url, newEncodedPolyline):
    return url.replace("sgl%7CGqaxnC_xA_%60H", newEncodedPolyline.replace("\\\\","\\"))

def pictureUrlForRoute(origin, destination, polyLine):
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
    dmap.add_marker(AddressMarker(origin,label='A'))
    dmap.add_marker(AddressMarker(destination,label='B'))
    dmap.add_path_latlon(46.7623430,23.5575370)
    dmap.add_path_latlon(46.7765820,23.6037750)
    return handlePictureUrl(dmap.generate_url(), polyLine)