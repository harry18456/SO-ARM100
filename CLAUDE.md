# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SO-ARM100 is a hardware design repository for the SO-100 and SO-101 robot arms, created by RobotStudio in collaboration with Hugging Face. The SO-101 is the current generation. The arms are designed for AI teleoperation using the LeRobot library — a leader arm (hand-operated) controls a follower arm (motorized), and the recorded demonstrations are used to train policies.

This is primarily a **hardware documentation repo** (STL files, BOMs, assembly guides), not a software project. The Python/LeRobot integration is for motor setup, calibration, and teleoperation.

## Repository Structure

- `STL/` — 3D printable parts for SO-100 and SO-101 (follower and leader arms)
- `STEP/` — CAD source files
- `Simulation/` — URDF files for SO-100 and SO-101 simulation
- `Mini/` — Miniature version of the arm
- `Optional/` — Add-on hardware (camera mounts, compliant grippers, base mounts, etc.)
- `media/` — Images for documentation
- `NOTE.md` — Local working notes for motor setup, calibration, and teleoperation

## Commands

All commands use `uv` as the package manager.

```bash
# Install dependencies
uv add lerobot
uv add "lerobot[feetech]"

# Find connected motor control board port
ls /dev/ttyACM* /dev/ttyUSB*

# Setup motor IDs (one motor at a time)
uv run python -m lerobot.scripts.lerobot_setup_motors --robot.type so101_follower --robot.port /dev/ttyACM0
uv run python -m lerobot.scripts.lerobot_setup_motors --teleop.type so101_leader --teleop.port /dev/ttyACM0

# Calibrate arms (all motors connected)
uv run python -m lerobot.scripts.lerobot_calibrate --robot.type so101_follower --robot.port /dev/ttyACM0
uv run python -m lerobot.scripts.lerobot_calibrate --teleop.type so101_leader --teleop.port /dev/ttyACM0

# Teleoperate (both arms connected)
uv run python -m lerobot.scripts.lerobot_teleoperate --robot.type so101_follower --robot.port /dev/ttyACM0 --teleop.type so101_leader --teleop.port /dev/ttyACM1
```

## Key Details

- **Motors**: STS3215 servos by Feetech, controlled via `scservo_sdk` (installed as part of `lerobot[feetech]`)
- **Motor control board**: Waveshare board using QinHeng CH341 chip, appears as `/dev/ttyACM*`
- **Permission**: User must be in the `dialout` group to access serial ports (`sudo usermod -a -G dialout $USER`)
- **SO-101 follower arm**: 6x C001 motors (1/345 gear ratio), all identical
- **SO-101 leader arm**: Mixed gear ratios — 1x C001 (1/345), 2x C044 (1/191), 3x C046 (1/147)
- **Calibration files**: Stored in `~/.cache/huggingface/lerobot/calibration/`
- **`wrist_roll`** is a continuous rotation joint — it is intentionally skipped during manual range-of-motion calibration
- **Motor setup quirk**: `lerobot_setup_motors` must go in order. If a motor fails mid-sequence, use a custom script to set individual motor IDs (see `setup_missing_motors.py`)
