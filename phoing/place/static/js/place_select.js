let geocoder = new kakao.maps.services.Geocoder();

let DEFAULT_LAT = 37.564214;
let DEFAULT_LON = 127.001699;


let location_input = document.getElementById('place-location'), // 도로명 주소 input
    lat_input = document.getElementById('place-lat'), // lat input
    lon_input = document.getElementById('place-lon'); // lon input

let mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = { 
        center: new kakao.maps.LatLng(DEFAULT_LAT, DEFAULT_LON), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨 
    }; 

let map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

// HTML5의 geolocation으로 사용할 수 있는지 확인합니다 
if (navigator.geolocation) {
    
    // GeoLocation을 이용해서 접속 위치를 얻어옵니다
    navigator.geolocation.getCurrentPosition(function(position) {
        
        var lat = position.coords.latitude, // 위도
            lon = position.coords.longitude; // 경도
        
        var locPosition = new kakao.maps.LatLng(lat, lon), // 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다
            message = '<div style="padding:5px;">마커를 드래그 해 위치를 지정해주세요!</div>'; // 인포윈도우에 표시될 내용입니다
        
        // 마커와 인포윈도우를 표시합니다
        displayMarker(locPosition, message);
            
      });
    
} else { // HTML5의 GeoLocation을 사용할 수 없을때 마커 표시 위치와 인포윈도우 내용을 설정합니다
    
    var locPosition = new kakao.maps.LatLng(33.450701, 126.570667),    
        message = '마커를 드래그 해 위치를 지정해주세요!'
        
    displayMarker(locPosition, message);
}



// // 지도에 마커와 인포윈도우를 표시하는 함수입니다
function displayMarker(locPosition, message) {

    let markerSrc = 'http://www.pngall.com/wp-content/uploads/2017/05/Map-Marker-Free-Download-PNG.png', // 출발 마커이미지의 주소입니다    
    markerSize = new kakao.maps.Size(50, 45), // 출발 마커이미지의 크기입니다 
    markerOption = { 
        offset: new kakao.maps.Point(15, 43) // 출발 마커이미지에서 마커의 좌표에 일치시킬 좌표를 설정합니다 (기본값은 이미지의 가운데 아래입니다)
    };

    // 출발 마커 이미지를 생성합니다
    let markerImage = new kakao.maps.MarkerImage(markerSrc, markerSize, markerOption);

    // 마커를 생성합니다
    let marker = new kakao.maps.Marker({  
        map: map, 
        position: locPosition,
        draggable: true, // 출발 마커가 드래그 가능하도록 설정합니다
        image: markerImage // 출발 마커이미지를 설정합니다
    }); 


    // 출발 마커에 dragend 이벤트를 등록합니다
    kakao.maps.event.addListener(marker, 'dragend', function() {
        searchDetailAddrFromCoords(marker.getPosition(), function(result, status) {
            if (status === kakao.maps.services.Status.OK) {
                
                // let detailAddr = !!result[0].road_address ? '<div>도로명주소 : ' + result[0].road_address.address_name + '</div>' : '';
                // detailAddr += '<div>지번 주소 : ' + result[0].address.address_name + '</div>';
                
                // let content = '<div class="bAddr">' +
                //                 '<span class="title">법정동 주소정보</span>' + 
                //                 detailAddr + 
                //             '</div>';
    
                // // 인포윈도우에 클릭한 위치에 대한 법정동 상세 주소정보를 표시합니다
                // infowindow.setContent(content);
                // infowindow.open(map, marker);

                location_input.value = !!result[0].road_address ? result[0].road_address.address_name : result[0].address.address_name;
                
                lat_input.value = marker.getPosition().getLat();
                lon_input.value = marker.getPosition().getLng();

            }   
        });
    });


    let iwContent = message, // 인포윈도우에 표시할 내용
        iwRemoveable = true;

    // 인포윈도우를 생성합니다
    let infowindow = new kakao.maps.InfoWindow({
        content : iwContent,
        removable : iwRemoveable
    });
    
    // 인포윈도우를 마커위에 표시합니다 
    // infowindow.open(map, marker);
    
    // 지도 중심좌표를 접속위치로 변경합니다
    // map.setCenter(locPosition);   
    map.panTo(locPosition);

}   


function searchDetailAddrFromCoords(coords, callback) {
    // 좌표로 법정동 상세 주소 정보를 요청합니다
    geocoder.coord2Address(coords.getLng(), coords.getLat(), callback);
}



