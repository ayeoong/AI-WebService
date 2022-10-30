function toggleVisibility(cb)
{
  var x = document.querySelectorAll("#selected"); 
  b = document.getElementById("save_button");
  b.disabled = !(x[0].checked || x[1].checked) ;
} 