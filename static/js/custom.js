// // let autocomplete;



// function initAutoComplete(){
//     var quezon_city = new google.maps.LatLngBounds(
//         new google.maps.LatLng(14.777775, 121.134932),
//         new google.maps.LatLng(14.605136, 120.988440));
// autocomplete = new google.maps.places.Autocomplete(
//     document.getElementById('id_information-address'),
//     {
//         types: ['geocode', 'establishment'],
//         // //default in this app is "IN" - add your country code
//         componentRestrictions: {'country': ['ph']},
//         // bounds: quezon_city,
//     // strictBounds: true,
//     })
// // function to specify what should happen when the prediction is clicked
// autocomplete.addListener('place_changed', onPlaceChanged);
// }

// function onPlaceChanged (){
    
//     var place = autocomplete.getPlace();
    
//     // User did not select the prediction. Reset the input field or alert()
//     if (!place.geometry){
//         document.getElementById('id_information-address').placeholder = "Start typing...";
//     }
//     else{
//         // console.log('place name=>', place.name)
//     }

//     // get the address components and assign them to the fields
//     // console.log(place);
//     var geocoder = new google.maps.Geocoder()
//     var address = document.getElementById('id_information-address').value

//     geocoder.geocode({'address': address}, function(results, status){
//         // console.log('results=>', results)
//         // console.log('status=>', status)
//         if(status == google.maps.GeocoderStatus.OK){
//             var latitude = results[0].geometry.location.lat();
//             var longitude = results[0].geometry.location.lng();

//             // console.log('lat=>', latitude);
//             // console.log('long=>', longitude);
//             $('#id_information-latitude').val(latitude);
//             $('#id_information-longitude').val(longitude);

//             $('#id_information-address').val(address);
//         }
//     });

//     // loop through the address components and assign other address data
//     console.log(place.address_components);
//     for(var i=0; i<place.address_components.length; i++){
//         for(var j=0; j<place.address_components[i].types.length; j++){
//             // get country
//             if(place.address_components[i].types[j] == 'country'){
//                 $('#id_information-country').val(place.address_components[i].long_name);
//             }
//             // get state
//             if(place.address_components[i].types[j] == 'administrative_area_level_1'){
//                 $('#id_information-state').val(place.address_components[i].long_name);
//             }
//             // get city
//             if(place.address_components[i].types[j] == 'locality'){
//                 $('#id_information-city').val(place.address_components[i].long_name);
//             }
//             // get pincode
//             if(place.address_components[i].types[j] == 'postal_code'){
//                 $('#id_information-pin_code').val(place.address_components[i].long_name);
//             }else{
//                 $('#id_information-pin_code').val("");
//             }
//         }
//     }

// }

// var input = document.getElementById('id_information-address');
// var options = {
//     componentRestrictions: {
//         country: 'ph'
//     }
// };

// var autocomplete = new google.maps.places.Autocomplete(input, options);

// $(input).on('input',function(){
// 	var str = input.value;
//   var prefix = 'Quezon City, ';
// 	if(str.indexOf(prefix) == 0) {
// 		console.log(input.value);
// 	} else {
// 		if (prefix.indexOf(str) >= 0) {
//     	input.value = prefix;
//     } else {
//   		input.value = prefix+str;
//    }
// 	}

// });

google.maps.event.addListener(autocomplete, 'place_changed', function () {
    
    var place = autocomplete.getPlace();
    
    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_information-address').placeholder = "Start typing...";
    }
    else{
        // console.log('place name=>', place.name)
    }

    // get the address components and assign them to the fields
    // console.log(place);
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_information-address').value

    geocoder.geocode({'address': address}, function(results, status){
        // console.log('results=>', results)
        // console.log('status=>', status)
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            // console.log('lat=>', latitude);
            // console.log('long=>', longitude);
            $('#id_information-latitude').val(latitude);
            $('#id_information-longitude').val(longitude);

            $('#id_information-address').val(address);
        }
    })

    console.log(place.address_components);
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            // get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_information-country').val(place.address_components[i].long_name);
            }
            // get state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_information-state').val(place.address_components[i].long_name);
            }
            // get city
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_information-city').val(place.address_components[i].long_name);
            }
            // get pincode
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_information-pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_information-pin_code').val("");
            }
        }
    }

});


$("#id_general-accident_factor").change(function () {
    const url = $("#form_incidentgeneral").attr("data-acc-url");  // get the url of the `load_cities` view
    const accidentId = $(this).val();  // get the selected country ID from the HTML input

    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= /persons/ajax/load-cities/ )
        data: {
            'accident_factor_id': accidentId       // add the country id to the GET parameters
        },
        success: function (data) {
            let select_element = $('#id_general-accident_subcategory'); //Sub_category select  
            //console.log(data) // `data` is the return of the `load_cities` view function
            $(select_element).html(data);  // replace the contents of the city input with the data that came from the server

            let html_data = '';
            data.forEach(function (accident_subcategory) {
                html_data += `<option value="${accident_subcategory.id}">${accident_subcategory.sub_category}</option>`
            });
            console.log(html_data);
            $("#id_general-accident_subcategory").html(html_data);

        }
    });

});

$("#id_general-collision_type").change(function () {
    const url = $("#form_incidentgeneral").attr("data-acc-url");  // get the url of the `load_cities` view
    const collisionId = $(this).val();  // get the selected country ID from the HTML input

    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= /persons/ajax/load-cities/ )
        data: {
            'collision_type_id': collisionId       // add the country id to the GET parameters
        },
        success: function (data) {  
            //console.log(data) // `data` is the return of the `load_cities` view function
            $("#id_general-collision_subcategory").html(data);  // replace the contents of the city input with the data that came from the server

            let html_data = '<option value="">---------</option>';
            data.forEach(function (collision_subcategory) {
                html_data += `<option value="${collision_subcategory.id}">${collision_subcategory.sub_category}</option>`
                
            });
            console.log(html_data);
            // $("#id_general-collision_subcategory").html(html_data);
            // if ($("#id_general-collision_subcategory").find(html_data).length <= 1){
            //     $("#id_general-collision_subcategory").disable=true;
            // }

        }
    });

});
