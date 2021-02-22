let DEFAULT_LAT = 37.564214;
let DEFAULT_LON = 127.001699;

var mapContainer = document.getElementById('map'), // 지도를 표시할 div  
    mapOption = { 
        center: new kakao.maps.LatLng(DEFAULT_LAT, DEFAULT_LON), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };

var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다


let userMarker;
let userMarkerSrc = 'http://www.pngall.com/wp-content/uploads/2017/05/Map-Marker-Free-Download-PNG.png', // 출발 마커이미지의 주소입니다    
    userMarkerSize = new kakao.maps.Size(35, 40), // 출발 마커이미지의 크기입니다 
    userMarkerOption = { 
        offset: new kakao.maps.Point(17, 43) // 출발 마커이미지에서 마커의 좌표에 일치시킬 좌표를 설정합니다 (기본값은 이미지의 가운데 아래입니다)
    };

// 출발 마커 이미지를 생성합니다
let userMarkerImage = new kakao.maps.MarkerImage(userMarkerSrc, userMarkerSize, userMarkerOption);
// 마커를 생성합니다

userMarker = new kakao.maps.Marker({  
    map: map, 
    position: map.getCenter(),
    draggable: true, // 출발 마커가 드래그 가능하도록 설정합니다
    image: userMarkerImage, // 출발 마커이미지를 설정합니다
    zIndex: 3
}); 

if (navigator.geolocation) {
    
    // GeoLocation을 이용해서 접속 위치를 얻어옵니다
    navigator.geolocation.getCurrentPosition(function(position) {
        
        var lat = position.coords.latitude, // 위도
            lon = position.coords.longitude; // 경도

        var locPosition = new kakao.maps.LatLng(lat, lon);

        map.setCenter(locPosition);
        userMarker.setPosition(locPosition);

    });
        
    
} else { // HTML5의 GeoLocation을 사용할 수 없을때 마커 표시 위치와 인포윈도우 내용을 설정합니다
    
    var locPosition = new kakao.maps.LatLng(DEFAULT_LAT, DEFAULT_LON);
        
    map.setCenter(locPosition);
    userMarker.setPosition(map.getCenter);
}

