import os
import json


def get_token() -> str | None:
    token = os.getenv("DISCORD_TOKEN")
    if token:
        return token.strip()

    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("DISCORD_TOKEN="):
                    token = line.split("=", 1)[1].strip().strip("\"' ")
                    if token:
                        return token

    cfg_path = "config.json"
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        token = data.get("DISCORD_TOKEN") or data.get("token")
        if token:
            return token.strip()

    return None