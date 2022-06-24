# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0
import os
import subprocess
import sys
import sysconfig
from pathlib import Path

package_name = "sim2real_docs"
current_dir = Path(__file__).parent
src_path = os.path.join(current_dir, package_name)
install_path = os.path.join(current_dir)
dst_path = sysconfig.get_path('purelib')

def main():
    subprocess.call([sys.executable, '-m', 'ensurepip','--upgrade'])
    subprocess.call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.call([sys.executable, '-m', 'pip', 'install', install_path], shell=True)

    if os.name == 'nt':
        subprocess.call(['xcopy', src_path, os.path.join(dst_path, package_name), '/s/h/e/k/f/c/i'])
    else:
        subprocess.call(['cp', '-r', src_path, dst_path])

if __name__ == "__main__":
    main()
