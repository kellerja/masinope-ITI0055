from prax3 import *

map_size = '300x300'
map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=bfs)
info['name'] = '{} with bfs'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=greedy, h=h)
info['name'] = '{} with greedy h=direct'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=greedy, h=h_man)
info['name'] = '{} with greedy h=manhattan'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=a_star, h=h)
info['name'] = '{} with a* h=direct'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=a_star, h=h_man)
info['name'] = '{} with a* h=manhattan'.format(map_size)
print(info)

print()
map_size = '300x300Empty'
map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=bfs)
info['name'] = '{} with bfs'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=greedy, h=h)
info['name'] = '{} with greedy h=direct'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=greedy, h=h_man)
info['name'] = '{} with greedy h=manhattan'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=a_star, h=h)
info['name'] = '{} with a* h=direct'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=a_star, h=h_man)
info['name'] = '{} with a* h=manhattan'.format(map_size)
print(info)

print()
map_size = '600x600'
map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=bfs)
info['name'] = '{} with bfs'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=greedy, h=h)
info['name'] = '{} with greedy h=direct'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=greedy, h=h_man)
info['name'] = '{} with greedy h=manhattan'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=a_star, h=h)
info['name'] = '{} with a* h=direct'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=a_star, h=h_man)
info['name'] = '{} with a* h=manhattan'.format(map_size)
print(info)

print()
map_size = '900x900'
map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=bfs)
info['name'] = '{} with bfs'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=greedy, h=h)
info['name'] = '{} with greedy h=direct'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=greedy, h=h_man)
info['name'] = '{} with greedy h=manhattan'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=a_star, h=h)
info['name'] = '{} with a* h=direct'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=a_star, h=h_man)
info['name'] = '{} with a* h=manhattan'.format(map_size)
print(info)

print()
map_size = '900x900Empty'
map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=bfs)
info['name'] = '{} with bfs'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=greedy, h=h)
info['name'] = '{} with greedy h=direct'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=greedy, h=h_man)
info['name'] = '{} with greedy h=manhattan'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=a_star, h=h)
info['name'] = '{} with a* h=direct'.format(map_size)
print(info)

map_data = load_map('{}.txt'.format(map_size))
path, info = search(map_data, algorithm=a_star, h=h_man)
info['name'] = '{} with a* h=manhattan'.format(map_size)
print(info)
