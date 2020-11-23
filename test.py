import itertools

l = [1,2,3,4,5]
subsets = set(itertools.combinations(l,2))

print(subsets)