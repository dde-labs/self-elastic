# Query

A query mapping examples.

```text

```

```json
{
    "filtered": {
       "query": {
          "match_all": {}
       },
       "filter": {
          "bool": {
             "must": { ....... Cond 1 },
             "should": { ....... Cond 2 }
          }
       }
    }
}
```

```text
Cond 1 or Cond 2
```

```json
{
    "bool": {
         "should": [   // OR
            { ...... Cond 1 },
            { ...... Cond 2 }
         ]
    }
}
```