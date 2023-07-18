# Use python dict to realize reduce
def reduce(arr_list):
    reduce_dict = {}
    
    for arr in arr_list:
        for key in arr: 
            if key in reduce_dict:
                temp = reduce_dict[key]
                reduce_dict[key] = temp + 1
            else:
                reduce_dict[key] = 1

    for item in reduce_dict.items():
        print(item)
    return reduce_dict
