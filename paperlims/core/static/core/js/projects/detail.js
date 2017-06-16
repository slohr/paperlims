  function unlock() {
    var csrftoken = Cookie.get('csrftoken');

    $.ajax({
        url: Urls.project_unlock(object.id),
        type: 'POST',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(result) {
          location.reload();
        },
        error: function(xhr,status,result) {
            alert(xhr.responseText);
        }

    });
  }

  function lock() {
    var csrftoken = $.cookie('csrftoken');

    $.ajax({
        url: Urls.project.lock(object.id),
        type: 'POST',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(result) {
          location.reload();
        },
        error: function(xhr,status,result) {
            alert(xhr.responseText);
        }

    });
  }



$(document).ready(function () {

  build_experiment_actions = function() {
    var action_container = $('<div>');
    action_container.addClass('btn-group')

    var action_button = $('<button data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">');
    action_button.addClass('btn btn-default dropdown-toggle');
    action_button.text('Action ');
    action_button.append(
        $('<span>').addClass('caret')
    );

    var action_list = $('<ul>');
    action_list.addClass('dropdown-menu');

    action_list.append($('<li>').html('<span class="view pointer column-action" data-toggle="tooltip" title="View Experiment">&nbsp;<i class="glyphicon glyphicon-eye-open"></i>&nbsp;View</span>'));


    action_list.append($('<li role="separator">').addClass('divider'));
    action_list.append($('<li>').html('<span class="delete pointer column-action" data-toggle="tooltip" title="Delete Experiment">&nbsp;<i class="glyphicon glyphicon-remove"></i>&nbsp;Delete</span>'));


    action_container.append(action_button).append(action_list);

    //wrap in a throw-away div to get the actual html of interest
    //maybe do this instead now action_container.prop('outerHTML');
    return $('<div>').append(action_container.clone()).html();

  }

  build_project_analysis_actions = function() {
    var action_container = $('<div>');
    action_container.addClass('btn-group')

    var action_button = $('<button data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">');
    action_button.addClass('btn btn-default dropdown-toggle');
    action_button.text('Action ');
    action_button.append(
        $('<span>').addClass('caret')
    );

    var action_list = $('<ul>');
    action_list.addClass('dropdown-menu');

    action_list.append($('<li>').html('<span class="view pointer column-action" data-toggle="tooltip" title="View Analysis">&nbsp;<i class="glyphicon glyphicon-eye-open"></i>&nbsp;View</span>'));


    action_list.append($('<li role="separator">').addClass('divider'));
    action_list.append($('<li>').html('<span class="delete pointer column-action" data-toggle="tooltip" title="Delete Analysis">&nbsp;<i class="glyphicon glyphicon-remove"></i>&nbsp;Delete</span>'));


    action_container.append(action_button).append(action_list);

    //wrap in a throw-away div to get the actual html of interest
    //maybe do this instead now action_container.prop('outerHTML');
    return $('<div>').append(action_container.clone()).html();

  }


});
