# date-range-cli
A cli tool that iterates through a range of dates

Get a range of dates:
```sh
daterange -s 2020-01-01 -e 2020-01-05
2020-01-01 2020-01-02 2020-01-03 2020-01-04 2020-01-05
```

How to install:

```sh
pip install date-range-cli==0.0.3
```

### Todos

 - Support hours instead of just days
 - Need to add granularity (hr vs day) to iterate on a single hour from day to day
