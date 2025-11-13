# HEPData-link

`analyses.json` file includes the list of all the analyses recasted in MadAnalysis and enables the correct links in HEPData. The analyses format is constructed as follows;

```
{
    "inspire_id": "<INSPIRE HEP ID to the paper>",
    "implementations": [
        {
            "name": "<TITLE of the recast>",
            "path": "<DOI link to the recast>"
        }
    ]
}
```
