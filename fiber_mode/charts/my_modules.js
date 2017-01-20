angular.module('Coder', ['myAppControllers', 'myAppServices'] );

angular.module('myAppControllers', [])
	.controller('codeController',
				['$scope',
				 'srvInfo',
				 function ($scope, srvInfo) {
					$scope.decode = function(data) {//run decoder
						var RE = /^[a-z|A-Z]*$/;
							if(document.getElementById('text_to_decode').value.match(RE)){
								srvInfo.getDecoded(
								function(data) {
									$scope.decoder_result = data;
								});
								document.getElementById('text_to_decode').style='background-color:white;';
								document.getElementById('text_error').style='display:none;';
							}else{
								document.getElementById('text_error').style='display:inline;';
								document.getElementById('text_to_decode').style='background-color:#ffa1a1;';
								document.getElementById('text_error').innerHTML="Put english chars only";
							}
					};
				 }]);

// communication with the server
angular.module('myAppServices', [])
    .service('srvInfo',
             function($http) {
                 this.Decode = function(callback) {
                     return $http.get('/ajax/test_js_plot/?text='+document.getElementById('text_to_decode').value+'&input_key='+document.getElementById('input_key').value).success(callback);
                 };
                 
             });

const mydiv = document.querySelector('myPlot')
console.log(mydiv)