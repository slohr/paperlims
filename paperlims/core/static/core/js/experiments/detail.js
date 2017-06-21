  function unlock() {
    var csrftoken = Cookie.get('csrftoken');

    $.ajax({
        url: Urls.experiment_unlock(object.id),
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
        url: Urls.experiment.lock(object.id),
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



});
