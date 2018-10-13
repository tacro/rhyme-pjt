/* =====================================
beat-player
======================================*/
$(function(){
  var beats_list = document.getElementById('beats-list');
  var player = document.getElementById('beat-player');
  beats_list.addEventListener('change', function() {
    var selected_index = beats_list.selectedIndex;
    player.pause();
    $(player).removeAttr('src');
    if (selected_index > 1) { //if it's 0 or 1, user selects nothing
      var beat = beats_list[selected_index]
      var beat_url = $(beat).attr('trackUrl');
      console.log(beat_url);
      $(player).attr('src', beat_url);
      player.play();
    }
  });
});
