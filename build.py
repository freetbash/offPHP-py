import os
import shutil
if __name__ == '__main__':
    try:
        shutil.rmtree("dist")
    except:
        pass
    cmd = "pyinstaller -w -i op.ico offPHP.py"
    os.system(cmd)
    # shutil.copytree("php", "dist/offPHP/php")
    shutil.copy("op.ico", "dist/offPHP/op.ico")
