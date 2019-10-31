ERROR   = 1
WARN    = 2
LOG     = 3
INFO    = 4

prefixes = {
	1:"[E*]",
	2:"[W*]",
	3:"[L*]",
	4:"[I*]"
}

def log(prefix, message):
	print(prefixes[prefix],message)
