# Using `magique.declarative` objects

That module contains entities to avoid using `while (true)` and another imperative constructions
enforcing thread management and cycling. The objects suggest using callbacks like an Observer pattern
You can subscribe behavior like in C# via `+=` if you want so 

## Creating and using Observable objects

Observable variables initialization, including collections

```python 
from magique.declarative import obs, Observable
from magique.declarative import odict, olist, ObservableDict, ObservableList

obs_int = Observable(5)
obs_int2 = obs(42)  # creates the same Observable instance
empty_obs = obs()  # default value = None

my_list = ObservableList(range(100))  # accepts any Iterable as input
my_list2 = olist([1, 2, 3])           # creates the same ObservableList
empty_list = olist()                  # without elements

my_dict = ObservableDict({"key": 4567})              # accepts Iterable, Dict, Zip
my_dict2 = odict([("key", "value"), ("what", 42)])   # creates the same ObservableDict
empty_dict = odict()
```

The value in Observable objects is contained in the property `value`

```python
raw_value = obs_int.value
obs_int.value = 71   # updating Observable's value
```

Attach and detach callbacks

```python
from src.magique.declarative import obs

obs_int = obs(25)
callback = lambda value: print(f"upd: {value}")

obs_int.attach_on_update(callback)  # standard way
obs_int += callback                 # alternative C#-like way

obs_int.detach_on_update(callback)  # standard way
obs_int -= callback                 # alternative C#-like way
```

### About wrapping `list` or `dict` or any other mutable objects

The mistake you can get is assigned to lists and dicts. `obs()` wrapped list will invoke subscribed
functions if only the list has been changed (its index updates, appending, removing have no effect)

The `obs()` is suitable for immutable objects. If your object is mutable, there are additional
listeners and wrappers required

For list and dict `magique.declarative` provides wrappers as `ObservableList` and `ObservableDict`
with all basic list and dict methods including iterators, indexes, slicing and
contaning checks same as list and dict

```python
from magique.declarative import obs, olist

list1 = obs([1, 2, 3])
list2 = olist([1, 2, 3])

callback = lambda value: print(f"upd: {value}")
list1.attach_on_update(callback)
list2.attach_on_update(callback)

list1.value.append(4)   # nothing happened, because value not updated directly
list1.append(5)         # raises Error
list1.value = [2, 3]    # upd: [2, 3]

list2.append(4)         # upd: [1, 2, 3, 4]
list2[0] = "hello"      # upd: ["hello", 2, 3, 4]
```

## LoopMetrics and HookMetrics

`LoopMetrics` allows to create an `Observable` object by listening not observable value by loop,
but the loop running in another daemon `Thread`. As result, the loop isn't blocking the invoker

The target metrics functions, which calculates some value is invoked repeatedly by time,
which you can configure in instance constructor or updating the `loop_delay_seconds` field.
Default value = 0.5 seconds

The updated event and its callbacks are invoked if calculated value not equals to the previous
value

```python
from random import randint  
from src.magique.declarative import LoopMetrics, loop_metrics, loop_obs

get_random_number = lambda: randint(100, 999)
print_square =  lambda value: print(value ** 2) 

random_metrics = LoopMetrics(get_random_number, initial_value=100)
random_metrics = loop_obs(get_random_number, initial_value=100)     # creates the same LoopMetrics

random_metrics.attach_on_update(print_square)
random_metrics.start_metrics_loop()


# alternative way to create a metrics via decorator
# but the decorator is breaking the decorators rule
# and instead of function generates LoopMetrics
# instance, but still being Callable

@loop_metrics(initial_value=100, start_immediately=True)
def random_metrics():
    return randint(1000, 9999)

random_metrics.attach_on_update(print_square)
```