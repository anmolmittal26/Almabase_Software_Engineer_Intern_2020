import requests
import json

def heapify(n, i, ll = []):  #heapify function for heapsort

    smallest = i
    left = 2*i+1
    right = 2*i+2

    if left < n and ll[smallest][1] > ll[left][1]:
        smallest = left
    if right < n and ll[smallest][1] > ll[right][1]:
        smallest = right

    if i != smallest:
        ll[i], ll[smallest] = ll[smallest], ll[i]
        heapify(n, smallest, ll)

def heapsort(ll = []):  #heapsort function
    n = len(ll)
    for i in range(n//2-1, -1, -1):
        heapify(n, i, ll)


def call_api(apicall, **kwargs):        #recursion function to iterate through all the pages recieved. 

    data = kwargs.get('page', [])

    resp = requests.get(apicall)
    data += resp.json()

    if len(data) > 4000: #Increase this number if repository count is more than 4000
        return (data)

    if 'next' in resp.links.keys():
        return (call_api(resp.links['next']['url'], page=data))

    return (data)

n, m, c = 6, 4, 0               # n = Top repos of organization, m = Top contributors of a particular repository
organization = 'microsoft'         # organization = The organization we want to get result

s1 = 'https://api.github.com/orgs/'
s2 = '/repos?per_page=100'

api_get_repos = s1+organization+s2      #final api_call = https://api.github.com/orgs/:organization/repos?per_page=100

data = call_api(api_get_repos)          #call of recursion function to recieve list of all repository

l = []       #list for storing the result

for xx in data:
    if xx["private"] != "false":    #omit this statement if we want to list private repository also
        x = xx["name"]      #name of repository
        y = xx["forks"]     #forks count of particular repository

        if c < n:
            l.append((x, y))    #tuple of (repository_name, forks_count)
            c += 1
            if c == n:
                heapsort(l)

        elif y > l[0][1]:
            l[0] = (x, y)
            heapify(c, 0, l)

length_of_repos = len(l)

for xx in range(length_of_repos-1, 0, -1):
    l[0], l[xx] = l[xx], l[0]
    heapify(xx, 0, l)

print "List of", n, "most popular repositories of", organization, "on the basis of number of forks and their top", m, "contributors are:"
print ""

count = 1

for i in range(0, length_of_repos):     #loop to iterate through top repository recieved

    s3 = 'https://api.github.com/repos/'
    s4 = '/contributors?per_page=100'

    top_contributors = s3+organization+'/'+l[i][0]+s4   #final api_call = https://api.github.com/repos/:organization/:repo_name/contributors?per_page=100

    print count,"=> Repository_name:", l[i][0]," || Forks_count: ", l[i][1]
    count += 1

    print "  Top", m, "contributors of repository", l[i][0], "are:"
    c = 0

    contributors_data = requests.get(top_contributors).json()  #call to retrieve list of top m contributors of respective repository

    for j in contributors_data:     #loop all the top contributors of the particular respository
        print "     ", c+1, "->", "Login_name:", j["login"], " ||  Contributions: ", j["contributions"]
        c += 1;
        if c >= m:
            break
    print ""
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print ""
