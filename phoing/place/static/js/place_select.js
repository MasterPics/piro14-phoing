let geocoder = new kakao.maps.services.Geocoder();

let DEFAULT_LAT = 37.564214;
let DEFAULT_LON = 127.001699;

let location_input = document.getElementById('place-location'), // 도로명 주소 input
    lat_input = document.getElementById('place-lat'), // lat input
    lon_input = document.getElementById('place-lon'); // lon input

var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = { 
        center: new kakao.maps.LatLng(DEFAULT_LAT, DEFAULT_LON), // 지도의 중심좌표
        level: 4 // 지도의 확대 레벨 
    }; 

var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

// HTML5의 geolocation으로 사용할 수 있는지 확인합니다 


let ps = new kakao.maps.services.Places();  // 장소 검색 객체를 생성합니다
let markers = []; // 마커를 담을 배열입니다

let infowindow = new kakao.maps.InfoWindow({zIndex:1}); // 검색 결과 목록이나 마커를 클릭했을 때 장소명을 표출할 인포윈도우를 생성합니다

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


// 출발 마커에 dragend 이벤트를 등록합니다
kakao.maps.event.addListener(userMarker, 'dragend', function() {
    searchDetailAddrFromCoords(userMarker.getPosition(), function(result, status) {
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
            lat_input.value = userMarker.getPosition().getLat();
            lon_input.value = userMarker.getPosition().getLng();
        }   
    });
});

searchPlaces();


function searchDetailAddrFromCoords(coords, callback) {
    // 좌표로 법정동 상세 주소 정보를 요청합니다
    geocoder.coord2Address(coords.getLng(), coords.getLat(), callback);
}



// 키워드 검색을 요청하는 함수입니다
function searchPlaces() {
    let keyword = document.getElementById('keyword').value;
    if (!keyword.replace(/^\s+|\s+$/g, '')) {
        alert('키워드를 입력해주세요!');
        return false;
    }
    // 장소검색 객체를 통해 키워드로 장소검색을 요청합니다
    ps.keywordSearch(keyword, placesSearchCB); 
}

// 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {
        // 정상적으로 검색이 완료됐으면
        // 검색 목록과 마커를 표출합니다
        displayPlaces(data);
        // 페이지 번호를 표출합니다
        displayPagination(pagination);
    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
        alert('검색 결과가 존재하지 않습니다.');
        return;
    } else if (status === kakao.maps.services.Status.ERROR) {
        alert('검색 결과 중 오류가 발생했습니다.');
        return;
    }
}

// 검색 결과 목록과 마커를 표출하는 함수입니다
function displayPlaces(places) {
    let listEl = document.getElementById('placesList'), 
    menuEl = document.getElementById('menu_wrap'),
    fragment = document.createDocumentFragment(), 
    bounds = new kakao.maps.LatLngBounds(), 
    listStr = '';
    // 검색 결과 목록에 추가된 항목들을 제거합니다
    removeAllChildNods(listEl);
    // 지도에 표시되고 있는 마커를 제거합니다
    removeMarker();
    for ( let i=0; i<places.length; i++ ) {
        // 마커를 생성하고 지도에 표시합니다
        let placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
            marker = addMarker(placePosition, i), 
            itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다
        // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
        // LatLngBounds 객체에 좌표를 추가합니다
        bounds.extend(placePosition);
        // 마커와 검색결과 항목에 mouseover 했을때
        // 해당 장소에 인포윈도우에 장소명을 표시합니다
        // mouseout 했을 때는 인포윈도우를 닫습니다
        (function(marker, title) {
            kakao.maps.event.addListener(marker, 'mouseover', function() {
                displayInfowindow(marker, title);
            });
            kakao.maps.event.addListener(marker, 'mouseout', function() {
                infowindow.close();
            });
            kakao.maps.event.addListener(marker, 'click', function(){
                map.setLevel(6);
                map.panTo(marker.getPosition());
                // map.setLevel((map.getLevel() > 5) ? 5 : map.getLevel());
                userMarker.setPosition(marker.getPosition());
                renewLocationInputs();
            });
            // itemEl.onmouseover =  function () {
            //     displayInfowindow(marker, title);
            // };
            // itemEl.onmouseout =  function () {
            //     infowindow.close();
            // };
            itemEl.onclick = function () {
                map.setCenter(marker.getPosition());
                map.setLevel((map.getLevel() > 5) ? 5 : map.getLevel());
                userMarker.setPosition(marker.getPosition());
                renewLocationInputs();
            }
        })(marker, places[i].place_name);
        fragment.appendChild(itemEl);
    }
    // 검색결과 항목들을 검색결과 목록 Elemnet에 추가합니다
    listEl.appendChild(fragment);
    menuEl.scrollTop = 0;
    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
    map.setBounds(bounds);
    userMarker.setPosition(map.getCenter());
}

