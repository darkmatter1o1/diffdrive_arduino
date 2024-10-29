import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import serial

class ImuPublisher(Node):

    def __init__(self):
        super().__init__('imu_publisher')
        self.publisher_ = self.create_publisher(Imu, 'imu/data', 10)
        self.serial_port = serial.Serial('/dev/ttyUSB0', 115200) # Adjust to your serial port

        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        line = self.serial_port.readline().decode('utf-8').strip()
        data = line.split(',')
        if len(data) != 6:
            return

        imu_msg = Imu()
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = 'base_link'
        
        # Convert string data to float and populate IMU message
        imu_msg.linear_acceleration.x = float(data[0])
        imu_msg.linear_acceleration.y = float(data[1])
        imu_msg.linear_acceleration.z = float(data[2])
        imu_msg.angular_velocity.x = float(data[3])
        imu_msg.angular_velocity.y = float(data[4])
        imu_msg.angular_velocity.z = float(data[5])

        self.publisher_.publish(imu_msg)

def main(args=None):
    rclpy.init(args=args)
    imu_publisher = ImuPublisher()
    rclpy.spin(imu_publisher)

    imu_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

