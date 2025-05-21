# Web page file template
each page of the frontend exists of a html, css and js file.<br>
all html files are made according to the following template:<br>
````html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Blank Page</title>
  <link rel="stylesheet" href="../static/css/home.css" />
</head>
<body>

  <!-- Content goes here -->

  <script src="../static/js/home.js"></script>
</body>
</html>

````

# File structures
the file structure is as follows:<br>

the templates folder had all the html files,<br>
the static folder has the css and js files in their folders as well as all the assets like fonts and images.
![structure.png](structure.png)

## Navigation bar
The navigation bar is made in JavaScript in this way the navbar can be injected into every HTML file where it is needed. 

The call upon the navbar in an HTML file you need to include this code:

```HTML
   <link rel="stylesheet" href="../static/css/navbar.css" />

   <div id="navbar"></div>

   <script src="../static/js/navbar.js"></script>

```
These lines of code will dynamically inject the navbar on page load.