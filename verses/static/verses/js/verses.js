/* =====================================
  Like Button Ajax
======================================*/

function updateText(btn, newCount, verb){
  btn.text(newCount + " " + verb)
}

$('.like-btn').click(function(e){
  e.preventDefault()
  var likeUrl = $(this).attr("data-href")
  var likeCount = $(this).attr("data-likes")
  var addLike = likeCount + 1
  var removeLike = likeCount - 1
  $.ajax({
    url: likeUrl,
    method: "GET",
    data: {},
    success: function(data){
      console.log(data)
      var newLikes;
      if (data.liked){
        updateText($(this), addLike, "Unlike")
      } else {
        updateText($(this), removeLike, "Like")
      }
    }, error: function(error){
      console.log(error)
      console.log("error")
    }
  })
})
