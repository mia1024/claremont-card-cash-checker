# Completely Convoluted Claremont Card Cash Checker (CCCCCC)



## Sanity check

First, check that you can actually log in to the website by going to [here](https://cards.services.claremont.edu/index.php?cid=35) and log in. If you can't, figure out how before proceeding. Note that this website doesn't use your normal school email + password combination. 

## Run

Download or clone this repository. Install dependency by running 

```bash
python3 -m pip install requests
```

Then, **edit** `check.py` and replace the first 2 lines with your student id and password (the one you get from email). 

Finally, run the script by 
```bash
python3 check.py
```

## Sample Output
```
Flex: $2.50
Claremont Cash: $26.50
Swipes: 4
```
