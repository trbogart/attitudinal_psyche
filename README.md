# attitudinal_psyche

AP subtype calculator (see https://attitudinalpsyche.com)

Licensed under the Creative Commons BY license:
https://creativecommons.org/licenses/by/4.0/

```This license enables reusers to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator.```

To run the script in interactive mode:
`python ap_shadow_type_calculator.py`

To run the script with arguments:
`python ap_shadow_type_calculator.py [ap_type] [subtype]`

AP type is any of the 24 permutation of FLEV (e.g. LFEV and LEFV).
Subtype is 4 digits between 0 and 4.

To build Windows desktop program:
- Install pyinstaller (see https://pyinstaller.org/)
- pyinstaller --distpath dist\windows --onefile ap_shadow_type_calculator.py
- File will be created as dist/windows/ap_shadow_type_calculator.exe

To create Discord bot:
- Create an application at https://discord.com/developers/applications
- Go to Bot tab
  - Enable "Public Bot"
  - Enable "Message Content Intent"
  - Copy token
- Go to OAuth2 tab
  - Select "bot" and "applications.commands" under scopes
  - Select "Send Messages" in "Bot Permissions"
  - Copy generated URL. An admin for the Discord server can go there to add the bot to the server.
- Create `.env` file in same directory where `ap_shadow_type_discord.py` will be run (do not commit to git)
  - `DISCORD_TOKEN=<token from bot page>` 
- To run server:
  - `python ap_shadow_type_discord.py`