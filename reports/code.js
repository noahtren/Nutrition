var p = document.getElementById('parent');
p.onmouseover = function() {
  document.getElementById('popup').style.display = 'block';
}
p.onmouseout = function() {
  document.getElementById('popup').style.display = 'none';
}