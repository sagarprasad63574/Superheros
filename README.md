# Superheros

## Table of Contents
1. [Overview](#Overview)
1. [Navigation](#Navigation)
1. [User Flow](#User-Flow)
2. [Schema](#Schema)

## Overview

### Description
A website to view details about superheroes and add superheroes to a favorites list. The details can be the biography, powerstats, appearance, work, and connections of a superhero. Users are able to create new superheroes and edit information about newly created superheroes. Users are able to add new superheroes created by other users to their favorites list.

### Deployed: https://superheros-app.herokuapp.com/

### Navigation

**Flow Navigation**

* Home 
* Login / Sign up
* Search 
  * View Superheros
  * View details about a superhero
  * Add Superhero to list
* View details about a superhero
  * Show information about superhero(Biography, Powerstats, Appearance, Work, Connections)
* Favorites 
  * View all superheros in list
  * View details about a superhero
  * Delete a superhero
* My superheros
  * Create a new superhero
  * View details about a superhero
  * Delete a superhero in list
* View superheros from other users
  * View superheros created by other users
  * View details about a superhero
  * Add superhero to list
  
### Wireframe
### https://github.com/sagarprasad63574/Superheros/blob/master/static/images/My%20superhero%20list.png

### User-Flow
* Using sessions: if the user is not logged in, redirect to the login page or create an account page. 
If the user is logged in or created an account, direct the user to the search page for searching for a superhero by their name.
* After searching, the user is able to view more information about a superhero by clicking the view button and add a superhero to their favorites list by clicking on the add button. 
* Then the user is redirected to favorites list and can see all of their superheroes. The list will contain superheroe's name, image, view button, and delete button. 
* If the user clicks on the view button, the user will be directed to a page to view more information about the superhero that can be the superheroes powerstats, biography, appearance, work, and connections
* If the user clicked on the edit button, the user will be directed to an edit page where the user will be able to view and edit information about a superheros powerstats, biography, appearance, work, and connections. Then the user is redirected to their favorite’s list. 
* In addition, on the favorites page, there will be another button to add a new superhero. When the user has clicked on the create new superhero button, the user will be directed to a page where the user will be able to add a new superhero to their my superheros list. Then the user is directed to their my superheros list.
* The user is able to view their my superheros list by clicking on the my superheroes button on the nav bar.
* In my superheros list page, the user is able to click on the edit button and delete button to edit and delete a superhero in their list. 
* Lastly if the user clicks on the superheros link on the left side of the nav bar, the user will be redirected to a page to search for a superheros created by other users and the user is able to view details about that superhero and add that superhero to their favorites list. 

### Features
* Search
  * API/Search route is able to search for a superhero name listed in the API
  * favorites/view route is able to search for a superhero name in the user's favorite list
  * mylist/view route is able to search for a superhero name in the user's my superheros list
* Order By
  * favorites/view route is able to search for name and sort by asc/dec by name of superhero 
  * mylist/view route is able to search for name and sort by asc/dec by name of superhero 
  
## 3. Schema 

### Models
#### User

   | Property      | Type     | Description |
   | ------------- | -------- | ------------|
   | id | int | Unique id |
   | first_name | String| Not null |
   | last_name | String | Not null |
   | username | String | Not null and unique |
   | password | String | Not null |
   | image_url | String | Not null |
   
#### Superheros

   | Property      | Type     | Description |
   | ------------- | -------- | ------------|
   | id | Integer | Unique id |
   | user_id | Integer | Reference to User model |
   | superheroinfo_id | Integer | Reference to Superheroinfo model  |
   
#### MySuperheros

   | Property      | Type     | Description |
   | ------------- | -------- | ------------|
   | id | Integer | Unique id |
   | user_id | Integer | Reference to User model |
   | superheroinfo_id | Integer | Reference to Superheroinfo model |
   
#### SuperheroInfo

   | Property      | Type     | Description |
   | ------------- | -------- | ------------|
   | id | Integer | Unique id |
   | superhero_id | String | Unique id |
   | name | String | Not null |
   | image_url | String | Nullable |

#### Powerstats

   | Property      | Type     | Description |
   | ------------- | -------- | ------------|
   | id | Integer | Unique id |
   | superhero_id | Integer | Reference to Superheroinfo model |
   | intelligence | String | Not null |
   | strength | String | Not null |
   | speed | String | Not null |
   | durability | String | Not null |
   | power | String | Not null |
   | combat | String | Not null |

#### Biography

   | Property      | Type     | Description |
   | ------------- | -------- | ------------|
   | id | Integer | Unique id |
   | superhero_id | Integer | Reference to Superheroinfo model |
   | full_name | String | Nullable |
   | place_of_birth | String | Nullable |
   | first_appearance | String | Nullable |
   | alter_egos | String | Nullable |
   | publisher | String | Nullable |

#### Appearance

   | Property      | Type     | Description |
   | ------------- | -------- | ------------|
   | id | Integer | Unique id |
   | superhero_id | Integer | Reference to Superheroinfo model |
   | gender | String | Nullable |
   | race | String | Nullable |
   | height | String | Nullable |
   | weight | String | Nullable |
   | eye_color | String | Nullable |
   | hair_color | String | Nullable |

#### Work

   | Property      | Type     | Description |
   | ------------- | -------- | ------------|
   | id | Integer | Unique id |
   | superhero_id | Integer | Reference to Superheroinfo model |
   | occupation | String | Nullable |
   | base_of_operation | String | Nullable |

#### Connections

   | Property      | Type     | Description |
   | ------------- | -------- | ------------|
   | id | Integer | Unique id |
   | superhero_id | Integer | Reference to Superheroinfo model |
   | group_affiliation | String | Nullable |
   | relatives | String | Nullable |
   
## 4. API
### https://superheroapi.com/?ref=apilist.fun

## 5. Technology Stack
* Python, requests, json, blueprints
* Flask framework
* SQL Alchemy
* Git
* Heroku

