import bpy

import math
import random
from pathlib import Path
import time

import numpy as np


# -----------------------------------------------------------------------------
# Geometry utilities
# -----------------------------------------------------------------------------

def spherical_to_cartesian(radius, theta, phi):
    """Convert spherical coordinates to Cartesian coordinates."""
    x = radius * math.sin(phi) * math.cos(theta)
    y = radius * math.sin(phi) * math.sin(theta)
    z = radius * math.cos(phi)
    return x, y, z


def rotation_matrix(v1, v2):
    """Compute the rotation matrix that rotates vector v1 to vector v2."""
    # Normalize input vectors to make the rotation independent of vector length.
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)

    # The rotation axis is perpendicular to both vectors.
    axis = np.cross(v1, v2)
    axis_norm = np.linalg.norm(axis)
    if axis_norm == 0:
        # The two vectors are parallel, so no rotation is required.
        return np.eye(3)

    axis = axis / axis_norm

    # Rotation angle between the two vectors.
    angle = np.arccos(np.dot(v1, v2))

    # Rodrigues' rotation formula.
    c = np.cos(angle)
    s = np.sin(angle)
    t = 1 - c

    x = axis[0]
    y = axis[1]
    z = axis[2]

    rotation_matrix = np.array([[t * x * x + c, t * x * y - z * s, t * x * z + y * s],
                                [t * x * y + z * s, t * y * y + c, t * y * z - x * s],
                                [t * x * z - y * s, t * y * z + x * s, t * z * z + c]])

    return rotation_matrix


def rotation_matrix_to_euler_angles(R):
    """Convert a rotation matrix to Euler angles in Blender's XYZ convention."""
    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6  # Numerical threshold for gimbal-lock-like cases.

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return x, y, z


# -----------------------------------------------------------------------------
# Blender object helpers
# -----------------------------------------------------------------------------

def get_obj_by_name(name, suffix=None):
    """Fetch a Blender object by its base name and an optional modality suffix."""
    full_name = name + suffix if suffix else name
    return bpy.data.objects[full_name]


# -----------------------------------------------------------------------------
# Random scene sampling
# -----------------------------------------------------------------------------

def random_earth():
    """Randomly rotate the Earth around its z-axis."""
    theta = random.uniform(0, 2 * math.pi)
    bpy.data.objects['Earth'].rotation_euler = (0.0, 0.0, theta)
    return math.degrees(theta)


def random_moon():
    """Randomly place and rotate the Moon on a sphere around the Earth."""
    radius = 63.78 + 3844.04  # Earth radius + average Earth-Moon distance, scaled by 1/100.
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0, math.pi)
    x, y, z = spherical_to_cartesian(radius, theta, phi)

    roll = random.uniform(0, 2 * math.pi)
    pitch = random.uniform(0, 2 * math.pi)
    yaw = random.uniform(0, 2 * math.pi)

    bpy.data.objects['Moon'].location = (x, y, z)
    bpy.data.objects['Moon'].rotation_euler = (roll, pitch, yaw)

    # Coordinates are converted back to kilometers for label files.
    return (x * 100.0, y * 100.0, z * 100.0), (math.degrees(roll), math.degrees(pitch), math.degrees(yaw))


def random_obj(obj_vi, obj_ir, obj_sg):
    """Randomly sample the target object's orbital position and 6D pose."""
    EARTH_RADIUS = 63.78  # Scaled Earth radius. Increase/decrease only if the scene scale changes.
    radius = random.uniform(EARTH_RADIUS + 2.00, EARTH_RADIUS + 100.00)  # Target altitude range: 200-10000 km.
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0, math.pi)
    x, y, z = spherical_to_cartesian(radius, theta, phi)

    roll = random.uniform(0, 2 * math.pi)
    pitch = random.uniform(0, 2 * math.pi)
    yaw = random.uniform(0, 2 * math.pi)

    # Keep the visible-light, infrared, and segmentation versions perfectly aligned.
    obj_vi.location, obj_vi.rotation_euler = (x, y, z), (roll, pitch, yaw)
    obj_ir.location, obj_ir.rotation_euler = (x, y, z), (roll, pitch, yaw)
    obj_sg.location, obj_sg.rotation_euler = (x, y, z), (roll, pitch, yaw)

    return ((x * 100.0, y * 100.0, z * 100.0), (math.degrees(roll), math.degrees(pitch), math.degrees(yaw)),
            (radius - EARTH_RADIUS) * 100.0)


