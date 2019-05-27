from functools import reduce

train_data = [['Yes', 'No', 'No', 'Yes', 'Some', '$$$', 'No', 'Yes', 'French', '0-10', 'Yes'],
    ['Yes', 'No', 'No', 'Yes', 'Full', '$', 'No', 'No', 'Thai', '30-60', 'No'],
    ['No', 'Yes', 'No', 'No', 'Some', '$', 'No', 'No', 'Burger', '0-10', 'Yes'],
    ['Yes', 'No', 'Yes', 'Yes', 'Full', '$', 'No', 'No', 'Thai', '10-30', 'Yes'],
    ['Yes', 'No', 'Yes', 'No', 'Full', '$$$', 'No', 'Yes', 'French', '>60', 'No'],
    ['No', 'Yes', 'No', 'Yes', 'Some', '$$', 'Yes', 'Yes', 'Italian', '0-10', 'Yes'],
    ['No', 'Yes', 'No', 'No', 'None', '$', 'Yes', 'No', 'Burger', '0-10', 'No'],
    ['No', 'No', 'No', 'Yes', 'Some', '$$', 'Yes', 'Yes', 'Thai', '0-10', 'Yes'],
    ['No', 'Yes', 'Yes', 'No', 'Full', '$', 'Yes', 'No', 'Burger', '>60', 'No'],
    ['Yes', 'Yes', 'Yes', 'Yes', 'Full', '$$$', 'No', 'Yes', 'Italian', '10-30', 'No'],
    ['No', 'No', 'No', 'No', 'None', '$', 'No', 'No', 'Thai', '0-10', 'No'],
    ['Yes', 'Yes', 'Yes', 'Yes', 'Full', '$', 'No', 'No', 'Burger', '30-60', 'Yes']
]

class_wait = [{} for _ in range(len(train_data) - 2)]
class_leave = [{} for _ in range(len(train_data) - 2)]
total = [{} for _ in range(len(train_data) - 2)]

for sample in train_data:
    for i, attr in enumerate(sample):
        if (i == 10): continue
        if sample[10] == 'Yes':
            class_wait[i][attr] = class_wait[i].get(attr, 0) + 1
        else:
            class_leave[i][attr] = class_leave[i].get(attr, 0) + 1
        total[i][attr] = total[i].get(attr, 0) + 1

print('Yes', class_wait)
print('No', class_leave)
print('Total', total)
def calc_attr_p(attr, attr_value, class_value):
    cur_class = class_wait if class_value == 'Yes' else class_leave
    return (cur_class[attr].get(attr_value, 0) + 1) /\
           (sum([cur_class[attr].get(x, 0) for x in cur_class[attr]]) + len(total[attr]))


class_wait_P = [{x: calc_attr_p(i, x, 'Yes') for x, y in attr_count.items()} for i, attr_count in enumerate(class_wait)]
class_leave_P = [{x: calc_attr_p(i, x, 'No') for x, y in attr_count.items()} for i, attr_count in enumerate(class_leave)]

class_wait_p = len(list(filter(lambda x: x[10] == 'Yes', train_data)))
class_leave_p = (len(train_data) - class_wait_p) / len(train_data)
class_wait_p /= len(train_data)


def classification(attrs):
    class_wait_p_given_attrs = class_wait_p * reduce(lambda x, y: x * y,
                                                     [x.get(attrs[i], calc_attr_p(i, attrs[i], 'Yes'))
                                                      for i, x in enumerate(class_wait_P)])
    class_leave_p_given_attrs = class_leave_p * reduce(lambda x, y: x * y,
                                                       [x.get(attrs[i], calc_attr_p(i, attrs[i], 'No'))
                                                        for i, x in enumerate(class_leave_P)])
    #print(class_wait_p_given_attrs, class_leave_p_given_attrs)
    return 'Yes' if class_wait_p_given_attrs > class_leave_p_given_attrs else 'No'


print('Yes', class_wait_P)
print('No', class_leave_P)
print('P(wait aka yes)=', class_wait_p)
print('P(leave aka no)=', class_leave_p)
for sample in train_data:
    result = classification(sample[:-1])
    if result != sample[-1]:
        print('Mistake', sample, 'Result', result)

print(classification(['Yes', 'Yes', 'Yes', 'Yes', 'None', '$$', 'No', 'Yes', 'Thai', '10-30']))
print(classification(['Yes', 'No', 'Yes', 'No', 'Some', '$', 'No', 'Yes', 'Italian', '>60']))
