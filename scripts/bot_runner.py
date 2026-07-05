#!/usr/bin/env python3
"""
⏰ bot_runner.py — Multi-Script Scheduler / Runner

Run beberapa script secara paralel atau sequential dengan interval.
Berguna untuk mengaktifkan banyak monitor sekaligus dari 1 command.

Config format (bot_config.json):
    {
        "bots": [
            {"name": "token-checker", "script": "check_token.py", "args": ["<MINT>"], "interval": 300},
            {"name": "whale-tracker", "script": "whale_tracker.py", "args": ["<MINT>"], "interval": 60},
            {"name": "price-alert", "script": "price_alert.py", "args": ["--mint", "<MINT>", "--above", "0.001"], "interval": null}
        ]
    }

Usage:
    python bot_runner.py --config bot_config.json
    python bot_runner.py --config bot_config.json --dry-run
    python bot_runner.py --status

Dependencies:
    pip install requests
"""
import os
import sys
import json
import time
import signal
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

STATE_FILE = Path.home() / ".solana_bot_runner.json"


class BotRunner:
    def __init__(self, config_path: str, dry_run: bool = False):
        self.config_path = config_path
        self.dry_run = dry_run
        self.config = json.loads(Path(config_path).read_text())
        self.bots = self.config["bots"]
        self.running = {}

    def log(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {msg}", flush=True)

    def run_once(self, bot: dict):
        """Run single bot."""
        name = bot["name"]
        script = bot["script"]
        args = bot.get("args", [])

        cmd = [sys.executable, script] + args
        self.log(f"▶️  Running {name}: {' '.join(cmd)}")

        if self.dry_run:
            return

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            self.running[name] = {
                "last_run": datetime.now().isoformat(),
                "exit_code": result.returncode,
                "stdout_lines": len(result.stdout.splitlines()),
            }
            if result.returncode != 0:
                self.log(f"⚠️  {name} exited {result.returncode}: {result.stderr[:200]}")
        except subprocess.TimeoutExpired:
            self.log(f"⏰ {name} timed out")
        except Exception as e:
            self.log(f"❌ {name} error: {e}")

    def save_state(self):
        STATE_FILE.write_text(json.dumps(self.running, indent=2))

    def run_loop(self):
        """Main scheduler loop."""
        self.log(f"🚀 Bot Runner — {len(self.bots)} bot(s)")
        for b in self.bots:
            self.log(f"   • {b['name']}: every {b.get('interval', 'once')}s")

        # Separate repeating vs one-shot
        repeating = [b for b in self.bots if b.get("interval")]
        one_shot = [b for b in self.bots if not b.get("interval")]

        # Run one-shot immediately
        for bot in one_shot:
            self.run_once(bot)

        if not repeating:
            self.log("✅ All one-shot bots completed.")
            return

        last_run = {b["name"]: 0 for b in repeating}

        def shutdown(signum, frame):
            self.log("\n👋 Shutting down...")
            self.save_state()
            sys.exit(0)

        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        try:
            while True:
                now = time.time()
                for bot in repeating:
                    name = bot["name"]
                    interval = bot["interval"]
                    if now - last_run[name] >= interval:
                        self.run_once(bot)
                        last_run[name] = now
                        self.save_state()
                time.sleep(1)
        except KeyboardInterrupt:
            shutdown(None, None)


def show_status():
    """Show last known status."""
    if not STATE_FILE.exists():
        print("📭 No state recorded yet.")
        return
    state = json.loads(STATE_FILE.read_text())
    print(f"\n📊 Bot Status:\n")
    for name, info in state.items():
        last = info.get("last_run", "?")
        ec = info.get("exit_code", "?")
        lines = info.get("stdout_lines", "?")
        print(f"  {name:<20}  last: {last}  exit: {ec}  lines: {lines}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Multi-bot scheduler")
    parser.add_argument("--config", help="Config JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Show commands without running")
    parser.add_argument("--status", action="store_true", help="Show last run status")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if not args.config or not Path(args.config).exists():
        parser.print_help()
        sys.exit(1)

    runner = BotRunner(args.config, dry_run=args.dry_run)
    runner.run_loop()


if __name__ == "__main__":
    main()
