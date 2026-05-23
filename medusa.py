import os
import time
import RPi.GPIO as GPIO

# Hardware Configuration (Medusa Node v1.01)
BUZZER_PIN = 18 
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
buzzer = GPIO.PWM(BUZZER_PIN, 1000) # 1kHz frequency for maximum acoustic penetration

print("--- MEDUSA NODE ONLINE v1.01 ---")
print("Status: Monitoring Layer 3 Heartbeat...")

try:
    while True:
        # Pinging Google DNS to verify Network Layer (Layer 3) path stability
        # Redirecting output to /dev/null to keep the console clean
        response = os.system("ping -c 1 -W 1 8.8.8.8 > /dev/null 2>&1")

        if response == 0:
            print("✔ Heartbeat: STABLE")
        else:
            print("🚨 ALERT: NETWORK CUTOUT! Triggering Physical Alarm...")
            buzzer.start(50) # 50% Duty Cycle
            time.sleep(1)    
            buzzer.stop()

        time.sleep(5) # Polling interval to balance responsiveness and network overhead
except KeyboardInterrupt:
    print("\n[!] Medusa Sentry Deactivated by User.")
    GPIO.cleanup()
