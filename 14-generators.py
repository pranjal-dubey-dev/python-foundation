'''Generator is a special kind of function that returns 
an iterator object. 
Use yield to produce series of result over time.
'''

from typing import Any, Generator
from memory_profiler import profile, memory_usage
import random

def square_numbers(nums: list):
    for i in nums:
        yield (i*i)


my_nums = square_numbers([1, 2, 3, 4, 5])

# my_nums = [x*x for x in [1, 2, 3, 4, 5]]  list_comprehension
print(my_nums)     #<generator object square_numbers at 0x000001f0606d9150>

my_nums = (x*x for x in [1, 2, 3, 4, 5])
print(my_nums)
print(list(my_nums))
# print(next(my_nums))
# print(next(my_nums))
# print(next(my_nums))
# print(next(my_nums))
# print(next(my_nums))

#print(next(my_nums))     StopIteration



for num in my_nums:
    print(num)



def fun(max: int) -> Generator[Any, None, None]:
    i =1
    while i<=max:
        yield i
        i += 1

ctr = fun(5)

for n in ctr:
    print(n)


names = ['Pranjal', 'Meet', 'Sakshi', 'Diya', 'Akash', 'Rick']
majors = ['Maths', 'Engineering', 'CompSci', 'Arts', 'Business']



@profile
def people_list(num_people):
    result = []
    for i in range(num_people):
        person = { 
            'id' : i,
            'name': random.choice(names),
            'major' : random.choice(majors)
        }
        result.append(person)
    return result

@profile
def people_generator(num_people):
    for i in range(num_people):
        person = { 
            'id' : i,
            'name': random.choice(names),
            'major' : random.choice(majors)
        }
        yield person



def consume_list():
    people = people_list(1_000_000)


def consume_generator():
    gen = people_generator(1_000_000)

    for _ in range(1_000_000):
        next(gen)


if __name__ == '__main__':
    mem_list = memory_usage(consume_list)
    print("List memory used:", max(mem_list) - min(mem_list), "MiB")

    mem_generator = memory_usage(consume_generator)
    print("Generator memory used:", max(mem_generator) - min(mem_generator), "MiB")




 
