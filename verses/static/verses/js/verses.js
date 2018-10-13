/* =====================================
beat-player
======================================*/

$(function(){
  var beats_list = document.getElementById('beats-list');
  var player = document.getElementById('beat-player');
  beats_list.addEventListener('change', function() {
    var selected_beat = beats_list.selectedIndex;
    if (selected_beat > 1) { //if it's 0 or 1, user selects nothing
      var beat_url = beats_list[selected_beat].value;
      $(player).removeAttr('src');
      $(player).attr('src', beat_url);
      player.play();
    }
  });
});
