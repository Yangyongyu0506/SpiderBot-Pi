import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/yangy/SpiderBot/ros2_workspace/install/sensor_debug'
