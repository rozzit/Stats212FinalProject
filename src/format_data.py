
lines = open('SOL_scores_by_subgroup.csv', 'r').read().splitlines()

seen_IDs = set()
output_lines = []
for line in lines[1:]:
    id = line.split(',')[0].strip()
    if id not in seen_IDs:
        seen_IDs.add(id)
        output_lines += [line]

# print(output_lines)
# print(seen_IDs)
print("Missing data on IDs:")
print(sorted(list(map(int, list(set(str(i) for i in range(1, 998)) - seen_IDs)))))

# Missing data on IDs:
# [42, 85, 128, 171, 214, 257, 300, 343, 386, 429, 472, 515, 558, 601, 644, 687, 730, 773, 816, 859, 902, 945, 988]

with open('SOL_scores_by_subgroup.csv', 'w+') as f_out:
    f_out.write(lines[0] + '\n')
    f_out.write('\n'.join(output_lines))