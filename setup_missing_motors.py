from lerobot.robots.so_follower.config_so_follower import SOFollowerRobotConfig
from lerobot.robots.so_follower.so_follower import SOFollower

cfg = SOFollowerRobotConfig(port='/dev/ttyACM0')
robot = SOFollower(cfg)

for motor in ['shoulder_pan', 'wrist_roll']:
    input(f"Connect '{motor}' motor only and press enter.")
    robot.bus.setup_motor(motor)
    print(f"'{motor}' motor id set to {robot.bus.motors[motor].id}")

print("Done!")