// 검색결과 항목을 Element로 반환하는 함수입니다
function getListItem(index, places) {
    let el = document.createElement('li'),
    itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                '<div class="info">' +
                '   <h5>' + places.place_name + '</h5>';
    if (places.road_address_name) {
        itemStr += '    <span>' + places.road_address_name + '</span>' +
                    '   <span class="jibun gray">' +  places.address_name  + '</span>';
    } else {
        itemStr += '    <span>' +  places.address_name  + '</span>'; 
    }
      itemStr += '  <span class="tel">' + places.phone  + '</span>' +
                '</div>';           
    el.innerHTML = itemStr;
    el.className = 'item';
    return el;
}

// 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
function addMarker(position, idx, title) {
    let imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png', // 마커 이미지 url, 스프라이트 이미지를 씁니다
        imageSize = new kakao.maps.Size(36, 37),  // 마커 이미지의 크기
        imgOptions =  {
            spriteSize : new kakao.maps.Size(36, 691), // 스프라이트 이미지의 크기
            spriteOrigin : new kakao.maps.Point(0, (idx*46)+10), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
            offset: new kakao.maps.Point(13, 37) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
        },
        markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions),
        marker = new kakao.maps.Marker({
            position: position, // 마커의 위치
            image: markerImage 
        });
    
    // kakao.maps.event.addListener(marker, 'click', markerClickListener(marker));
    marker.setMap(map); // 지도 위에 마커를 표출합니다
    markers.push(marker);  // 배열에 생성된 마커를 추가합니다
    return marker;
}
// 지도 위에 표시되고 있는 마커를 모두 제거합니다
function removeMarker() {
    for ( let i = 0; i < markers.length; i++ ) {
        markers[i].setMap(null);
    }   
    markers = [];
}
// 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
function displayPagination(pagination) {
    let paginationEl = document.getElementById('pagination'),
        fragment = document.createDocumentFragment(),
        i; 
    // 기존에 추가된 페이지번호를 삭제합니다
    while (paginationEl.hasChildNodes()) {
        paginationEl.removeChild (paginationEl.lastChild);
    }
    for (i=1; i<=pagination.last; i++) {
        let el = document.createElement('a');
        el.href = "#";
        el.innerHTML = i;
        if (i===pagination.current) {
            el.className = 'on';
        } else {
            el.onclick = (function(i) {
                return function() {
                    pagination.gotoPage(i);
                }
            })(i);
        }
        fragment.appendChild(el);
    }
    paginationEl.appendChild(fragment);
}
// 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
// 인포윈도우에 장소명을 표시합니다
function displayInfowindow(marker, title) {
    let content = '<div style="padding:5px;z-index:1;">' + title + '</div>';
    infowindow.setContent(content);
    infowindow.open(map, marker);
}
 // 검색결과 목록의 자식 Element를 제거하는 함수입니다
function removeAllChildNods(el) {   
    while (el.hasChildNodes()) {
        el.removeChild (el.lastChild);
    }
}
$(function (){
	$("#button").click(function (){
  	$("#menu_wrap").toggle();
  });
});


// function markerClickListener(targetMarker) {
//     return function(){
//         markerLoc = targetMarker.getPosition();
//         map.setLevel((map.getLevel() > 4 ? 4 : map.getLevel()));
//         map.setCenter(markerLoc);
//         marker.setPosition(markerLoc);
//     }
// }

 

function renewLocationInputs(){
    searchDetailAddrFromCoords(userMarker.getPosition(), function(result, status) {
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
            lat_input.value = userMarker.getPosition().getLat();
            lon_input.value = userMarker.getPosition().getLng();
        }   
    });
}


