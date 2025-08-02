// Helper Functions
String.prototype.niceify = function() {
  return this.replaceAll('_', ' ').replace(/\b[a-z]/g, function(letter) {
    return letter.toUpperCase();
  });
}

// App Logic
$.getJSON('plugins', function(data) {
  console.log(data);
  document.getElementById("navbar").innerHTML = '<a href="/" class="p-2 border-2 border-danger sat-plugins border-bottom">Home</button>';
  data.forEach((element) => {
    document.getElementById("navbar").innerHTML +='<a href="#'+element+'" id="nav_item_'+element+'" class="p-2 border-2 border-danger sat-plugins" onclick="load_content(\''+element+'\')">'+element.niceify()+'</a>'
  });
}).done(function () {load_content(window.location.hash.replace("#", ""));});

function load_content(plugin) {
  $.getJSON('plugins/'+plugin, function(data) {
    // console.log(data);
    document.getElementById("sidebar").innerHTML = '';
    data.forEach((element) => {
      document.getElementById("sidebar").innerHTML += '<button onclick="start_feature_read(\''+plugin+'\', \''+element+'\',\'\')" class="btn btn-secondary p-2 mt-1" id="feature_button_'+element+'" type="button">'+element.niceify()+'</button><br>'
    });
    document.getElementById("sidebar").innerHTML += '';
    $("#navbar > .sat-plugins").removeClass("border-bottom");
    $("#nav_item_"+plugin).addClass("border-bottom");
    start_feature_read(plugin, data[0],'')
  });

}

function start_feature_read(plugin, feature, id) {
  document.getElementById("feature_button_"+feature).disabled = true;
  $(".btn-primary").addClass("btn-secondary");
  $("#sidebar > .btn").removeClass("btn-primary");

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
        tablecode = '<table class="table"><thead><tr><th></th><th></th>'
        Object.keys(data['table'][0]).forEach((element) => tablecode+='<th scope="col">'+element.niceify()+'</th>');
        tablecode += '</tr></thead><tbody>'
        data['table'].forEach((element) => {
          for(let key in element) {
            if (key.startsWith('base64_')) {
              element[key] = '<img src="data:image/png;base64,' + element[key] + '" style="max-width: 100px; max-height: 100px;">';
            }
          }
          tablecode += '<tr><td><a onclick="start_feature_read(\''+plugin+'\', \''+feature+'\', \''+element['id']+'\')">Edit</a></td><td><a onclick="start_feature_delete(\''+plugin+'\', \''+feature+'\', \''+element['id']+'\')">Delete</a></td><td>'+Object.values(element).join('</td><td>')+'</td></tr>'
        });
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
      Object.keys(data['form']).forEach((element) => {
        let input_elem = '';
        if (element.startsWith('is_')) {
          input_elem = '<select class="form-control" name="'+element+'" id="form_'+element+'"><option value="false">false</option><option value="true">true</option></select>';
        }
        else {
          input_elem = '<input type="text" class="form-control" name="'+element+'" id="form_'+element+'" '+((element=='id')?('readonly'):(''))+'>';
        }

        formcode += '<div class="mb-3"><label for="form_'+element+'" class="form-label">'+element+'</label>'+input_elem+'</div>'
      });

      formcode += '<div class="mb-3"><button type="submit" class="btn btn-primary" onclick="start_feature_update(\''+plugin+'\', \''+feature+'\', $(\'#form\').serialize());start_feature_read(\''+plugin+'\', \''+feature+'\',\'\')">Save</button></div>'
      formcode += '</form>'

      document.getElementById("results").innerHTML = formcode

      Object.entries(data['form']).forEach(function([key, value], index) {        
        if (key.startsWith('is_')) {
          $('#form_' + key).val(value.toString());  // Ensure value is a string
        } else {
          $('#form_' + key).val(value);  // Apply to the key, not the index
        }
      });
    }


    // document.getElementById("results").innerHTML = '<code class="language-bash">>>'+plugin+'/'+feature+' '+arg1+'\n'+data['pretty']+'</code>\n\n'+document.getElementById("results").innerHTML
    // document.getElementById("results").scrollTop = document.getElementById("results").scrollHeight;
    document.getElementById("feature_button_"+feature).disabled = false;
    $("#feature_button_"+feature).addClass("btn-primary");
    $("#feature_button_"+feature).removeClass("btn-secondary");

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

