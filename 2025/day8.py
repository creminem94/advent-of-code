import os
import numpy as np

def dist(p1, p2):
    # 3d euclidean distance
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def compute_all_distances(points):
    n_points = len(points)
    distances = []
    for i in range(n_points):
        for j in range(i + 1, n_points):
            distances.append({
                'i': i,
                'j': j,
                'dist': int(dist(points[i], points[j]))
            })
    
    # sort distances by distance
    distances = sorted(distances, key=lambda x: x['dist'])
    return distances

def find_in_cluster(point_idx, clusters):
    for c_idx in range(len(clusters)):
        cluster = clusters[c_idx]
        if point_idx in cluster:
            return c_idx
    return -1

def part_1():
    with open(os.path.join(os.path.dirname(__file__), 'boxes.txt'), 'r') as file:
        # read lines
        content = file.read()
        point_list = content.splitlines()
        points = [tuple(map(int, line.split(','))) for line in point_list]
        distances = compute_all_distances(points)
        # print(np.count_nonzero(distances))
        clusters = []
        n_dist_to_computed = 1000
        for d in distances[:n_dist_to_computed]:
            i = d['i']
            j = d['j']
            i_cluster = find_in_cluster(i, clusters)
            j_cluster = find_in_cluster(j, clusters)
            if i_cluster == -1 and j_cluster == -1:
                # create new cluster
                clusters.append(set([i, j]))
            elif i_cluster != -1 and j_cluster == -1:
                clusters[i_cluster].add(j)
            elif i_cluster == -1 and j_cluster != -1:
                clusters[j_cluster].add(i)

            elif i_cluster != j_cluster:
                # merge clusters
                clusters[i_cluster] = clusters[i_cluster].union(clusters[j_cluster])
                del clusters[j_cluster]     
            # print(clusters)

        print(clusters)
        # get the 3 largest clusters
        clusters = sorted(clusters, key=lambda x: len(x), reverse=True)
        largest_clusters = clusters[:3]
        # multiply their sizes
        total = 1
        for c in largest_clusters:
            total *= len(c)

        print(total)
            
        

def part_2():
    with open(os.path.join(os.path.dirname(__file__), 'boxes.txt'), 'r') as file:
        # read lines
        content = file.read()
        point_list = content.splitlines()
        points = [tuple(map(int, line.split(','))) for line in point_list]
        distances = compute_all_distances(points)
        # print(np.count_nonzero(distances))
        clusters = []
        last_added_couple = (-1, -1)
        for d in distances:
            i = d['i']
            j = d['j']
            i_cluster = find_in_cluster(i, clusters)
            j_cluster = find_in_cluster(j, clusters)
            if i_cluster == -1 and j_cluster == -1:
                # create new cluster
                clusters.append(set([i, j]))
                last_added_couple = (i, j)
            elif i_cluster != -1 and j_cluster == -1:
                clusters[i_cluster].add(j)
                last_added_couple = (i, j)
            elif i_cluster == -1 and j_cluster != -1:
                clusters[j_cluster].add(i)
                last_added_couple = (i, j)
            elif i_cluster != j_cluster:
                # merge clusters
                clusters[i_cluster] = clusters[i_cluster].union(clusters[j_cluster])
                del clusters[j_cluster]     
                last_added_couple = (i, j)
            # print(clusters)

        last_points = points[last_added_couple[0]], points[last_added_couple[1]]
        print(f'Last added points: {last_points}')
        # multiply their x coords
        total = last_points[0][0] * last_points[1][0]
        print(total)
            
part_2()    