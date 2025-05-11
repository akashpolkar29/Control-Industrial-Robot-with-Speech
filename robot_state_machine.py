class RobotStateMachine:
    def __init__(self):
        self.state = "idle"

    def transition(self, command):
        print(f"🤖 Executing command: {command}")
        if command == "start":
            self.state = "active"
            print("✅ Robot started.")
        elif command == "stop":
            self.state = "idle"
            print("🛑 Robot stopped.")
        elif command == "move up":
            print("⬆️ Robot arm moving up.")
        elif command == "move down":
            print("⬇️ Robot arm moving down.")
        elif command == "rotate":
            print("🔄 Robot is rotating.")
        elif command == "grip":
            print("✊ Robot is gripping the object.")
        elif command == "release":
            print("🖐️ Robot released the object.")
        elif command == "move left":
            print("⬅️ Robot moving left.")
        elif command == "move right":
            print("➡️ Robot moving right.")
        elif command == "pick the object":
            print("📦 Picking the object.")
        elif command == "stop immediately":
            self.state = "emergency_stop"
            print("🚨 EMERGENCY STOP ACTIVATED!")
        else:
            print("❓ Unknown command.")
