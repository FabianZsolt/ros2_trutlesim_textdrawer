from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    text_arg = DeclareLaunchArgument(
        'text_to_draw',
        default_value='ZSOLT',
        description='A kirajzolando szoveg'
    )
    scale_arg = DeclareLaunchArgument(
        'scale',
        default_value='1.25',
        description='Meretezesi arany'
    )

    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim'
    )

    drawer_node = Node(
        package='turtlesim_text_drawer',
        executable='drawer_node',
        name='text_drawer_node',
        output='screen',
        parameters=[{
            'text_to_draw': LaunchConfiguration('text_to_draw'),
            'scale': LaunchConfiguration('scale')
        }]
    )

    return LaunchDescription([
        text_arg,
        scale_arg,
        turtlesim_node,
        drawer_node
    ])