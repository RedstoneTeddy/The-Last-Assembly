python -m nuitka ^
  --mode=standalone ^
  --output-filename="The Last Assembly.exe" ^
  --include-data-dir=assets=assets ^
  --include-data-dir=map_data=map_data ^
  --windows-icon-from-ico=assets/icon.png ^
  --windows-icon-from-ico=assets/icon.ico ^
  --windows-console-mode=disable ^
  main.py
