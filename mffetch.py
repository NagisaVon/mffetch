import requests

# open page
page = requests.get('https://dbenedetto.people.amherst.edu/math121/')

print(page.text)

# check list
# markdown link style [I'm an inline-style link](https://www.google.com)
listfilename = 'filelist.md'
## r-read b-binary w-write t-text-mode
listfile=open(listfilename, 'w')
list=listfile.read()
print(list)

# download file
rf = requests.get('https://dbenedetto.people.amherst.edu/math121/exam2spring17compact.pdf', allow_redirects=True)
open('exam2spring17compact.pdf', 'wb').write(rf.content)