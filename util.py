def putstring(what, where):
    import StringIO
    from fabric.api import put
    put(StringIO.StringIO(what), where)

def append(what,where):
	import fabric.contrib.files
	fabric.contrib.files.append(where,what)


"""This ensures that the line you specify appears somewhere in the config file.  If not, it is added to the end."""
def config(what,where):
	import fabric.contrib.files
	if not fabric.contrib.files.contains(where,what):
		append(what,where)