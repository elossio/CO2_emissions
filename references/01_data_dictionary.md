# Data Dictionary

Dataset retrieved from the [Canadian government
website](https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64).

Details about the terminologies are available
[here](https://natural-resources.canada.ca/energy-efficiency/transportation-alternative-fuels/personal-vehicles/choosing-right-vehicle/buying-electric-vehicle/understanding-the-tables/21383)
and summarized below.

The datasets provide model-specific fuel consumption ratings and estimated carbon dioxide
emissions for new light-duty vehicles available for retail sale in Canada.

| Column Name            | Description                                                                                       | Data Type   |
|------------------------|---------------------------------------------------------------------------------------------------|-------------|
| `Model year`           | Model year                                                                                        | Numeric     |
| `Make`                 | Manufacturer                                                                                      | Categorical |
| `Model`                | Model (see below)                                                                                 | Categorical |
| `Vehicle class`        | Vehicle class (see below)                                                                         | Categorical |
| `Engine size (L)`      | Engine displacement in litres                                                                     | Numeric     |
| `Cylinders`            | Number of cylinders                                                                               | Numeric     |
| `Transmission`         | Transmission type (see below)                                                                     | Categorical |
| `Fuel type`            | Fuel type (see below)                                                                             | Categorical |
| `City (L/100km)`       | Fuel consumption in L/100 km in city driving                                                      | Numeric     |
| `Highway (L/100km)`    | Fuel consumption in L/100 km on highways                                                          | Numeric     |
| `Combined (L/100km)`   | Fuel consumption in L/100 km considering 55% city driving and 45% highway driving                 | Numeric     |
| `Combined (mpg)`       | Combined fuel consumption in miles per gallon                                                     | Numeric     |
| `CO2 emissions (g/km)` | CO2 emissions in g/km for combined driving                                                        | Numeric     |
| `CO2 rating`           | CO2 emission rating scale                                                                         | Categorical |
| `Smog rating`          | Smog pollutant emission rating scale                                                              | Categorical |

## Details for the `Model` column

- AWD = All-wheel drive — vehicle designed to operate with all wheels driven
- 4WD / 4X4 = Four-wheel drive — vehicle designed to operate with either two or four wheels driven
- FFV = Flexible-fuel vehicle — vehicle designed to run on gasoline and ethanol blends of up to 85% ethanol (E85)
- CNG = Compressed natural gas; NGV = Natural gas vehicle
- SWB = Short wheelbase; LWB = Long wheelbase; EWB = Extended wheelbase; # = High-output engine

## Details for the `Vehicle class` column

For cars:

| Vehicle class                        | Interior volume                          |
|--------------------------------------|------------------------------------------|
| Two-seater (T)                       | n/a                                      |
| Minicompact (I)                      | Less than 2,405 L (85 cu. ft.)           |
| Subcompact (S)                       | 2,405–2,830 L (85–99 cu. ft.)            |
| Compact (C)                          | 2,830–3,115 L (100–109 cu. ft.)          |
| Mid-size (M)                         | 3,115–3,400 L (110–119 cu. ft.)          |
| Full-size (L)                        | 3,400 L (120 cu. ft.) or more            |
| Station wagon: Small (WS)            | Less than 3,680 L (130 cu. ft.)          |
| Station wagon: Mid-size (WM)         | 3,680–4,530 L (130–159 cu. ft.)          |

Where L = litres and cu. ft. = cubic feet.

For pickup trucks, trucks, and vans:

| Vehicle class                        | Gross vehicle weight                     |
|--------------------------------------|------------------------------------------|
| Pickup truck: Small (PS)             | Less than 2,722 kg (6,000 lb)            |
| Pickup truck: Standard (PL)          | 2,722–3,856 kg (6,000–8,500 lb)          |
| Sport utility vehicle: Small (US)    | Less than 2,722 kg (6,000 lb)            |
| Sport utility vehicle: Standard (UL) | 2,722–4,536 kg (6,000–9,999 lb)          |
| Minivan (V)                          | Less than 3,856 kg (8,500 lb)            |
| Van: Cargo (VC)                      | Less than 3,856 kg (8,500 lb)            |
| Van: Passenger (VP)                  | Less than 4,536 kg (10,000 lb)           |
| Special purpose vehicle (SP)         | Less than 3,856 kg (8,500 lb)            |

Where kg = kilograms and lb = pounds.

## Details for the `Transmission` column

- A = Automatic
- AM = Automated manual
- AS = Automatic with select shift
- AV = Continuously variable
- M = Manual
- Number of gears/speeds (1–10)

## Details for the `Fuel type` column

- X = Regular gasoline
- Z = Premium gasoline
- D = Diesel
- E = E85 (ethanol and gasoline blend with up to 85% ethanol)
- B = Electricity
- N = Natural gas
