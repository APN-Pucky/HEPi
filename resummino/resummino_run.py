import subprocess
from string import Template
import numpy as np

"""
resummino_params
"""

def queue(params):
	names = []
	for d in params:
		# TODO insert defautl if missing in d!
		name="_".join("".join(str(_[0]) + "_" + str(_[1])) for _ in d.items())
		with open('plot_template.in', 'r') as f:
			src = Template(f.read())
			result = src.substitute(d)
			open("input/" + name, "w").write(result)			
			open("output/" + name +".out", "w").write(result + "\n\n")			
		sname = d['slha']
		with open('mastercode.in', 'r') as f:
			src = Template(f.read())
			result = src.substitute(d)
			open("input/" + sname, "w").write(result)			
			open("output/" + name +".out", "a").write(result + "\n\n")			
		names.append(name)
	return names


def run( names ):
	res_path = "~/git/resummino_ug_to_UX_vNLO/"
	template = res_path + 'build/bin/resummino ./input/{} >> ./output/{}.out'

	args = names
	# Run commands in parallel
	processes = []

	for arg in args:
		command = template.format(arg,arg)
		process = subprocess.Popen(command, shell=True)
		processes.append(process)

	# Collect statuses
	output = [p.wait() for p in processes]

sp = []
p = {'energy' : 13000, 'p1': 2000002, 'p2': 1000022, 'slha' : "mastercode.in" , "mu_f" : 1. , "mu_r" : 1.}
for mu_f in np.logspace(-1,1,3):
	for mu_r in np.logspace(-1,1,3):
		p['mu_r'] = mu_r
		p['mu_f'] = mu_f
		sp.append(p.copy())

print(sp)
names = queue(sp)
run(names)

