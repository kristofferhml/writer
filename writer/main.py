import rclpy
import os
import csv
from datetime import datetime
from rclpy.node import Node
from std_msgs.msg import Float32


METRICS_TOPIC = os.getenv('METRICS_TOPIC', 'ph')
FILE_NAME = os.getenv('FILE_NAME', 'tmp.csv')
FOLDER = os.getenv('FOLDER', '')

class Writer(Node):

    def __init__(self):
        super().__init__('writer')
        
        self.file = os.path.join(FOLDER, FILE_NAME)
        self.subscription = self.create_subscription(
            Float32,
            METRICS_TOPIC,
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        
    def listener_callback(self, msg):
        
        current_date = datetime.now()
        with open(self.file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([current_date.isoformat(),msg.data])
        
        self.get_logger().info('Appending: "%d"' % msg.data)
        
def main(args=None):
    rclpy.init(args=args)

    subscriber = Writer()

    rclpy.spin(subscriber)
    subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()