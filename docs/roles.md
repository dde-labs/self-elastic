# Roles

```json
{
  "ai-chatbot-role": {
    "cluster": [
      "monitor",
      "manage_connector"
    ],
    "indices": [
      {
        "names": [
          "ai-data-*"
        ],
        "privileges": [
          "all"
        ],
        "allow_restricted_indices": false
      }
    ],
    "applications": [],
    "run_as": [],
    "metadata": {},
    "transient_metadata": {
      "enabled": true
    }
  }
}
```
