# Incremental Discord Bot

An open-source incremental / idle clicker Discord bot written in Python.

Click to earn resources, buy buildings for passive income, unlock powerful gem and dark-matter upgrades, and reincarnate to push your progress even further.

---

## Features

- 💰 **Main currency** – Earn resources by clicking and from buildings.
- 💎 **Gems** – Mid-game currency used to buy permanent upgrades.
- 🌑 **Dark Matter** – Late-game currency used for reality-warping upgrades.
- 🏗 **Lots of buildings** – Progress from basic farms to multiverse structures.
- ✨ **Reincarnation system** – Reset your run to gain reincarnation points and a permanent multiplier.
- 📈 **Permanent upgrades**
  - Gem upgrades: click power, production boosts, cost discounts.
  - Dark upgrades: multiply reincarnation rewards and global power.
- 🧮 **Offline progress** – Income is calculated based on time since last action.
- 💾 **Per-user saves** – Each user has their own save file under `userdata/`.

---

## Tech Stack

- **Language:** Python 3.10+  
- **Library:** [discord.py](https://github.com/Rapptz/discord.py) (slash commands + components)  
- **Storage:** JSON files per user (`userdata/<user_id>.json`)

---

## Commands Overview

All commands are **slash commands**.

### Core Gameplay

- `/click`  
  Opens a private GUI (ephemeral message) with a **Click** button. Each press:
  - Gives resources based on your current multiplier and upgrades.
  - Updates the embed to show your current resources.
  - Doesn’t spam the channel.

- `/shop`  
  Opens a private shop GUI:
  - Select a building from a dropdown.
  - See its cost, income, and how many you own.
  - Buttons:
    - **Buy 1**
    - **Buy 10**
  - Buying buildings increases your passive income in all currencies.

- `/stats`  
  Shows your overall progression in a nice embed:
  - 💰 Resources and income/sec  
  - 💎 Gems and income/sec  
  - 🌑 Dark Matter and income/sec  
  - 📈 Cash multiplier  
  - 🖱 Total clicks  
  - 🔁 Reincarnations  
  - ✨ Reincarnation points  
  - 💎 Gem upgrade levels  
  - 🌑 Dark upgrade levels  
  - 🏛 A summary of owned buildings  
  - Level (based on total lifetime resources)

### Upgrades

- `/upgrades`  
  Gem upgrades (spent with 💎). Includes things like:
  - **Click Power** – more resources per click.
  - **Production Boost** – more income from all buildings.
  - **Shop Discount** – buildings become cheaper.

  GUI:
  - Select upgrade from dropdown.
  - **Buy 1** / **Buy 10** with a button.
  - Costs scale with each level.

- `/darklab`  
  Dark matter upgrades (spent with 🌑). Includes things like:
  - **Reincarnation Boost** – more reincarnation points per reset.
  - **Reality Warp** – global multiplier to production and clicks.

  GUI:
  - Select upgrade from dropdown.
  - **Buy 1** / **Buy 5** with buttons.
  - Costs scale aggressively (late game content).

### Progression / Prestige

- `/boost`  
  Spend **resources** to permanently increase your cash multiplier.  
  Each boost costs more than the previous one.

- `/reincarnate`  
  Prestige / reset mechanic:
  - You must reach a minimum **lifetime resources** threshold.
  - When you reincarnate:
    - You **lose** current resources, buildings, and clicks.
    - You **gain** a large amount of **reincarnation points** (based on lifetime resources and dark upgrades).
    - These points permanently increase your cash multiplier.
  - Your lifetime resources persist so future reincarnations get stronger.

---

If you want to tweak **game balance** (building costs, incomes, upgrade values, reincarnation rewards), you only need to touch:

* `data/balance.py`

---

## Setup & Installation

### 1. Clone the repository

bash
git clone https://github.com/0Chessz0/Incremental-Discord-Bot.git
cd incremental-discord-bot

### 2. Create a virtual environment (optional but recommended)

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate


### 3. Install dependencies

pip install -r requirements.txt

---

## Discord Bot Setup

### 1. Create a Discord application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application**, give it a name, and create it.
3. Go to the **Bot** tab:

   * Click **Add Bot**.
   * Enable **Privileged Gateway Intents**
4. Under **Token**, click **Reset Token** or **Copy** and **keep it secret**.

### 2. Invite the bot to your server

1. In the Developer Portal, go to **OAuth2 → URL Generator**.
2. Under **Scopes**, check:

   * `bot`
   * `applications.commands`
3. Under **Bot Permissions**, give at least:

   * `Send Messages`
   * `Use Application Commands`
4. Copy the generated URL, open it in your browser, and invite the bot to your server.


## Configuration (Bot Token)

You must set your bot token. There are 3 supported ways:

### Option 1: Environment variable

bash
# Windows (PowerShell)
$env:DISCORD_TOKEN="YOUR_BOT_TOKEN_HERE"

# Linux/macOS
export DISCORD_TOKEN="YOUR_BOT_TOKEN_HERE"

### Option 2: `.env` file

Create a file named `.env` in the project root:

env
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE

### Option 3: `config.json`

Create `config.json` in the project root:

json
{
  "DISCORD_TOKEN": "YOUR_BOT_TOKEN_HERE"
}

> ⚠️ **Never commit your token to GitHub**. Treat it like a password.



## Running the Bot

From the project root:
python bot.py

You should see logs like:

Synced X slash commands.
Logged in as Incremental Discord Bot#1234 (ID: 123456789012345678)

If you see an error about the token, double-check your `.env`, environment variable, or `config.json`.


## How to Play

1. In your Discord server, type `/click` and press enter.

   * A private clicker GUI will appear with a **Click** button and your current resources.
2. Use `/shop`:

   * Buy buildings to start generating passive income in resources, gems, and dark matter.
3. Use `/stats`:

   * Check your current income, currencies, buildings, upgrades, and reincarnation status.
4. Use `/upgrades` when you have gems:

   * Buy gem upgrades to boost click power, production, and reduce costs.
5. Use `/darklab` when you start getting dark matter:

   * Buy dark upgrades to massively boost reincarnation rewards and global multipliers.
6. Use `/boost`:

   * Spend resources on permanent multiplier boosts.
7. When your progress slows, use `/reincarnate`:

   * Trade your current run for a lot of reincarnation points and a stronger multiplier, then start again stronger.

Play loop:
**click → buy buildings → earn more → upgrade with gems → upgrade with dark matter → reincarnate → repeat**.

## Saving & Data

* All player data is stored in JSON under `userdata/`:

  * `userdata/<discord_user_id>.json`
* Data is personal per user and includes:

  * Currencies, buildings, upgrades, reincarnations, etc.
* The bot supports “offline” income by tracking the last update time.

To reset yourself manually, you can delete your own JSON file while the bot is stopped.

## Contributing

Contributions are welcome!

Ideas:

* More buildings / upgrade types
* New currencies or zones
* Achievements and challenges
* Balancing tweaks

Feel free to open an issue or submit a pull request.


## License

This project is licensed under the **MIT License**.
See the [`LICENSE`](./LICENSE) file for details.
