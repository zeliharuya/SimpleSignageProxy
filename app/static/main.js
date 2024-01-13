$.getJSON('plugins', function(data) {
  console.log(data);
  data.forEach((element) => {
    document.getElementById("navbar").innerHTML +='<a href="#'+element+'" id="nav_item_'+element+'" class="p-2 border-2 border-danger sat-plugins" onclick="load_content(\''+element+'\')">'+element+'</a>'
  });
}).done(function () {load_content(window.location.hash.replace("#", ""));});


function load_content(plugin) {
  $.getJSON('plugins/'+plugin, function(data) {
    // console.log(data);
    document.getElementById("sidebar").innerHTML = ''
    data.forEach((element) => {
      document.getElementById("sidebar").innerHTML += '<button onclick="start_feature_read(\''+plugin+'\', \''+element+'\',\'\')" class="btn btn-primary p-2 mt-1" id="feature_button_'+element+'" type="button">'+element+'</button><br>'
    });
    document.getElementById("sidebar").innerHTML += ''
    $("#navbar > .sat-plugins").removeClass("border-bottom")
    $("#nav_item_"+plugin).addClass("border-bottom");
    start_feature_read(plugin, data[0],'')
  });

}

function start_feature_read(plugin, feature, id) {
  document.getElementById("feature_button_"+feature).disabled = true;
  $.getJSON('plugins/'+plugin+'/'+feature+'?id='+id, function(data) {
    if ("text" in data){
      document.getElementById("results").innerHTML = data['text']
    }

    if ("table" in data){
      if (data['table'] == false){
       tablecode = '<div class="input-group mt-2"><input type="text" class="form-control" placeholder="New ID" aria-label="data" aria-describedby="arg1-button" id="arg1"><button class="btn btn-outline-secondary" type="button" id="new_button" onclick="start_feature_create(\''+plugin+'\', \''+feature+'\', document.getElementById(\'arg1\').value)">NEW</button></div>'
       document.getElementById("results").innerHTML = tablecode
      }
      else {
        tablecode = '<table class="table"><thead><tr>'
        Object.keys(data['table'][0]).forEach((element) => tablecode+='<th scope="col">'+element+'</th>');
        tablecode += '<th></th><th></th></tr></thead><tbody>'
        data['table'].forEach((element) => tablecode+='<tr><td>'+Object.values(element).join('</td><td>')+'</td><td><a onclick="start_feature_read(\''+plugin+'\', \''+feature+'\', \''+element['id']+'\')">Edit</a></td><td><a onclick="start_feature_delete(\''+plugin+'\', \''+feature+'\', \''+element['id']+'\')">Delete</a></td></tr>');
        // tablecode+='<tr><td>NEW</td>';
        // Object.keys(data['table'][0]).forEach((element) => tablecode+='<td></td>');
        // tablecode += '<td></td></tr>'
        tablecode += '</tbody></table>'
        tablecode += '<br><div class="input-group mt-2"><input type="text" class="form-control" placeholder="New ID" aria-label="data" aria-describedby="arg1-button" id="arg1"><button class="btn btn-outline-secondary" type="button" id="new_button" onclick="start_feature_create(\''+plugin+'\', \''+feature+'\', document.getElementById(\'arg1\').value)">NEW</button></div>'
        document.getElementById("results").innerHTML = tablecode
      }
    }

    if ("form" in data){
      formcode = '<form id="form" onsubmit="return false;">'
      Object.keys(data['form']).forEach((element) => formcode+='<div class="mb-3"><label for="form_'+element+'" class="form-label">'+element+'</label><input type="text" class="form-control" name="'+element+'" id="form_'+element+'" '+((element=='id')?('readonly'):(''))+'></div>');

      formcode += '<div class="mb-3"><button type="submit" class="btn btn-primary" onclick="start_feature_update(\''+plugin+'\', \''+feature+'\', $(\'#form\').serialize());start_feature_read(\''+plugin+'\', \''+feature+'\',\'\')">Save</button></div>'
      formcode += '</form>'

      document.getElementById("results").innerHTML = formcode

      Object.values(data['form']).forEach(function callback(value, index) {
        $('#form_'+Object.keys(data['form'])[index]).val(value);
      });



    }


    // document.getElementById("results").innerHTML = '<code class="language-bash">>>'+plugin+'/'+feature+' '+arg1+'\n'+data['pretty']+'</code>\n\n'+document.getElementById("results").innerHTML
    // document.getElementById("results").scrollTop = document.getElementById("results").scrollHeight;
    document.getElementById("feature_button_"+feature).disabled = false

  }).fail(function() { alert("Error with module "+plugin+"/"+feature); });
}

function start_feature_delete(plugin, feature, id) {
  $.ajax({
   url: 'plugins/'+plugin+'/'+feature+'?id='+id,
   type: 'DELETE',
   success: function(response) {
    start_feature_read(plugin, feature, '')
   }
  });
}

function start_feature_update(plugin, feature, element_data) {
  console.log("updated: "+element_data)
  // element_data = ""
  // Object.values(element).forEach(function callback(value, index) {
    // element_data+=`${Object.keys(element)[index]}=${encodeURI(value)}&`;
  // });
  // Accept serialized element data!
  $.ajax({
   url: 'plugins/'+plugin+'/'+feature+'?'+element_data,
   type: 'PUT',
   success: function(response) {
    start_feature_read(plugin, feature, '')
   }
  });
}

function start_feature_create(plugin, feature, id) {
  $.post( 'plugins/'+plugin+'/'+feature+'?id='+id )
  .done(function( data ) {
    start_feature_read(plugin, feature, '')
  });
  console.log("created: "+id)
}

