# attitudinal_psyche

Subtype calculator and other tools for attitudinal psyche (see https://attitudinalpsyche.com)

Licensed under the Creative Commons BY license: https://creativecommons.org/licenses/by/4.0/

> This license enables reusers to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator.

To run the script in interactive mode: `python ap_shadow_type_calculator.py`

To run the script with arguments: `python ap_shadow_type_calculator.py [ap_type] [subtype]`

AP type is any of the 24 permutation of FLEV (e.g. LFEV and LEFV).
Subtype is 4 digits between 0 and 4.

To create Discord bot (only needs to be done once):
- Create an application at https://discord.com/developers/applications
- Go to Bot tab
  - Set username and icon (can use `Shadow.jpg`) 
  - Enable "Public Bot"
  - Enable "Message Content Intent"
  - Copy token (for next step)
- Create `.env` file in same directory where `ap_discord.py` will be run (do not commit to git)
  - `DISCORD_TOKEN=<token from bot page>` 
  - This can be set as an environment variable instead
- Go to OAuth2 tab
  - Select "bot" and "applications.commands" under scopes
  - Select "Send Messages" in "Bot Permissions"
  - Copy generated URL. An admin for the Discord server can go there to add the bot to the server.

To run Discord server:
1. Make sure that Python is installed
2. Obtain .env file corresponding to bot and copy to this directory 
3. Run command:
   - Linux/Mac: `run_ap_discord.sh`
   - Windows: `run_ap_discord.bat`
   - Manual:
     1. Change to this directory
     2. Create VM (`python -m venv .venv`)
     3. Start VM (`. .venv/bin/activate` in Linux/Mac or `.venv\Scripts\activate.bat` in Windows)
     4. Use pip to install requirements.txt (`pip install -r requirements.txt`)
     5. Start Discord bot (`python ap_discord.py`)