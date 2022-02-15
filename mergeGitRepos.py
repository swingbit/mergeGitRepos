#!/usr/bin/python

import subprocess
import yaml
import logging
import argparse

log_levels = {
	'critical': logging.CRITICAL,
	'error': logging.ERROR,
	'warn': logging.WARNING,
	'warning': logging.WARNING,
	'info': logging.INFO,
	'debug': logging.DEBUG
}

parser = argparse.ArgumentParser()
parser.add_argument(
	'-log',
	'--loglevel',
	choices = list(log_levels.keys()),
	default='info',
	help='Select logging level. Example --loglevel debug, default=info'
)
args = parser.parse_args()

logging.basicConfig(level=log_levels[args.loglevel.lower()], format='[%(levelname)s] %(message)s')

# helper for cmdline execution
def shell(cmd, cwd=None, stdout=None, stderr=None):
		logging.debug(f"(cwd={cwd}) excuting: {cmd}")
		p = subprocess.Popen(cmd.split(' '), cwd=cwd, stdout=stdout, stderr=stderr)
		p.wait()
		return p.returncode

# Check requirements
for cmd in [ 'git', 'git filter-repo' ]:
	if shell(cmd + " --version", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
		logging.fatal(f"{cmd} not available. Aborting.")
		exit(1)


# Load configuration
with open('mergeGitRepos.conf', 'r') as file:
		conf = yaml.safe_load(file)
try:
	NEWREPO = conf['newrepo']
	MAPPING = conf['mapping']
except:
	logging.fatal("The minimal configuration should include top-level definitions 'newrepo', 'mapping'")
	exit(2)

logging.info("# Cloning and preparing repos for merge")
for r in MAPPING.keys():
	shell(f"rm -rf {r}")
	logging.info(f"## Cloning and preparing repo {r}")
	shell(f"git clone --quiet {MAPPING[r]['gitparent']}/{r}.git")
	for b in MAPPING[r]['branches'].keys():
		# If branch exists, just set the upstream
		if shell(f"git rev-parse --verify {b}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=r) == 0:
			shell(f"git branch --quiet -u origin {b}", cwd=r)
		# Otherwise, also create it
		else:
			shell(f"git branch --quiet --track {b} origin/{b}", cwd=r)
	
	# Remove origin remote so nothing can be accidentally pushed upstream to the original repos
	shell("git remote rm origin", cwd=r)
	# Move the repo to a subfolder with the same name, and rewrite all paths
	subfolder = r
	if 'subfolder' in MAPPING[r]:
		subfolder = MAPPING[r]['subfolder']
	shell(f"git filter-repo --quiet --force --to-subdirectory-filter {subfolder}", cwd=r)

# Start work on the new repo
logging.info("# Initialising new repo")
shell(f"rm -rf {NEWREPO}")
shell(f"git init --quiet {NEWREPO}")

logging.info("# Merging repos into new repo")
for r in MAPPING.keys():
	logging.info(f"## Merging repo {r}")
	# Fetch from the previously modified source repo
	shell(f"git remote add {r} ../{r}", cwd=NEWREPO)
	shell(f"git fetch -q {r}", cwd=NEWREPO)
	for b, b1 in MAPPING[r]['branches'].items():
		branches = b1
		if not isinstance(b1, list):
			branches = [b1]
		for branch in branches:
			logging.info(f"merge {r}/{b} into {NEWREPO}/{branch}")
			# If branch exists, just switch to it
			if shell(f"git rev-parse --verify {branch}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=NEWREPO) == 0:
				shell(f"git checkout --quiet {branch}", cwd=NEWREPO)
			# Otherwise, create it and set the start-point
			else:
				shell(f"git checkout --quiet -b {branch} {r}/{b}", cwd=NEWREPO)
			# Merge
			shell(f"git merge --quiet --no-edit --allow-unrelated-histories {r}/{b}", cwd=NEWREPO)
	shell(f"git remote rm {r}", cwd=NEWREPO)

