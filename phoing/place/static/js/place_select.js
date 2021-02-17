let DEFAULT_LAT = 37.564214;
let DEFAULT_LONG = 127.001699;


let lat = DEFAULT_LAT;
let lon = DEFAULT_LONG;




if (navigator.geolocation) {

    navigator.geolocation.getCurrentPosition(function(position) {

    lat = position.coords.latitude; // 위도
    lon = position.coords.longitude; // 경도

    console.log(lat, lon, "in geolocation")

    });

}

console.log(lat, lon, "after geolocation")


let mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = { 
        center: new kakao.maps.LatLng(lat, lon), // 지도의 중심좌표
        level: 4 // 지도의 확대 레벨 
    }; 


let map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다


let locPosition = new kakao.maps.LatLng(lat, lon), // 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다
    message = '<div style="padding:5px;">마커를 드래그해 위치를 설정하세요!</div>'; // 인포윈도우에 표시될 내용입니다
        
// 마커와 인포윈도우를 표시합니다
displayMarker(locPosition, message);

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
    map.setCenter(locPosition);      
}   




// function centerLatLon () {

//     let lat = DEFAULT_LAT;
//     let lon = DEFAULT_LONG;

//     if (navigator.geolocation) {

//         navigator.geolocation.getCurrentPosition(function(position) {
    
//         lat = position.coords.latitude; // 위도
//         lon = position.coords.longitude; // 경도

//         console.log(lat, lon, "in geolocation2")

//         });
    
//     }

//     console.log(lat, lon, "in geolocation")
//     return {
//         lat: lat,
//         lon: lon
//     };

// }