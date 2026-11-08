# One Nation and immigration attitudes, 1998–2025: AES analysis

Code and aggregate output supporting the essay *One Nation and Immigration, 1998–2025: Why a More Diverse Australia Is Listening* (David le Comte, POIX2010, Macquarie University, November 2026).

## What this repository contains

| File | Purpose |
|---|---|
| `aes_series.py` | Share of voters wanting immigration reduced, by birthplace and House vote, for the AES 1998, 2010, 2019, 2022 and 2025 (Table A1 of the essay). |
| `aes_extra_items.py` | Supplementary items cited in the essay: the 2025 "immigrants increase the cost of housing" item by vote, and the 1998 perception items about Asians. |
| `output_series_1998_2025.csv` / `.txt` | Output of `aes_series.py`. |
| `output_extra_items.txt` | Output of `aes_extra_items.py`. |
| `requirements.txt` | Python packages needed. |

## Data (not included)

The Australian Election Study licence does not permit redistribution of the survey data. Request the Stata (`.dta`) files from the Australian Data Archive:

| Survey | Dataset DOI |
|---|---|
| AES 1998 | https://doi.org/10.4225/87/FFBWUU |
| AES 2010 | https://doi.org/10.4225/87/CYJNSM |
| AES 2019 | https://doi.org/10.26193/KMAMMW |
| AES 2022 | https://doi.org/10.26193/W3U2S3 |
| AES 2025 | https://doi.org/10.26193/A9VEXA |

## Method

- **Attitude:** "Do you think the number of immigrants allowed into Australia nowadays should be reduced or increased?" (five-point scale). "Reduce" = "reduced a little" + "reduced a lot".
- **Vote:** first preference in the House of Representatives.
- **Birthplace:** Australia versus overseas, from the country-of-birth item.
- **Weights:** 1998 unweighted (no weight in the file); 2010 `weight2`; 2019 `wt_pooled`; 2022 `weight`; 2025 `weight`.
- **Validation:** the all-voter figures reproduce the published AES series exactly (48, 52, 49, 30, 53 per cent; Cameron, McAllister and Pietsch 2025, *Trends in Australian Political Opinion*, 134).
- **Caution:** One Nation subsamples are small after 1998 (26 in 2019, 30 in 2022, 37 in 2025).

## How to run

```
pip install -r requirements.txt
python aes_series.py aes1998.dta aes2010.dta aes2019.dta aes2022.dta aes2025.dta output_series_1998_2025.csv
python aes_extra_items.py aes1998.dta aes2025.dta
```

## Acknowledgement

Tabulations were prepared with the assistance of Claude (Anthropic) and checked by the author against the published AES figures.

## Licence

Code released under the MIT Licence.
