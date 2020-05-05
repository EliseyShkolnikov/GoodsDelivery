jQuery(function(){
          $("#Top").hide().removeAttr("href");
          if ($(window).scrollTop()>="200") $("#Top").fadeIn("slow")
          $(window).scroll(function(){
          if ($(window).scrollTop()<="200") $("#Top").fadeOut("slow")
          else $("#Top").fadeIn("slow")
          });
        
          $("#Bottom").hide().removeAttr("href");
          if ($(window).scrollTop()<=$(document).height()-"999") $("#Bottom").fadeIn("slow")
          $(window).scroll(function(){
          if ($(window).scrollTop()>=$(document).height()-"999") $("#Bottom").fadeOut("slow")
          else $("#Bottom").fadeIn("slow")
          });
        
          $("#Top").click(function(){
          $("html, body").animate({scrollTop:0},"slow")
          })
          $("#Bottom").click(function(){
          $("html, body").animate({scrollTop:$(document).height()},"slow")
          })
        });