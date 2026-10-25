import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen
import math

# Betuk definialasa 0..1-es koordinatarendszerben
FONT = {
    'R': [((0, 0), (0, 1)), ((0, 1), (0.7, 1)), ((0.7, 1), (0.7, 0.5)), ((0.7, 0.5), (0, 0.5)), ((0, 0.5), (0.7, 0))],
    'O': [((0, 0), (0, 1)), ((0, 1), (0.7, 1)), ((0.7, 1), (0.7, 0)), ((0.7, 0), (0, 0))],
    'S': [((0.7, 1), (0, 1)), ((0, 1), (0.5, 0.5)), ((0.5, 0.5), (0.7, 0.5)), ((0.7, 0.5), (0.7, 0)), ((0.7, 0), (0, 0))],
    '2': [((0, 0.8), (0.2, 1)), ((0.2, 1), (0.7, 1)), ((0.7, 1), (0.7, 0.6)), ((0.7, 0.6), (0, 0)), ((0, 0), (0.7, 0))],
    'Z': [((0, 1), (0.7, 1)), ((0.7, 1), (0, 0)), ((0, 0), (0.7, 0))],
}

# Szinek betunkent (RGB): Piros, Zold, Narancs, Cian
COLORS = [
    (255, 60, 60),    # R - Piros
    (60, 220, 60),    # O - Zold
    (255, 160, 30),   # S - Narancs
    (50, 200, 255),   # 2 - Cian
]

class TextDrawerNode(Node):
    def __init__(self):
        super().__init__('text_drawer_node')

        self.declare_parameter('text_to_draw', 'ROS 2')
        self.declare_parameter('scale', 1.5)

        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.set_pen_cli = self.create_client(SetPen, '/turtle1/set_pen')

        self.current_pose = None
        self.commands = []
        self.cmd_index = 0
        self.initialized = False
        self.last_pen_state = None

        self.timer = self.create_timer(1.0 / 30.0, self.control_loop)
        self.get_logger().info('Turtlesim Text Drawer Node futasra kesz.')

    def pose_callback(self, msg: Pose):
        self.current_pose = msg

    def build_path(self):
        text = self.get_parameter('text_to_draw').get_parameter_value().string_value
        scale = self.get_parameter('scale').get_parameter_value().double_value

        start_x = 0.8
        start_y = 4.5
        char_width = 0.7 * scale
        char_spacing = 0.5 * scale

        curr_x = start_x
        char_idx = 0

        for char in text.upper():
            if char == ' ':
                curr_x += char_width + char_spacing
                continue

            color = COLORS[char_idx % len(COLORS)]
            char_idx += 1

            if char in FONT:
                for p1, p2 in FONT[char]:
                    start_pt = (curr_x + p1[0] * scale, start_y + p1[1] * scale)
                    end_pt = (curr_x + p2[0] * scale, start_y + p2[1] * scale)
                    # Toll fel -> odamegy
                    self.commands.append({'target': start_pt, 'pen_off': 1, 'color': color})
                    # Toll le -> megrajzolja
                    self.commands.append({'target': end_pt, 'pen_off': 0, 'color': color})
                curr_x += char_width + char_spacing

        # Vegere felreallas: a teknos usszon el a sarokba toll nelkul, hogy lathato legyen a rajz
        self.commands.append({'target': (10.0, 1.0), 'pen_off': 1, 'color': (0, 0, 0)})
        self.get_logger().info(f'Palyatervezes kesz. Szoveg: "{text}", Lepesszam: {len(self.commands)}')

    def set_pen(self, off_val, rgb):
        pen_state = (off_val, rgb)
        if self.last_pen_state == pen_state:
            return
        if self.set_pen_cli.service_is_ready():
            req = SetPen.Request()
            req.r, req.g, req.b = rgb
            req.width = 4
            req.off = off_val
            self.set_pen_cli.call_async(req)
            self.last_pen_state = pen_state

    def control_loop(self):
        if self.current_pose is None:
            return

        if not self.initialized:
            self.build_path()
            self.initialized = True
            return

        if self.cmd_index >= len(self.commands):
            self.set_pen(1, (0, 0, 0))
            self.cmd_pub.publish(Twist())
            return

        current_cmd = self.commands[self.cmd_index]
        target_x, target_y = current_cmd['target']
        self.set_pen(current_cmd['pen_off'], current_cmd['color'])

        dx = target_x - self.current_pose.x
        dy = target_y - self.current_pose.y
        dist = math.sqrt(dx**2 + dy**2)

        # Pont elerve
        if dist < 0.06:
            self.cmd_index += 1
            if self.cmd_index >= len(self.commands):
                self.get_logger().info('Rajz befejezve!')
            return

        target_angle = math.atan2(dy, dx)
        angle_err = target_angle - self.current_pose.theta

        while angle_err > math.pi:
            angle_err -= 2 * math.pi
        while angle_err < -math.pi:
            angle_err += 2 * math.pi

        twist = Twist()
        # Ha a szoghiba nagyobb, alljon meg es csak forogjon (igy tokeletesen egyenesek lesznek a szarak)
        if abs(angle_err) > 0.15:
            twist.linear.x = 0.0
            twist.angular.z = 4.5 * angle_err
        else:
            twist.linear.x = min(2.5, max(0.4, 2.0 * dist))
            twist.angular.z = 3.0 * angle_err

        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = TextDrawerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()