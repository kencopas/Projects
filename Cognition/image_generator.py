from random import randint, uniform


# my_image = (0.4, 0.4, 0.4,
#             0.4, 0, 0,
#             0.2, 0.8, 0)



def gen_set(n, length):
    my_dict = {}
    weight_graph = [round(uniform(0, 1), 1) for _ in range(length**2)]
    for _ in range(n):
        # new_image = my_image # Custom image
        new_image = tuple(randint(0,10)/10 for _ in range(length**2)) # Random image
        my_dict[new_image] = eval_image(new_image, weight_graph)
    return my_dict

def eval_image(image, weight_graph):
    return round(sum([w*x for w, x in zip(weight_graph, image)])/sum(weight_graph), 3)