def random_cam(cam_dist, obj_x, obj_y, obj_z):
    """Randomly place the camera around the object and point it toward the target."""
    # Label coordinates are stored in kilometers, while Blender scene coordinates are scaled by 1/100.
    obj_x /= 100.0
    obj_y /= 100.0
    obj_z /= 100.0

    radius = cam_dist  # Camera-target distance in Blender units; input cam_dists are divided by 10 in render().
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0, math.pi)
    x, y, z = spherical_to_cartesian(radius, theta, phi)

    # Align the camera's negative z-axis with the direction from the camera to the object.
    R = rotation_matrix(np.array([0, 0, -1]), np.array([-x, -y, -z]))
    x += obj_x
    y += obj_y
    z += obj_z

    roll, pitch, yaw = rotation_matrix_to_euler_angles(R)

    scale = cam_dist * 15.0  # View-direction jitter in degrees; larger values increase pose diversity.
    roll += random.uniform(-math.radians(scale), math.radians(scale))
    pitch += random.uniform(-math.radians(scale), math.radians(scale))
    yaw += random.uniform(-math.radians(scale), math.radians(scale))

    bpy.data.objects['Camera'].location, bpy.data.objects['Camera'].rotation_euler = (x, y, z), (roll, pitch, yaw)
    bpy.data.objects['Light'].location, bpy.data.objects['Light'].rotation_euler = (x, y, z), (roll, pitch, yaw)

    return math.degrees(roll), math.degrees(pitch), math.degrees(yaw)


# -----------------------------------------------------------------------------
# Rendering pipeline
# -----------------------------------------------------------------------------

