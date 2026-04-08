# SO-ARM101 筆記

## 環境確認

```bash
# 確認 Motor Control Board 有接上
lsusb && ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null
# 正常應該看到 /dev/ttyACM0 和 QinHeng Electronics USB Single Serial

# 確認 lerobot 有安裝
python3 -c "import lerobot; print(lerobot.__version__)" 2>/dev/null || echo "未安裝"
```

## 安裝 LeRobot（用 uv）

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv init .
uv add lerobot
uv add "lerobot[feetech]"   # feetech 馬達驅動（必裝）
```

## 權限設定（只需做一次）

```bash
sudo usermod -a -G dialout asus
newgrp dialout   # 或登出再登入讓群組生效
```

---

## 燒錄馬達 ID

程式會自動引導你一顆一顆插馬達，**每次只接 1 顆**，按 Enter 後自動設定 ID。

**Follower arm：**
```bash
uv run python -m lerobot.scripts.lerobot_setup_motors --robot.type so101_follower --robot.port /dev/ttyACM0
```

**Leader arm：**
```bash
uv run python -m lerobot.scripts.lerobot_setup_motors --teleop.type so101_leader --teleop.port /dev/ttyACM0
```

---

## Follower Arm（執行臂）

馬達全部用 **C001（齒比 1/345）x6**，接同一塊 Motor Control Board。

| ID | 關節 |
|----|------|
| 1 | 底座旋轉 shoulder_pan |
| 2 | 肩膀 shoulder_lift |
| 3 | 手肘 elbow_flex |
| 4 | 手腕上下 wrist_flex |
| 5 | 手腕旋轉 wrist_roll |
| 6 | 夾爪 gripper |

---

## Leader Arm（遙控臂）

馬達共 6 顆，接另一塊 Motor Control Board：
- **C001 x1**（齒比 1/345）
- **C044 x2**（齒比 1/191）
- **C046 x3**（齒比 1/147）

| ID | 關節 | 馬達型號 | 齒比 |
|----|------|---------|------|
| 1 | 底座旋轉 shoulder_pan | C044 | 1/191 |
| 2 | 肩膀 shoulder_lift | C001 | 1/345 |
| 3 | 手肘 elbow_flex | C044 | 1/191 |
| 4 | 手腕上下 wrist_flex | C046 | 1/147 |
| 5 | 手腕旋轉 wrist_roll | C046 | 1/147 |
| 6 | 夾爪 gripper | C046 | 1/147 |

---

## 已知問題：燒錄時某顆馬達失敗

`lerobot_setup_motors` 會依序引導設定，若中途某顆失敗（接線鬆、偵測不到），後續顆數不會自動補上。

**症狀：** 校準或連線時出現 `Missing motor IDs: - 1` 或 `- 5` 之類的錯誤。

**處理方式：** 用以下腳本單獨補設指定馬達，不需要重跑全部：

```bash
uv run python setup_missing_motors.py
```

內容（`setup_missing_motors.py`）：
```python
from lerobot.robots.so_follower.config_so_follower import SOFollowerRobotConfig
from lerobot.robots.so_follower.so_follower import SOFollower

cfg = SOFollowerRobotConfig(port='/dev/ttyACM0')
robot = SOFollower(cfg)

for motor in ['shoulder_pan', 'wrist_roll']:  # 改成實際缺的馬達名稱
    input(f"Connect '{motor}' motor only and press enter.")
    robot.bus.setup_motor(motor)
    print(f"'{motor}' motor id set to {robot.bus.motors[motor].id}")
```

---

## 校準 Follower Arm

校準時需要**所有馬達都串接好**，一次完成。

```bash
uv run python -m lerobot.scripts.lerobot_calibrate --robot.type so101_follower --robot.port /dev/ttyACM0
```

步驟：
1. 先把手臂移到中間位置，按 Enter
2. 依序把每個關節（除了 wrist_roll）從最小轉到最大，按 Enter 停止記錄
3. 校準檔存在 `~/.cache/huggingface/lerobot/calibration/robots/so_follower/None.json`

> `wrist_roll` 被跳過是正常的，它是連續旋轉關節，程式用不同方式處理。

## 校準 Leader Arm

```bash
uv run python -m lerobot.scripts.lerobot_calibrate --teleop.type so101_leader --teleop.port /dev/ttyACM0
```

步驟同 Follower arm，校準檔存在 `~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/None.json`

---

## 校準結果（2026-03-29 / 2026-04-08）

### Follower Arm
| 關節 | MIN | MAX | 範圍 |
|------|-----|-----|------|
| shoulder_pan | 778 | 3475 | 2697 |
| shoulder_lift | 1411 | 3766 | 2355 |
| elbow_flex | 999 | 3188 | 2189 |
| wrist_flex | 1004 | 3158 | 2154 |
| gripper | 1573 | 3028 | 1455 |

### Leader Arm
| 關節 | MIN | MAX | 範圍 |
|------|-----|-----|------|
| shoulder_pan | 686 | 3339 | 2653 |
| shoulder_lift | 950 | 3284 | 2334 |
| elbow_flex | 1301 | 3495 | 2194 |
| wrist_flex | 761 | 3070 | 2309 |
| gripper | 2024 | 3252 | 1228 |

---

## 遙操作測試

兩塊板子都接上電腦（應看到 `/dev/ttyACM0` 和 `/dev/ttyACM1`）：

```bash
uv run python -m lerobot.scripts.lerobot_teleoperate --robot.type so101_follower --robot.port /dev/ttyACM0 --teleop.type so101_leader --teleop.port /dev/ttyACM1
```

> 如果手臂動錯隻，把 ttyACM0 和 ttyACM1 對調。

---

## 進度

- [x] 環境安裝（LeRobot 0.4.4 + feetech）
- [x] Follower arm 燒錄 6 顆馬達 ID
- [x] Follower arm 校準
- [x] Leader arm 燒錄 6 顆馬達 ID
- [x] Leader arm 校準
- [x] 遙操作測試成功（2026-04-08）
- [ ] 資料收集（record）
- [ ] AI 訓練（train）

## 下一步

參考官方教學進行資料收集與 AI 訓練：
https://huggingface.co/docs/lerobot/so101
