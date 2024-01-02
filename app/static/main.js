$.getJSON('plugins', function(data) {
  console.log(data);
  data.forEach((element) => {
    document.getElementById("navbar").innerHTML +='<a href="#'+element+'" id="nav_item_'+element+'" class="p-2 border-2 border-danger sat-plugins" onclick="load_content(\''+element+'\')">'+element+'</a>'
  });
}).done(function () {load_content(window.location.hash.replace("#", ""))});


function load_content(plugin) {
  $.getJSON('plugins/'+plugin, function(data) {
    // console.log(data);
    document.getElementById("sidebar").innerHTML = ''
    data.forEach((element) => {
      document.getElementById("sidebar").innerHTML += '<button onclick="start_feature(\''+plugin+'\', \''+element+'\')" class="btn btn-primary p-2 mt-1" id="feature_button_'+element+'" type="button">'+element+'</button><br>'
    });
    document.getElementById("sidebar").innerHTML += ''
    $("#navbar > .sat-plugins").removeClass("border-bottom")
    $("#nav_item_"+plugin).addClass("border-bottom");
  });

}

function start_feature(plugin, feature) {
  arg1 = document.getElementById('arg1').value
  if (arg1 == ''){
    alert("Please enter something in the input field on top.")
    return;
  }
  document.getElementById("feature_button_"+feature).disabled = true;
  $.getJSON('plugins/'+plugin+'/'+feature+'?data='+arg1, function(data) {
    console.log(data);
    document.getElementById("results").innerHTML = '<code class="language-bash">>>'+plugin+'/'+feature+' '+arg1+'\n'+data['pretty']+'</code>\n\n'+document.getElementById("results").innerHTML
    // document.getElementById("results").scrollTop = document.getElementById("results").scrollHeight;
    hljs.highlightAll();
    document.getElementById("feature_button_"+feature).disabled = false

  }).fail(function() { alert("Error with module "+plugin+"/"+feature); });
}
