function Logger(){    var self = this;}Logger.prototype.printErrorMessage = function(message){    $("#error_message").text("Error message: "+message).fadeIn(1000);    setTimeout(function(){        $("#error_message").fadeOut(2000);    },3000);}