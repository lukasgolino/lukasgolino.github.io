<html lang="en">
<head>
<title>CSS Template</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script type="text/javascript" src="script/libs.min.js"></script>
<script type="text/javascript" src="script/Config.js"></script>
<script type="text/javascript" src="script/Piece.js"?></script>
<style>
* {
  box-sizing: border-box;
}

body {
  font-family: Arial, Helvetica, sans-serif;
}

/* Style the header */
header {
  padding: 30px;
  text-align: center;
  font-size: 35px;
  color: white;
}

/* Container for flexboxes */
section {
  display: -webkit-flex;
  display: flex;
}


aside {
  -webkit-flex: 1;
  -ms-flex: 1;
  flex: 1;
  padding: 20px;
}


/* Style the list inside the menu */
nav ul {
  list-style-type: none;
  padding: 0;
}

/* Style the content */
article {
  -webkit-flex: 3;
  -ms-flex: 3;
  flex: 3;
  padding: 10px;
}

/* Style the footer */
footer {
  padding: 10px;
  text-align: center;
  color: white;
}

/* Responsive layout - makes the menu and the content (inside the section) sit on top of each other instead of next to each other */
@media (max-width: 600px) {
  section {
    -webkit-flex-direction: column;
    flex-direction: column;
  }
}
</style>
</head>
<body onload="init('myCanvas', Piece, Config);">



<canvas id="myCanvas" style="position:absolute;z-index:2;left:0;top:0;" resize="false" width="150" height="100"</canvas>
<section>
	
<article>
	<h1>London</h1>
	<p>London is the capital city of England. It is the most populous city in the  United Kingdom, with a metropolitan area of over 13 million inhabitants.</p>
	<p>Standing on the River Thames, London has been a major settlement for two millennia, its history going back to its founding by the Romans, who named it Londinium.</p>
</article>
	
<aside>
	<ul>
		<li><a href="#">London</a></li>
		<li><a href="#">Paris</a></li>
		<li><a href="#">Tokyo</a></li>
	</ul>
</aside>
  
</section>



</body>
</html>
