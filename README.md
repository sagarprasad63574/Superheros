# Superheros

## Schema 

### Models
#### User

   | Property      | Type     | Description |
   | ------------- | -------- | ------------|
   | userID     | int   | unique id for the user  |
   | username       | String| unique username created by user |
   | password         | String     | used for authentication |
 

   
#### Flight

   | Property      | Type     | Description |
   | ------------- | -------- | ------------|
   | id      | int   | unique id for the flight |
   | minPrice        | String| minimum price that flight has been found |
   | carrier      | String  | airline  |
   | placeDep     | Place | take off location |
   | currency     | String | date when event is taking place|
   |placeDist| Place | destination of flight|
   
#### Place

   | Property      | Type     | Description |
   | ------------- | -------- | ------------|
   | id      | int   | unique id for the place|
   | stringId        | String| unique id for place |
   | airportName      | String  | name of airport |
   | cityyName     | String | name of city airport is located in |
   | countryName     | String | name of country is located in |
   
