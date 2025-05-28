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

To build Windows version:
- Install pyinstaller (see https://pyinstaller.org/)
- Run `pyinstaller --distpath dist\windows --onefile ap_shadow_type_calculator.py`
- File will be created as dist/windows/ap_shadow_type_calculator.exe

To build Mac version:
- Install pyinstaller (see https://pyinstaller.org/)
- Run `pyinstaller --distpath dist/macos --onefile --target-arch universal2 ap_shadow_type_calculator.py`
- File will be created as dist/windows/ap_shadow_type_calculator.exe
