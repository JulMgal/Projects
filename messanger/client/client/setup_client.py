import sys
from cx_Freeze import setup, Executable

build_exe_options = {
      'packages': ['common', 'logs', 'client', 'unit_tests'],
}

setup(name="messanger_client",
      version="0.0.1",
      description="messanger_client",
      options={
            'build_exe': build_exe_options
      },
      executables=[Executable('client.py', base='Win32GUI', targetName='client.exe',)]
      )
