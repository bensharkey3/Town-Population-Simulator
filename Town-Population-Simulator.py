import urllib.request

code = 'https://raw.githubusercontent.com/bensharkey3/Town-Population-Simulator/master/sourcecode.py'
response = urllib.request.urlopen(code)
data = response.read()
exec(data)