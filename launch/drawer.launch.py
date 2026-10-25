from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. Turtlesim ablak automatikus inditasa
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),
        # 2. Sajat rajzolo node inditasa paraméterrel
        Node(
            package='turtlesim_text_drawer',
            executable='drawer_node',
            name='text_drawer_node',
            output='screen',
            parameters=[
                {'text_to_draw': 'ROS 2'},
                {'scale': 1.6}
            ]
        )
    ])