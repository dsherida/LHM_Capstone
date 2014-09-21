from fabric.api import *

env.user = "asu"
env.password = "devteam"
env.hosts = ["198.235.130.22"]

def apt_upgrade():
	sudo("apt-get update")
	sudo("apt-get upgrade -y")

def deploy():
	with cd("/srv/lhm_capstone"):
		run("git pull")
		run("/srv/lhm_capstone/LHM_Backend/venv/bin/pip install -r /srv/lhm_capstone/LHM_Backend/requirements.txt")
		run("touch .")
		sudo("service uwsgi restart")
