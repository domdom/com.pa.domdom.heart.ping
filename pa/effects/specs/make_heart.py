
import utils
import math
import json
import copy

import colorsys

import random

from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')

#base ping object
base_ping = {
  "emitters": [
    {
      "spec": {
        "shader": "particle_transparent_nohdr",
        "facing": "EmitterZ",
        "alpha": [[0.066, 1 ], [0.2, 0.75 ], [0.8, 0.75 ], [1, 0 ] ],
        "size": [[0, 0 ], [0.0134, 0.67 ], [0.0266, 0.889 ], [0.04, 0.963 ], [0.0534, 0.98 ], [0.066, 1 ] ],
        "cameraPush": 0.1,
        "baseTexture": "/pa/effects/textures/particles/ping_ring.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "sizeX": 100,
      "offsetZ": 5,
      "rotationRate": 0.3927,
      "emissionBursts": 1,
      "maxParticles": 1,
      "lifetime": 6.0,
      "emitterLifetime": 0.1,
      "bLoop": False,
      "endDistance": -1,
      "useArmyColor": 1
    },
    {
      "spec": {
        "shader": "particle_transparent_screensize_nohdr",
        "size": [[0, 0 ], [0.1, 0.667 ], [0.2, 0.889 ], [0.3, 0.963 ], [0.4, 0.98 ], [0.5, 1 ] ],
        "alpha": [[0.3, 1 ], [0.5, 0.5 ], [0.7, 0.25 ], [1, 0 ] ],
        "cameraPush": 50,
        "polyAdjustCenter": 20,
        "baseTexture": "/pa/effects/textures/particles/softdot.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "sizeX": 100,
      "offsetZ": 25,
      "emissionBursts": 1,
      "maxParticles": 1,
      "lifetime": 1.0,
      "emitterLifetime": 0.1,
      "bLoop": False,
      "endDistance": -1,
      "useArmyColor": 1
    },
    {
      "spec": {
        "shader": "particle_transparent_nohdr",
        "facing": "EmitterZ",
        "size": [[0, 0 ], [0.1, 0.667 ], [0.2, 0.889 ], [0.3, 0.963 ], [0.4, 0.98 ], [0.5, 1 ] ],
        "red": 0.75,
        "green": 0.75,
        "blue": 0.75,
        "alpha": [[0, 0.5 ], [0.3, 0.25 ], [0.6, 0.125 ], [1, 0 ] ],
        "cameraPush": 0.5,
        "baseTexture": "/pa/effects/textures/particles/softdot.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "sizeX": 250,
      "offsetZ": 10,
      "emissionBursts": 1,
      "maxParticles": 1,
      "lifetime": 1.0,
      "emitterLifetime": 0.1,
      "bLoop": False,
      "endDistance": -1,
      "useArmyColor": 1
    }
  ]
}

base_beam = {
    "spec": {
        "shader": "particle_transparent",
        "shape": "beam",
        "sizeX": 1,
        "alpha": 1,
        "baseTexture": "/pa/effects/textures/particles/flat.papa"
    },
    "lifetime": 1,
    "emitterLifetime": 1,
    # "sizeX": [[0, 1],[1, 0]],
    "emissionBursts": 1,
    "bLoop": False,
    "endDistance": 3000
}

base_heart_particles = {
    "spec": {
        "shader": "particle_add",
        "sizeX": 0.6,
        "alpha": [[0, 1], [1, 0]],
        "dataChannelFormat": "PositionAndColor",
        "baseTexture": "/pa/effects/textures/particles/softdot.papa"
    },
    "lifetime": 0.2,
    "lifetimeRange": 0.1,
    "type": "EMITTER",
    "offsetRangeX" : 0.2,
    "offsetRangeY" : 0.2,
    "offsetRangeZ" : 0.2,
    "velocityRangeX": 1,
    "velocityRangeY": 1,
    "velocityRangeZ": 1,
    "velocity": 1, 
    "emissionRate": 20,
    "maxParticles": 40000,
    "emitterLifetime": 1,
    "endDistance": -1,
    "useWorldSpace": True,
    "bLoop": True
}

base_ring =     {
    "spec": {
        "shader": "particle_transparent_nohdr",
        "facing": "EmitterZ",
        "alpha": [[0.066, 1 ], [0.2, 0.75 ], [0.8, 0.75 ], [1, 0 ] ],
        "size": [[0, 0 ], [0.0134, 0.67 ], [0.0266, 0.889 ], [0.04, 0.963 ], [0.0534, 0.98 ], [0.066, 1 ] ],
        "cameraPush": 0.1,
        "baseTexture": "/pa/effects/textures/particles/ping_ring.papa",
        "dataChannelFormat": "PositionAndColor"
    },
    "sizeX": 100,
    "offsetZ": 5,
    "rotationRate": 0.3927,
    "emissionBursts": 1,
    "maxParticles": 1,
    "lifetime": 6.0,
    "emitterLifetime": 0.1,
    "bLoop": False,
    "endDistance": -1
}


def rainbow(n, offset=0, scale=1, revs=1, time=1):

    r = []
    g = []
    b = []

    for i in xrange(n + 1):
        t = offset + (float(i) / n) * revs

        rgb = colorsys.hsv_to_rgb(t % 1, 1, 1)

        r.append([float(i) / n * time, scale * rgb[0]])
        g.append([float(i) / n * time, scale * rgb[1]])
        b.append([float(i) / n * time, scale * rgb[2]])

    return (r, g, b)

def compute_u_a(s, t):
    u = 2.0 * s / t
    a = - float(u) / t * 1.2
    

    return (u, a)

def make_ping():
    # get base ping file
    base_ping # welp just defined it as a literal

    # delay for this animation
    delay = 1.0

    # number of co-centric hearts
    num_layers = 4

    # size of inner heart
    inner_size = 3.0
    outer_size = 10.0

    # each heart will rotate 
    num_rots = 1.0
    num_rot_frames = int(num_rots * 15)
    # rotation time in seconds
    rot_time = 5.0

    heart_height = 50.0
    ds = 1.1

    brightness_scale = 40

    # ring vars
    num_rings = 5

    # make the rings
    for i in xrange(num_rings):
        size = 80.0 - 15 * i
        height = 8.5 + i * 3.5
        rot_rate = -0.05 * i

        ring = copy.deepcopy(base_ring)

        ring['rotationRate'] = rot_rate
        ring['offsetZ'] = height
        ring['sizeX'] = size

        ring['spec']['red'], ring['spec']['green'], ring['spec']['blue'] = rainbow(10, float(i) / num_rings, 2, 1, 1)


        base_ping['emitters'].append(ring)



    for i in xrange(num_layers):

        # create size
        size_diff = (outer_size - inner_size) / num_layers
        size = inner_size + size_diff * (num_layers - i)
        
        # make heart shape
        r, z, points = make_heart(size, ds)

        j = 1

        shape_emitter = copy.deepcopy(base_beam)

        shape_emitter['maxParticles'] = points
        # rotate heart shape
        x1 = [[a[0], a[1] * math.cos(math.pi * 2 * j / float(num_rot_frames))] for a in r]
        y1 = [[a[0], a[1] * math.sin(math.pi * 2 * j / float(num_rot_frames))] for a in r]
        # vertically displace heart shape
        z1 = [[a[0], a[1] + heart_height - size_diff / 2 * i] for a in z]

        
        shape_emitter['delay'] = float(i) * rot_time / 30

        shape_emitter['offsetX'] = []
        shape_emitter['offsetY'] = []
        shape_emitter['offsetZ'] = 0

        shape_emitter['velocity'] = []
        shape_emitter['velocityX'] = []
        shape_emitter['velocityY'] = []
        shape_emitter['velocityZ'] = []

        for k in xrange(points):
            x = math.sin(float(random.randint(0, points-1)) / points * 2 * math.pi) * outer_size * 4 * random.random()
            y = math.cos(float(random.randint(0, points-1)) / points * 2 * math.pi) * outer_size * 4 * random.random()
            z = 0
            
            shape_emitter['velocityX'].append([z1[k][0], (x1[k][1] - x) / delay])
            shape_emitter['velocityY'].append([z1[k][0], (y1[k][1] - y) / delay])
            shape_emitter['velocityZ'].append([z1[k][0], (z1[k][1] - z) / delay])

            shape_emitter['offsetX'].append([z1[k][0], x])
            shape_emitter['offsetY'].append([z1[k][0], y])

            shape_emitter['velocity'].append([z1[k][0], math.sqrt(shape_emitter['velocityX'][-1][1] ** 2 + shape_emitter['velocityY'][-1][1] ** 2 + shape_emitter['velocityZ'][-1][1] ** 2)])


        shape_emitter['spec']['alpha'] = 0

        # add this emitter shape to the emitter
        base_ping['emitters'].append(shape_emitter)

        # get index of shape emitter
        idx = len(base_ping['emitters']) - 1

        # visible rainbow particles
        rgb = colorsys.hsv_to_rgb(float(i) / num_layers, 1, 1)
        particles = copy.deepcopy(base_heart_particles)

        particles['red'], particles['green'], particles['blue'] = rainbow(20, float(i) / num_layers + float(j) / num_rot_frames, brightness_scale, 1, 1)
        particles['spec']['alpha'] = [[0, 0], [0.3, 1]]
        # particles['spec']['red'], particles['spec']['green'], particles['spec']['blue'] = rainbow(20, float(i) / num_layers, brightness_scale, 1, 1)

        particles['linkIndex'] = idx
        base_ping['emitters'].append(particles)



    for i in xrange(num_layers):
        idelay = delay + i * rot_time / 30

        # create size
        size_diff = (outer_size - inner_size) / num_layers
        size = inner_size + size_diff * (num_layers - i)
        
        # make heart shape
        r, z, points = make_heart(size, ds)

        for j in xrange(num_rot_frames):
            shape_emitter = copy.deepcopy(base_beam)

            shape_emitter['maxParticles'] = points
            # rotate heart shape
            x1 = [[a[0], a[1] * math.cos(math.pi * 2 * j / float(num_rot_frames))] for a in r]
            y1 = [[a[0], a[1] * math.sin(math.pi * 2 * j / float(num_rot_frames))] for a in r]
            # vertically displace heart shape
            z1 = [[a[0], a[1] + heart_height - size_diff / 2 * i] for a in z]

            # compute the next step for transitioning
            x2 = [[a[0], a[1] * math.cos(math.pi * 2 * (j + 1) / float(num_rot_frames))] for a in r]
            y2 = [[a[0], a[1] * math.sin(math.pi * 2 * (j + 1) / float(num_rot_frames))] for a in r]

            shape_emitter['offsetX'] = x1
            shape_emitter['offsetY'] = y1
            shape_emitter['offsetZ'] = z1

            # make time velocity curve
            v = [0] * len(x2)

            for k in xrange(len(x2)):
                x2[k][1] = x2[k][1] - x1[k][1]
                y2[k][1] = y2[k][1] - y1[k][1]
                v[k] = [x2[k][0], math.sqrt(x2[k][1] * x2[k][1] + y2[k][1] * y2[k][1]) / (rot_time / num_rot_frames)]

            shape_emitter['velocityX'] = x2
            shape_emitter['velocityY'] = y2
            shape_emitter['velocity'] = v

            shape_emitter['spec']['alpha'] = 0
            # shape_emitter['red'], shape_emitter['green'], shape_emitter['blue'] = rainbow(20, float(i) / num_layers, brightness_scale, 1, 1)
            # shape_emitter['spec']['red'], shape_emitter['spec']['green'], shape_emitter['spec']['blue'] = rainbow(20, float(j) / num_rot_frames, 1, 1 / float(num_rot_frames) / 3, 1)

            shape_emitter['delay'] = idelay + (float(j) / num_rot_frames) * rot_time

            shape_emitter['lifetime'] = rot_time / num_rot_frames
            shape_emitter['emitterLifetime'] = rot_time / num_rot_frames

            # add this emitter shape to the emitter
            base_ping['emitters'].append(shape_emitter)

            # get index of shape emitter
            idx = len(base_ping['emitters']) - 1

            # visible rainbow particles
            rgb = colorsys.hsv_to_rgb(float(i) / num_layers, 1, 1)

            particles = copy.deepcopy(base_heart_particles)

            particles['red'], particles['green'], particles['blue'] = rainbow(20, float(i) / num_layers + float(j) / num_rot_frames, brightness_scale, 1, 1)
            # particles['spec']['red'], particles['spec']['green'], particles['spec']['blue'] = rainbow(20, float(i) / num_layers, brightness_scale, 1, 1)

            particles['linkIndex'] = idx

            base_ping['emitters'].append(particles)


def make_heart(radius, ds):
    b = radius
    a = b * 0.97

    t = 0

    # First we must compute the angles of the round bits on the heart
    y0 = math.sqrt(b**2 - (- a)**2)
    x0 = -a
    y1 = math.sin(-math.pi / 4) * b
    x1 = math.cos(-math.pi / 4) * b

    # start and end angle
    a0 = math.atan2(y1, x1)
    a1 = math.atan2(y0, x0)
    a3 = math.atan2(y0, -x0)

    # get angle in radians
    angle = a1 - a0
    
    s = angle * b * 2 + (a + 2 * b * math.sin(math.pi / 4)) * math.sqrt(2) * 2

    x = []
    y = []

    t = 0
    # bottom right straight part
    y.append([t, -(a + 2 * b * math.sin(math.pi / 4))])
    x.append([t, 0])
    t = (a + 2 * b * math.sin(math.pi / 4)) * math.sqrt(2) / s
    
    # right curvy bit
    num_points = int(math.floor(float(angle * b) / ds))
    for i in xrange(num_points):
        ang = float(i) / num_points * angle + a0
        vx = b * math.cos(ang) + a
        vy = b * math.sin(ang)
        x.append([b * (ang - a0)/ s + t, vx])
        y.append([b * (ang - a0)/ s + t, vy])

    # we are half way now
    t = 0.5
    # add middle concave point
    x.append([t, 0])
    y.append([t, y0])
    # left curvy bit
    for i in xrange(num_points):
        ang = float(i) / num_points * angle + a3
        vx = b * math.cos(ang) - a
        vy = b * math.sin(ang)
        x.append([b * (ang - a3)/ s + t, vx])
        y.append([b * (ang - a3)/ s + t, vy])

    # bottom left straight part
    y.append([1, -(a + 2 * b * math.sin(math.pi / 4))])
    x.append([1, 0])
     
    return (x, y, len(x))


make_ping()
utils.save_local_json(base_ping, 'ping.pfx')