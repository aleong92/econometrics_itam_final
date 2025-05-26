# Econometrics Workshop II
## ITAM

This repo is the final project of the course. **The goal is to succesfully extract data from INEGI's API and aggregate it into a single, usable dataframe.**

### What does this repo do?

Basically, it provides the user with a script to extract data from INEGI's API (this is México's official statistics and numbers government agency).

**I'll be tapping into the DNUE (a national directory of commercial establishments) to look, based on a set of coordinates, all restaurants found in a 0-5000 meter radius.**

INEGI's API search structure requires:

* A set of coordinates (Latitude, Longitude). I focus mainly on **three places**:
   1. **Polanco**, in Mexico City
   2. **Colonia Americana**, in Guadalajara 
   3. **San Pedro**, in Monterrey  
* A keyword. I selected **restaurants**
* A radius. I set it to **3.5km.**
* A personal token. Generate yours at [INEGI's API](https://www.inegi.org.mx/servicios/api_denue.html).

The call structure is simple:

```
https://www.inegi.org.mx/app/api/denue/v1/consulta/Buscar/{KEYWORD}/{LATITUDE},{LONGITUDE}/{RADIUS}/{YOUR TOKEN}
```

And the response is also fairly straightforward:

![Respuesta](https://www.inegi.org.mx/servicios/img/Buscar.png)


All fields are basically descriptive fields related to address, capacity and location. For further reference, visit [INEGI's site](https://www.inegi.org.mx/servicios/api_denue.html)

If you choose to execute the script in the **code** folder, you'll get a single dataframe, ready to be worked with, containing the data for each call made. This dataframe includes the following columns:

1. INEGI's id.
2. Restaurant id.
3. Restaurant name.
4. Restaurant capacity.
5. Street name.
6. Exterior number.
7. Interior number.
8. Longitude.
9. Latitude.
10. City

### What does this repo contain?

Well, here's the repo structure:

```
econometrics_itam_final/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── code/                  
│   └── inegi_data_extraction.py        
│
└── data/                  
    └── inegi_data_rest.csv          
```
