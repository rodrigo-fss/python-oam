# Python-OAM
![master CI](https://github.com/rodrigo-fss/python-oam/actions/workflows/github-actions.yml/badge.svg)
![coverage](https://github.com/rodrigo-fss/python-oam/blob/main/.github/badges/coverage_badge.svg)

### OAM toolbox made by the community to the community

Outlier detection has been used to detect and, if appropriate, remove anomalous observati-
ons from the data. It’s usability can identify system failures and frauds before they escalate
with potentially huge consequences.

One ramification of the contribution made by the outlier detection field is related
to understand which aspects of the anomalous observation significantly separate it from
the others in a given dataset. This area of research has been
called Outlier Aspect Mining (OAM). Promising results and applications and cases have
been presented by the community.

The objective of this lib is to contribute to OAM research in a practical way. **Python-OAM** allow
you to apply Outlier Aspect Mining algorithms and analyze the results in your own
datasets.

Feel free to not only use it but also extend it as wished.


Installation
---

To see Python-OAM in action on your own data:

You can install it using pip
```
pip install python-oam
```

python-oam is tested with:

|                     | Version (dev)  |
|---------------------|----------------|
| Python              | 3.7, 3.8, 3.9  |
| pandas              | 1.3.2          |
| seaborn             | 0.11.2         |
| tqdm                | 4.62.0         |

What 's OAM?
---
Outlying Aspect Mining (OAM), can be interpreted as "The task of looking for a set of
characteristics (or subspaces) where a given object is different from the rest of the other objects."

Something in the lines of:

> "OK, I know that this object is an outlier, but why exactly?"

**OAM helps you to figure it out!**

Defining the problem in a generic way, we consider a set of data
*X = {x1, x2, ..., xn}* with n observations in a D-dimensional space. The application of
OAM seeks to understand which dimensions of *D* make a sample of *X* to be considered
an outlier.

The existing OAM techniques are classified into three major groups,
*Score and Search* , *Feature Selection* and *Hybrid Approach*.

We mainly focused on the development of a **Score and Search** based toolbox,
so let's talk a little bit more about it

Score and Search
---
The Score and Search is the most researched OAM technique and the one with the greatest results till the moment.

This approach requires a **scoring** function, to measure how much the object differs from the other objects in a
given a set of dimensions (subspace).
The **search** algorithm will define which dimensions should be compared.
Then, the score will be compared across all subspaces generated by the search algorithm to detect the most divergent aspects.

That may have sounded a little too complex so we may break it down into an example

Let's say you have a dataset with different basketball players and their stats for a given season.
We can all agree that Stephen Curry was indeed an outlier in the 2015 season, but among all of
his stats, which one, or which set of stats, made him deliver so much more than the other players?

Was it the number of jumps? or his high number of field goals attempts? maybe the average running speed?

The **scoring** function will evaluate how different he was from the other players in, let's say,
the dimension of "Field Goals Made", in that matter he was one of the greatest at that season so, very different.

the **search** algorithm will combine different dimensions to be evaluated, like
let's come with a score of how different Stephen Curry was in comparison with the other
given his "Number of Jumps" and "Three Points Made". How about "Average Running Speed" and
"Offensive rebound"?

After scoring all the dimensions the search function returned, we compare them all
to get to the most outlier set of dimensions
> and that's a way to explain why Stephen Curry was recognized as an outlier basketball player in 2015 season.

Scoring Functions
---
### Ipath

The iPath (isolation Path) arises from the study published by
[Vinh et al. (2016)](https://link.springer.com/article/10.1007/s10618-016-0453-2).
The authors found that using the iForest anomaly detection approach (isolation
Forest), it is possible to establish a dimensionally unbiased metric. The idea behind scoring the
iPath is that, in the most discrepant subspace, **an anomalous object is easier to isolate than the others.**

The iPath process consists of making cuts in space, isolating objects from the rest
of the dough. In this scenario, if the object is surrounded by several others, you will need to
more cuts to separate it from the rest, while if the object is an outlier, it will take
less cuts. This behavior can be observed in Figure 1, where (a) represents the
procedure of an outlier that was isolated with only three cuts, while (b), a value
not considered an outlier, it needed 7 cuts to be isolated from the rest of the data.

![Image 1](https://i.postimg.cc/3w3Kwd5Q/ipath.png)


Search Functions
---
### Simple Combination

Simple Combinations consists of making all possible combinations of spaces between
a minimum and maximum size. This means that, for example, for a dataset of
*n* dimensions and a minimum and maximum size value equal to *i* and *j* respectively, the Simple
Combination will create all possible combinations without repetition.

Let's say you have a dataset with the followin dimensions
```python
['datetime','ticker','open','close','high','low','volume']
```

if your maximum value is one the Simple Combination algorithm will return:
```python
[['datetime'],['ticker'],['open'],['close'],['high'],['low'],['volume']]
```
if your maximum value is two the Simple Combination algorithm will return:
```python
[['datetime', 'ticker'], ['datetime', 'open'], ['datetime', 'close'], ['datetime', 'high'], ...]
```
This technique allows the user to analyze a large number of dimensions
controlling the combinatorial explosion caused by an all-to-all combination with no size limit.

Architecture
---

- Preprocess: contains a normalization function that allows the user to assign
weights for chosen dimensions;
- Score: contains the iPath class and will contain other score classes in the future;
- Search: contains the SimpleCombination class and will contain other search classes
in the future;
- Visualization: contains some functions to assist in the before and after visualization
application of OAM techniques

Although the implementation separates them into different modules, Score and Search
function as a set. As the scoring algorithm chosen, for the creation of
an instance of iPath requires only two parameters, the size of the generated subsamples
and the number of trees to be generated.

```python
ipath = IsolationPath(
    subsample_size=256,
    number_of_paths=50
)
```

Then SimpleCombination, implemented as a search method, receives the instance of the chosen scoring method,
the parameters that define the size of the generated subspaces and which dimensions will be used.

```python
search = SimpleCombination(
    ipath,
    min_items_per_subspace=2,
    max_items_per_subspace=4,
    dimensions=[
        "variation_mean", "variation_std", "up_count", "down_count",
    ]
)
```

The decision to decouple the Score from the Search, and then reference them in the moment
instance of classes, is linked to the possibility of combining them in different ways.
If a new scoring algorithm is implemented, it will only need to contain one
method called *score*, returning a number, to integrate with *SimpleCombination*.
Likewise, if a new *search* method is implemented, it will only need to
evaluate the dimension through the score method of the class received as a parameter to
integrate with the rest.

You can check a few examples of the lib in use in the ```oam/analysis```folder
and in the ```test/sample_search.py``` as well. Also, the tests should serve you
with some guidance on how to use specific functions - the coverage is pretty good
at the moment.

Tests
---
We recognize our testing strategy is quite simple, many times we just look for
exceptions in the happy path - we'll be glad to accept some help improving this area.

You can run them in your own through
```make test```.
