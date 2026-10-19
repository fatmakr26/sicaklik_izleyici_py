import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class IzleyiciNode(Node):
    def __init__(self):
        super().__init__('izleyici_node')
        # Bonus: Eşik değerini parametre olarak tanımlama
        self.declare_parameter('esik_degeri', 30.0)
        self.subscription = self.create_subscription(
            Float32,
            '/sicaklik',
            self.listener_callback,
            10
        )
        self.get_logger().info('İzleyici düğümü başlatıldı.')

    def listener_callback(self, msg):
        esik = self.get_parameter('esik_degeri').get_parameter_value().double_value
        sicaklik = msg.data

        if sicaklik > esik:
            self.get_logger().warn(f'UYARI: Yüksek Sıcaklık! Değer: {sicaklik:.2f} °C (Eşik: {esik:.1f} °C)')
        else:
            self.get_logger().info(f'Sıcaklık Normal: {sicaklik:.2f} °C')

def main(args=None):
    rclpy.init(args=args)
    node = IzleyiciNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

