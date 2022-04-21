#!/usr/bin/env python

import rospy
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation


from datetime import datetime
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan, JointState, Imu
from tf.transformations import euler_from_quaternion


class DataPlotter:
    def __init__(self):

        # Times used to integrate velocity to pose
        self.current_time = 0.0
        self.last_time = 0.0

        self.robot_pos = np.zeros(3)
        self.robot_angles_imu = np.zeros(3)
        self.robot_angles_odom = np.zeros(3)

        self.laser = {'ranges': np.array([]), 'angles': [], 'angle_min': 0.0, 'angle_max': 0.0, 'angle_increment': 0.0}
        self.instant_laser_data = [[], []]

        self.distance = 0.0
        rospy.init_node('distance_measurer', anonymous=True)

        # Motor velocities
        self.motor_velocity = np.zeros(6)

        # Subscribed topics
        rospy.Subscriber("/scan", LaserScan, self.callback_laser)
        rospy.Subscriber("/odom", Odometry, self.callback_odometry)
        rospy.Subscriber("/imu/data", Imu, self.callback_imu)

        self.started_laser = False
        self.started_odom = False
        self.started_imu = False

        self.dist_hist = [[], []]
        self.laser_hist = [[], []]

        self.figure = plt.figure(figsize=(12, 12))

    def callback_laser(self, data):
        """
        Callback routine to get the data from the laser sensor
        Args:
            data: laser data
        """
        self.laser['ranges'] = np.array(data.ranges)
        self.laser['angle_min'] = data.angle_min
        self.laser['angle_max'] = data.angle_max
        self.laser['angle_increment'] = data.angle_increment

        number_of_beams = int((self.laser['angle_max'] - self.laser['angle_min']) / self.laser['angle_increment'])

        angle = self.laser['angle_min']
        self.laser['angles'] = []
        for i in range(number_of_beams):
            self.laser['angles'].append(angle)
            angle += self.laser['angle_increment']
        self.laser['angles'] = np.array(self.laser['angles'])
        self.instant_laser_data = [[], []]

        if self.started_imu:
            for i in range(self.laser['angles'].shape[0]):
                x = self.robot_pos[0] + self.laser['ranges'][i] * np.cos(self.laser['angles'][i] + self.robot_angles_odom[-1])
                y = self.robot_pos[1] + self.laser['ranges'][i] * np.sin(self.laser['angles'][i] + self.robot_angles_odom[-1])

                if np.abs(x) == float('inf') or np.abs(y) == float('inf'):
                    continue

                self.laser_hist[0].append(x)
                self.laser_hist[1].append(y)
                self.instant_laser_data[0].append(x)
                self.instant_laser_data[1].append(y)

                if len(self.laser_hist[0]) > 1e4:
                    self.laser_hist[0].pop(0)
                    self.laser_hist[1].pop(0)
        self.started_laser = True

    def callback_odometry(self, data):
        """
        Callback routine to get the robot odometry data
        Args:
            data: odometry data
        """
        self.robot_pos[0] = data.pose.pose.position.x
        self.robot_pos[1] = data.pose.pose.position.y
        self.robot_pos[2] = data.pose.pose.position.z

        quat = np.zeros(4)
        quat[0] = data.pose.pose.orientation.x
        quat[1] = data.pose.pose.orientation.y
        quat[2] = data.pose.pose.orientation.z
        quat[3] = data.pose.pose.orientation.w

        self.robot_angles_odom = euler_from_quaternion(quat)

        self.dist_hist[0].append(self.robot_pos[0])
        self.dist_hist[1].append(self.robot_pos[1])

        self.started_odom = True

    def callback_imu(self, data):
        """
        Callback routine to get the data from the imu sensor
        Args:
            data: imu data
        """
        quat = np.zeros(4)
        quat[0] = data.orientation.x
        quat[1] = data.orientation.y
        quat[2] = data.orientation.z
        quat[3] = data.orientation.w

        self.robot_angles_imu = euler_from_quaternion(quat)

        self.started_imu = True

    def update(self, num):
        """
        Method that updates the plot
        """
        plt.clf()

        plt.plot(self.dist_hist[0], self.dist_hist[1], label='Path')
        plt.quiver(self.dist_hist[0][-1], self.dist_hist[1][-1],
                   np.cos(self.robot_angles_odom[-1]), np.sin(self.robot_angles_odom[-1]),
                   color='g', label='Robot', scale=50)
        try:
            plt.scatter(self.instant_laser_data[0], self.instant_laser_data[1], label='Laser', s=0.05, color='r')
        except ValueError:
            print(len(self.instant_laser_data[0]), len(self.instant_laser_data[1]))

        plt.xlim([-45, 18])
        plt.ylim([-60, 15])

        plt.xlabel('$x$')
        plt.ylabel('$y$')
        plt.title('Robot Path')

        plt.legend()
        plt.gca().set_aspect('equal', adjustable='box')
        return


if __name__ == '__main__':
    save_animation = False
    try:
        service = DataPlotter()
        print(f"Laser data ready: {service.started_laser}\n"
              f"Odometry data ready: {service.started_odom}\n"
              f"IMU data ready: {service.started_imu}")

        while not service.started_laser or not service.started_odom or not service.started_imu:
            continue

        if save_animation:
            service.animation = FuncAnimation(service.figure, service.update, interval=50, save_count=4000)
            f = "follow_wall_19_04.mp4"
            write_mp4 = animation.FFMpegWriter(fps=25)
            service.animation.save(f, writer=write_mp4)
        else:
            service.animation = FuncAnimation(service.figure, service.update, interval=50)
        plt.show()

    except rospy.ROSInterruptException:
        pass
