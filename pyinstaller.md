# === 以下适用于 windows ===

## -- 请先进入环境 --

运行
``` shell
conda activate lottery

PyInstaller -D console.spec
PyInstaller -D main.spec

mkdir .\dist\lottery
xcopy ".\dist\console\*.*" ".\dist\lottery" /e /y
xcopy ".\dist\main\*.*" ".\dist\lottery" /e /y

rd __pycache__ build dist\console dist\main /q/s

```

或直接启动`builder.bat`