def render_one_obj(objs_name, vi_dir, ir_dir, sg_dir, lb_dir, cam_dist, repeat, start):
    """Render visible-light, infrared, segmentation, and label files for one camera distance."""
    for i in range(repeat):
        # Randomly choose one target object for the current image.
        obj_earth = bpy.data.objects['Earth']
        obj_moon = bpy.data.objects['Moon']
        obj_name_render = random.choice(objs_name)
        obj_vi = get_obj_by_name(obj_name_render, '_vi')
        obj_ir = get_obj_by_name(obj_name_render, '_ir')
        obj_sg = get_obj_by_name(obj_name_render, '_sg')

        # Randomly sample Earth and Moon poses.
        earth_yaw = random_earth()
        (moon_x, moon_y, moon_z), (moon_roll, moon_pitch, moon_yaw) = random_moon()

        # Randomly sample the target object's 6D pose and the camera pose.
        (obj_x, obj_y, obj_z), (obj_roll, obj_pitch, obj_yaw), obj_height = random_obj(obj_vi, obj_ir, obj_sg)
        cam_roll, cam_pitch, cam_yaw = random_cam(cam_dist, obj_x, obj_y, obj_z)

        # Render the visible-light image.
        bpy.data.scenes["Scene"].view_layers["atmosphere"].use = False
        bpy.data.lights["Lamp"].energy = 4.5  # Main light intensity for visible-light rendering.
        bpy.data.lights["Lamp.001"].energy = 3 + cam_dist * 20.0  # Camera-side light; increase for brighter targets.
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.9  # Background brightness.
        obj_earth.hide_render = False
        obj_moon.hide_render = False
        obj_vi.hide_render = False
        obj_ir.hide_render = True
        obj_sg.hide_render = True
        bpy.ops.render.render()
        bpy.data.images["Render Result"].save_render(
            str(vi_dir / f"{obj_name_render}_camD{int(cam_dist * 10)}_{i + start}.png"))

        # Render the infrared image.
        bpy.data.scenes["Scene"].view_layers["atmosphere"].use = False
        bpy.data.lights["Lamp"].energy = 4.5  # Keep environmental illumination for infrared rendering.
        bpy.data.lights["Lamp.001"].energy = 0  # Disable camera-side light for infrared rendering.
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.9  # Infrared background brightness.
        obj_earth.hide_render = False
        obj_moon.hide_render = False
        obj_ir.hide_render = False
        obj_vi.hide_render = True
        obj_sg.hide_render = True
        bpy.ops.render.render()
        bpy.data.images["Render Result"].save_render(
            str(ir_dir / f"{obj_name_render}_camD{int(cam_dist * 10)}_{i + start}.png"))

        # Render the component segmentation label.
        bpy.data.scenes["Scene"].view_layers["atmosphere"].use = False
        bpy.data.lights["Lamp"].energy = 0  # Disable lighting to keep segmentation colors stable.
        bpy.data.lights["Lamp.001"].energy = 0  # Disable camera-side light for segmentation rendering.
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0  # Black background for labels.
        obj_earth.hide_render = True
        obj_moon.hide_render = True
        obj_sg.hide_render = False
        obj_vi.hide_render = True
        obj_ir.hide_render = True
        bpy.ops.render.render()
        bpy.data.images["Render Result"].save_render(
            str(sg_dir / f"{obj_name_render}_camD{int(cam_dist * 10)}_{i + start}.png"))

        # Save the metadata label file for the current rendered sample.
        with open(str(lb_dir / f"{obj_name_render}_camD{int(cam_dist * 10)}_{i + start}.txt"), 'w') as f:
            f.write(
                f"Object Name: {obj_name_render}\n")
            f.write(
                f"Earth Yaw(degree): {earth_yaw}\n")
            f.write(
                f"Moon Coordinate(km): ({moon_x}, {moon_y}, {moon_z})  "
                f"Moon Rotation(degree): ({moon_roll}, {moon_pitch}, {moon_yaw})\n")
            f.write(
                f"Orbital Altitude(km): {obj_height}\n")
            f.write(
                f"Object Coordinate(km): ({obj_x}, {obj_y}, {obj_z})  "
                f"Object Rotation(degree): ({obj_roll}, {obj_pitch}, {obj_yaw})\n")
            f.write(
                f"Camera Distance(m): {cam_dist * 10}  "
                f"Camera Rotation(degree): ({cam_roll}, {cam_pitch}, {cam_yaw})\n")


def render(root, objs_name, cam_dists, repeats, start=0):
    """Create the output folders and render samples for all camera distances."""
    root = Path(root)
    time_dir = Path(time.strftime('%Y-%m-%d %H-%M-%S', time.localtime()))
    bpy.context.scene.camera = bpy.data.objects['Camera']

    vi_dir = root / time_dir / "visible"
    vi_dir.mkdir(parents=True)
    ir_dir = root / time_dir / "infrared"
    ir_dir.mkdir(parents=True)
    sg_dir = root / time_dir / "segmentation"
    sg_dir.mkdir(parents=True)
    lb_dir = root / time_dir / "label"
    lb_dir.mkdir(parents=True)

    for cam_dist in cam_dists:
        cam_dist /= 10.0  # Input camera distance is stored in meters; Blender uses one tenth of this value.
        for repeat in repeats:
            render_one_obj(objs_name, vi_dir, ir_dir, sg_dir, lb_dir, cam_dist, repeat, start)


if __name__ == '__main__':
    render(root="E:/Task/Satellite Dataset/new_test1",  # Output root directory.
           objs_name=['AcrimSAT'],  # Object names to render; each object should have _vi, _ir, and _sg versions.
           cam_dists=[13, 15, 17, 19, 21, 23, 25, 27],  # Camera-target distances in meters.
           repeats=[10],  # Number of images rendered for each camera distance.
           start=0)  # Start index used in output filenames.
