ERROR   = 1000
WARN    = 2000
LOG     = 3000
INFO    = 4000

prefixes = {
	1000:"[E*]",
	2000:"[W*]",
	3000:"[L*]",
	4000:"[I*]"
}

def log(prefix, message):
	if prefix != LOG: return

	print(prefixes[prefix],message)
