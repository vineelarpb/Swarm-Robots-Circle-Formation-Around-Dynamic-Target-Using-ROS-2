import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

def algoReynolds(uav_positions, target_pos, threshold, max_speed=0.1):
    for i in range(len(uav_positions)):
        direction = target_pos - uav_positions[i]
        distance = np.linalg.norm(direction)
        if distance < threshold:
            uav_positions[i] -= max_speed * direction / distance
        else:
            uav_positions[i] += max_speed * direction / distance
    return uav_positions

def update_target_position(target_pos, max_speed=0.1):
    target_pos += np.random.uniform(-max_speed, max_speed, size=2)
    return target_pos

def main():
    num_steps = 100
    num_uavs = 100
    threshold = 2.0
    max_speed = 0.1

    target_pos = np.array([5.0, 5.0])
    initial_uav_positions = np.random.rand(num_uavs, 2) * 10

    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_title('UAVs Forming Circle Around Dynamic Target')

    target = ax.plot(target_pos[0], target_pos[1], 'ro', label='Dynamic Target')[0]
    uavs = ax.scatter(initial_uav_positions[:, 0], initial_uav_positions[:, 1], label='UAVs')

    def update(frame):
        nonlocal initial_uav_positions, target_pos
        target_pos = update_target_position(target_pos)
        initial_uav_positions = algoReynolds(initial_uav_positions, target_pos, threshold, max_speed)
        print("Initial UAV Positions:", initial_uav_positions)
        print("Target Position:", target_pos, "\n")
        target.set_data(target_pos[0], target_pos[1])
        uavs.set_offsets(initial_uav_positions)
        return target, uavs

    ani = FuncAnimation(fig, update, frames=num_steps, blit=True)

    pause_ax = plt.axes([0.81, 0.05, 0.1, 0.05])
    play_ax = plt.axes([0.91, 0.05, 0.05, 0.05])
    pause_button = Button(pause_ax, 'Pause', color='lightgrey', hovercolor='lightblue')
    play_button = Button(play_ax, 'Play', color='lightgrey', hovercolor='lightblue')

    def pause_animation(event):
        ani.event_source.stop()

    def play_animation(event):
        ani.event_source.start()

    pause_button.on_clicked(pause_animation)
    play_button.on_clicked(play_animation)

    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()


