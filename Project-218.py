import glob
import os
import sys
import time
import random

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

actor_list = []


def car_control():
    dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.51))
    time.sleep(20)


try:
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    map = world.get_map()
    get_blueprint_of_world = world.get_blueprint_library()
    car_model = get_blueprint_of_world.filter('model3')[0]
    spawn_point = (world.get_map().get_spawn_points()[20])
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)

    walkers_blueprint = random.choice(get_blueprint_of_world.filter('walker'))
    walkers_spawn_point = world.get_map().get_spawn_points()[15]
    dropped_walker = world.spawn_actor(walkers_blueprint, walkers_spawn_point)

    control_walker = carla.WalkerControl()
    control_walker.speed = 0.9
    control_walker.y=1# set y axis with control_walker
    control_walker.x=-1# set x axis with control_walker
    control_walker.direction.z = 0
    control_walker.jump=True#set jump with control_walker
    dropped_walker.apply_control(control_walker)


    simulator_camera_location_rotation = carla.Transform(walkers_spawn_point.location, walkers_spawn_point.rotation)
    simulator_camera_location_rotation.location += spawn_point.get_forward_vector() * 30
    simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)
    actor_list.append(dropped_vehicle)

    car_control()

    time.sleep(1000)
finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')
