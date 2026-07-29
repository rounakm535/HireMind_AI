import subprocess, sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'sqlalchemy>=2.0.41'])
