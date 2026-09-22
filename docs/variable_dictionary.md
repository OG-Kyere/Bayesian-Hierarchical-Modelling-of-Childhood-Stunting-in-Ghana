# Variable dictionary

This file documents the principal variables currently used in the thesis workflow. It is intended to make the public code interpretable without redistributing DHS microdata.

| Construct | DHS variable | Operationalization in this project |
|---|---|---|
| Slept in household previous night | `hv103` | Restrict to `yes` to reproduce the DHS de facto anthropometry population |
| Child age | `hc1` | Restrict to 0–59 months; categories 0–5, 6–11, 12–23, 24–35, 36–47, 48–59 |
| Height-for-age z-score | `hc70` | DHS value divided conceptually by 100; valid range -600 to 600 |
| Stunting outcome | derived from `hc70` | 1 if `hc70 < -200`, otherwise 0 |
| Survey weight | `hv005` | Rescaled as `hv005 / 1,000,000` for descriptive estimates |
| Community / PSU | `hv001` | Community random-intercept identifier |
| Household | `hv001 + hv002` | Unique household identifier nested within community |
| Child sex | `hv104` | Female / male |
| Residence | `hv025` | Urban / rural |
| Region | `hv024` | 16 administrative regions |
| Household wealth | `hv270` | DHS wealth quintiles |
| Drinking-water source | `hv201` | Grouped into improved vs unimproved source type for the current descriptive WASH analysis |
| Toilet facility | `hv205` | Grouped into improved vs unimproved/no facility type for the current descriptive WASH analysis |
| Maternal education | `hc61` | No education, primary, secondary, higher; missing retained explicitly in descriptive output |
| Detailed maternal schooling | `hc68` | Retained for checking/possible sensitivity coding |

## WASH grouping used for current descriptive figures

### Improved drinking-water source

Current coding includes piped sources, public tap/standpipe, tube well or borehole, protected well, protected spring, rainwater, tanker truck, cart with small tank, bottled water, and sachet water.

### Unimproved drinking-water source

Current coding includes unprotected well, unprotected spring, and surface-water sources.

### Improved sanitation

Current coding includes flush to piped sewer, septic tank or pit latrine; bio-digester; ventilated improved pit latrine; pit latrine with slab; and composting toilet.

### Unimproved/no sanitation

All remaining sanitation categories are currently grouped as unimproved/no facility.

These groupings follow JMP source/facility-type definitions. They do not by themselves identify basic or safely managed services, which require additional information such as collection time, sharing, availability, management, or water quality. The inferential WASH model will retain this distinction.
