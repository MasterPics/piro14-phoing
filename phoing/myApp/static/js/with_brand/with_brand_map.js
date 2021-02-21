let DEFAULT_LAT = 37.564214;
let DEFAULT_LON = 127.001699;


let mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = { 
        center: new kakao.maps.LatLng(DEFAULT_LAT, DEFAULT_LON), // 지도의 중심좌표
        level: 10 // 지도의 확대 레벨 
    }; 

let map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

// HTML5의 geolocation으로 사용할 수 있는지 확인합니다 
if (navigator.geolocation) {
    
    // GeoLocation을 이용해서 접속 위치를 얻어옵니다
    navigator.geolocation.getCurrentPosition(function(position) {
        
        let lat = position.coords.latitude, // 위도
            lon = position.coords.longitude; // 경도
        
        let locPosition = new kakao.maps.LatLng(lat, lon);// 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다
        
        // 마커와 인포윈도우를 표시합니다
        displayUserMarker(locPosition);
        displayContactMarkers();
            
      });
    
} else { // HTML5의 GeoLocation을 사용할 수 없을때 마커 표시 위치와 인포윈도우 내용을 설정합니다
    
    let locPosition = new kakao.maps.LatLng(DEFAULT_LAT, DEFAULT_LON);  
    displayUserMarker(locPosition);
    displayContactMarkers();

}

// 지도에 마커와 인포윈도우를 표시하는 함수입니다
function displayUserMarker(locPosition) {

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
        position: locPosition,
        draggable: true, // 출발 마커가 드래그 가능하도록 설정합니다
        image: userMarkerImage, // 출발 마커이미지를 설정합니다
        zIndex: 2
    }); 
    
    // 지도 중심좌표를 접속위치로 변경합니다
    map.setCenter(locPosition);      
}    


function displayContactMarkers(){
    let imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 
    
    for (let i = 0; i < with_brands.length; i ++) {
        
        // 마커 이미지의 이미지 크기 입니다
        let imageSize = new kakao.maps.Size(24, 35); 
        
        // 마커 이미지를 생성합니다    
        let markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 

        // 마커 위치
        let markerLoc = new kakao.maps.LatLng(with_brands[i].lat, with_brands[i].lon)
        
        // 마커를 생성합니다
        let marker = new kakao.maps.Marker({
            map: map, // 마커를 표시할 지도
            position: markerLoc, // 마커를 표시할 위치
            title : with_brands[i].title, // 마커의 타이틀, 마커에 마우스를 올리면 타이틀이 표시됩니다
            image : markerImage // 마커 이미지 
        });

        let infowindow = new kakao.maps.InfoWindow({
            content: displayCustomInfoWindow(with_brands[i]), // 인포윈도우에 표시할 내용
            zIndex: 3
        });

        kakao.maps.event.addListener(marker, 'mouseover', makeOverListener(map, marker, infowindow));
        kakao.maps.event.addListener(marker, 'mouseout', makeOutListener(infowindow));
        kakao.maps.event.addListener(marker, 'click', giveDetailListner(i))
    }

}

function displayCustomInfoWindow(with_brand) {
    let content = '<div class="info-window">' +
        '<div class="title"> Title: ' + with_brand.title + '</div>' +
        '<div class="pay"> Payment: ' + with_brand.pay + '</div>' + 
        '<div class="period"> Period: ' + with_brand.start_date + '-' + with_brand.end_date + '</div>' + 
        '<div class="address"> Address: ' + with_brand.address + '</div>' + 
        '<a href="/with_brand/detail/' + with_brand.pk + '/">자세히보기</a>' +  
    '</div>'

    return content;

}

function makeOverListener(map, marker, infowindow) {
    return function() {
        infowindow.open(map, marker);
    };
}

// 인포윈도우를 닫는 클로저를 만드는 함수입니다 
function makeOutListener(infowindow) {
    return function() {
        infowindow.close();
    };
}

function giveDetailListner(index) {
    return function() {
        window.location.href = "/with_brand/detail/" + (index + 1) + "/";
    }
}

