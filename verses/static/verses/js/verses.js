/* =====================================
Like Button Ajax
======================================*/

// getelementbyid.innnertext can change the text
// do it dynamically


function updateText(btn, id, newCount){
  btn.removeAttr("data-likes")
  console.log("data-likes removed.")
  btn.attr("data-likes", newCount)
  console.log("data-likes added again, value is : " + btn.attr("data-likes"))
  document.getElementById(id).innerText = newCount
}

$('.like-btn').click(function(e){
  e.preventDefault()
  var likeUrl = $(this).attr("data-href")
  var likeCount = parseInt($(this).attr("data-likes"))
  $.ajax({
    url: likeUrl,
    method: "GET",
    data: {},
    success: function(data){
      if (data.liked){
        likeCount = likeCount + 1
        updateText($('.like-btn'), 'like-text', likeCount)
        console.log("data-likes: " + $('.like-btn').attr("data-likes"))
      } else {
        likeCount = likeCount - 1
        updateText($('.like-btn'), 'like-text', likeCount)
        console.log("data-likes: " + $('.like-btn').attr("data-likes"))
      }
      console.log('ajax ends')
    }, error: function(error){
      console.log(error)
      console.log("error")
    }
  })
})



/* =====================================
 Infinite Scroll
======================================*/
var infinite = new Waypoint.Infinite({
  element: $('.infinite-container')[0],
  onBeforePageLoad: function () {
    $('.loading').show();
  },
  onAfterPageLoad: function ($items) {
    $('.loading').hide();
  }
});
