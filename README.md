# UXPatcher
An open-source alternative to UltraUXThemePatcher, allows you to install third-party themes.

The patch works by modyfying a function in `themeui.dll` and `uxinit.dll` to skip a signature check. All credit for the patch goes to [M. Hoefs](https://mhoefs.eu/index.php?lang=en).

Tested on Windows 10 22H2, build 19045.4529. If you want support for another version, open an issue.

> [!CAUTION]
> Modifying system files always poses a risk of rendering your system unbootable. Make sure you have an up-to-date restore point, as well as a copy of the original DLLs and another bootable drive in case things go wrong.

```
python3 patch.py
```
Then boot into safe mode or an installer USB and replace the two files in `%windir%\System32` with the patched copies.
