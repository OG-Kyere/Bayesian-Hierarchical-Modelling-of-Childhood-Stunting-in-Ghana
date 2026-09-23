# Variable dictionary

This note maps the main research variables to their DHS source fields. It is here so the code can be understood without making the restricted DHS microdata public.

| Construct | DHS variable | How it is used |
|---|---|---|
| Slept in household previous night | `hv103` | Restrict to `yes` to reproduce the de facto anthropometry population |
| Child age | `hc1` | Restrict to 0–59 months; primary model uses 0–5, 6–11, 12–23, 24–35, 36–47, 48–59 month groups |
| Height-for-age z-score | `hc70` | DHS stores HAZ multiplied by 100; valid range -600 to 600 |
| Stunting | derived from `hc70` | 1 when `hc70 < -200`; 0 otherwise |
| Survey weight | `hv005` | Divide by 1,000,000 for descriptive estimates |
| Community / cluster | `hv001` | Community random-intercept identifier |
| Household | `hv001 + hv002` | Household identifier nested within community |
| Child sex | `hv104` | Female / male |
| Residence | `hv025` | Urban / rural |
| Region | `hv024` | 16 administrative regions |
| Household wealth | `hv270` | DHS wealth quintiles |
| Drinking-water source | `hv201` | Primary model: improved vs unimproved source type |
| Sanitation facility | `hv205` | Primary model: improved vs unimproved/no facility type |
| Maternal education | `hc61` | No education, primary, secondary, higher |
| Detailed maternal schooling | `hc68` | Retained for checking and possible extensions |
| Design PSU | `hv021` | Used for Taylor-linearized descriptive SEs |
| Design stratum | `hv022` | Used for Taylor-linearized descriptive SEs |

## WASH coding

### Improved drinking-water source

The primary coding treats the following as improved source types: piped water, public tap/standpipe, tube well or borehole, protected well, protected spring, rainwater, tanker truck, cart with small tank, bottled water, and sachet water.

### Unimproved drinking-water source

Unprotected wells, unprotected springs, and surface-water sources are grouped as unimproved in the primary model.

A separate sensitivity analysis splits the unimproved group into **unprotected groundwater** and **surface water**. The surface-water category shows the clearest association with stunting in that analysis.

### Improved sanitation

The improved facility group includes flush to piped sewer, septic tank or pit latrine; bio-digester; ventilated improved pit latrine; pit latrine with slab; and composting toilet.

### Unimproved/no sanitation

All remaining categories are grouped as unimproved/no facility in the primary model. A sensitivity analysis separates open defecation from other unimproved sanitation.

These are source/facility-type groupings. They should not be described as complete JMP basic or safely managed service levels because the DHS variables used here do not establish all required service-level conditions such as sharing, collection time, availability, safe management, or water quality.
