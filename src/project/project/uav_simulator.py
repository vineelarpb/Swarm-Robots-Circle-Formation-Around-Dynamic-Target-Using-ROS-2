import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from std_msgs.msg import Float64MultiArray
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ROS Node for publishing UAV and target positions
class UAVSimulator(Node):
    def __init__(self):
        super().__init__('uav_simulator')
        self.uav_pub = self.create_publisher(Float64MultiArray, 'uav_positions', 10)
        self.target_pub = self.create_publisher(Point, 'target_position', 10)
        self.timer = self.create_timer(0.1, self.publish_positions)

    # Function to publish UAV and target positions
    def publish_positions(self):
        msg = Float64MultiArray()
        # msg.data = uav_positions.flatten()
        msg.data = uav_positions.flatten().tolist()

        self.uav_pub.publish(msg)

        target_msg = Point()
        target_msg.x, target_msg.y = target_pos
        self.target_pub.publish(target_msg)

# Function to simulate UAV movement to surround the target
def surround_target(target_pos, uav_positions, radius=2.0, max_speed=0.1):
    num_uavs = len(uav_positions)
    for i in range(num_uavs):
        direction = target_pos - uav_positions[i]
        distance = np.linalg.norm(direction)
        if distance > radius:  # UAV is outside the desired radius
            direction /= distance  # Normalize direction vector
            uav_positions[i] += direction * max_speed  # Move UAV towards target
    return uav_positions

# Function to update the animation
def update(frame):
    global target_pos, uav_positions
    target_pos = np.random.rand(2) * 10  # Random target position
    uav_positions = surround_target(target_pos, uav_positions)
    scat.set_offsets(uav_positions)
    scat_target.set_offsets(target_pos)
    return scat, scat_target

# Simulation parameters
num_uavs = 10
radius = 2.0
max_speed = 0.1

# Initial UAV positions
uav_positions = np.random.rand(num_uavs, 2) * 10  # Random initial positions
target_pos = np.random.rand(2) * 10  # Random initial target position

# Create the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Create the scatter plot for UAVs and target
scat = ax.scatter(uav_positions[:, 0], uav_positions[:, 1], label='UAVs')
scat_target = ax.scatter(target_pos[0], target_pos[1], color='red', label='Target')

# ROS initialization
rclpy.init()
node = UAVSimulator()

# Animation
ani = FuncAnimation(fig, update, frames=100, interval=100, blit=True)

# Show the plot
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('UAVs Surrounding Target')
plt.legend()
plt.grid(True)
plt.axis('equal')

# ROS Spin
rclpy.spin(node)

# Clean up
node.destroy_node()
rclpy.shutdown()
