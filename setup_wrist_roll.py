from lerobot.robots.so_follower.config_so_follower import SOFollowerRobotConfig
from lerobot.robots.so_follower.so_follower import SOFollower

cfg = SOFollowerRobotConfig(port='/dev/ttyACM0')
robot = SOFollower(cfg)
input("Connect wrist_roll motor only and press enter.")
robot.bus.setup_motor('wrist_roll')
print('wrist_roll motor id set to', robot.bus.motors['wrist_roll'].id)
