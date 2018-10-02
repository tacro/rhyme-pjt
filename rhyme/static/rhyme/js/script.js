/* =====================================
Like Button Ajax
======================================*/

// getelementbyid.innnertext can change the text
// do it dynamically


function updateText(btn, id, newCount){
  btn.removeAttr("data-likes")
  // console.log("data-likes removed.")
  btn.attr("data-likes", newCount)
  // console.log("data-likes added again, value is : " + btn.attr("data-likes"))
  document.getElementById(id).innerText = newCount
}

$('.like-btn').click(function(e){
  e.preventDefault()
  var likeUrl = $(this).attr("data-href")
  var id = 'like-text-' + $(this).attr("verse-id")
  // console.log("likeurl : " + likeUrl)
  var likeCount = parseInt($(this).attr("data-likes"))
  $.ajax({
    url: likeUrl,
    method: "GET",
    data: {},
    success: function(data){
      if (data.liked){
        likeCount = likeCount + 1
        updateText($('.like-btn'), id, likeCount)
        // console.log("data-likes: " + $('.like-btn').attr("data-likes"))
      } else {
        likeCount = likeCount - 1
        updateText($('.like-btn'), id, likeCount)
        // console.log("data-likes: " + $('.like-btn').attr("data-likes"))
      }
      // console.log('ajax ends')
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

/* =====================================
 Pull to refresh
======================================*/

function pullRefresh(elem, pageUrl){
  PullToRefresh.init({
    mainElement: elem,
    onRefresh: function(){
      // indexUrl = "/verses/index"
      // console.log(indexUrl)
      $.ajax({
        url: pageUrl,
        method: 'GET',
        success: function(){
          // console.log(indexUrl);
          window.location.reload(false);
        },
        error: function(error){
          console.log(error);
        }
      })
      var promise = new Promise(
        function(resolve, reject){
          setTimeout(()=>{
            resolve();
          }, 1000);
        }
      );
      return promise;
    }
  });
}
