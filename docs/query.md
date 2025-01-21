# Query

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