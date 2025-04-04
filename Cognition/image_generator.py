from random import randint, uniform


# my_image = (0.4, 0.4, 0.4,
#             0.4, 0, 0,
#             0.2, 0.8, 0)


weight_graph = [round(uniform(0, 1), 1) for _ in range(9)]

def gen_set(n):
    my_dict = {}
    for _ in range(n):
        # new_image = my_image # Custom image
        new_image = tuple(randint(0,10)/10 for _ in range(9)) # Random image
        my_dict[new_image] = eval_image(new_image)
    return my_dict

def eval_image(image):
    return round(sum([w*x for w, x in zip(weight_graph, image)])/4.5, 3)