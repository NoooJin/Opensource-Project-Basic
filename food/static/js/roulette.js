// @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

const $c = document.querySelector("canvas");
const ctx = $c.getContext(`2d`);


const product = [
  "한식", "중식", "돈까스 일식", "카페 디저트", "아시안 양식", "패스트푸드", "분식", "고기 요리", "기타",
];

const colors = ["#F6F1F1", "#F6F1F1", "#F6F1F1", "#F6F1F1", "#F6F1F1", "#F6F1F1",];

const newMake = () => {
    const [cw, ch] = [$c.width / 2, $c.height / 2];
    const arc = Math.PI / (product.length / 2);

    for (let i = 0; i < product.length; i++) {
      ctx.beginPath();
      ctx.fillStyle = colors[i % (colors.length -1)];
      ctx.moveTo(cw, ch);
      ctx.arc(cw, ch, cw, arc * (i - 1), arc * i);
      ctx.fill();
      ctx.closePath();
    }

    ctx.fillStyle = "#394867";
    ctx.font = "18px Jua";
    ctx.textAlign = "center";

    for (let i = 0; i < product.length; i++) {
      const angle = (arc * i) + (arc / 2);

      ctx.save()  ;

      ctx.translate(
        cw + Math.cos(angle) * (cw - 50),
        ch + Math.sin(angle) * (ch - 50),
      );

      ctx.rotate(angle + Math.PI / 2);

      product[i].split(" ").forEach((text, j) => {
        ctx.fillText(text, 0, 30 * j);
      });

      ctx.restore();
    }
}

const rotate = () => {
  $c.style.transform = `initial`;
  $c.style.transition = `initial`;

  setTimeout(() => {

    const ran = Math.floor(Math.random() * product.length);

    const arc = 360 / product.length;
    const rotate = (ran * arc) + 3600 + (arc * 3) - (arc/4);

    $c.style.transform = `rotate(-${rotate}deg)`;
    $c.style.transition = `1.5s`;

    // 백엔드 endpoint 에 랜덤으로 뽑은 카테고리를 넘겨줘서 도로명 주소를 json 반환받음
    // json 의 내용은 'address': str(address)
    var payload = new FormData();
    payload.append('category', product[ran])

    // roulette_request_endpoint 는 index.html 에 선언되어있음
    fetch(roulette_request_endpoint, {
        method: 'POST',
        body: payload
    })
    .then(response => response.json())
    .then(data => {
        // 얻은 도로명 주소로 Maps API 에 요청
        searchAddressToCoordinate(data['address'])
    })
    .catch(error => {
      console.error('Error:', error);
    });

    // const button_zindex =  document.getElementsByName("rullet-button");
    // button_zindex.style.zIndex = 1;
    // setTimeout(() => alert(`오늘 ${product[ran]} 어떠신가요?`), 2000);
  }, 1);
};

newMake();

var map = new naver.maps.Map("map", {
  center: new naver.maps.LatLng(36.628583, 127.457583),
  zoom: 15,
  mapTypeControl: true
});

var infoWindow = new naver.maps.InfoWindow({
  anchorSkew: true
});

map.setCursor('pointer');

function searchAddressToCoordinate(address) {
  naver.maps.Service.geocode({
      query: address
  }, function(status, response) {

      try {
        marker.setMap(null);
        infowindow.close();
      } catch (e) {

      }


      if (status === naver.maps.Service.Status.ERROR) {
          return alert('Something Wrong!');
      }

      if (response.v2.meta.totalCount === 0) {
          return alert('totalCount' + response.v2.meta.totalCount);
      }

      var htmlAddresses = [],
          item = response.v2.addresses[0],
          point = new naver.maps.Point(item.x, item.y);

      if (item.roadAddress) {
          htmlAddresses.push('[도로명 주소] ' + item.roadAddress);
      }

      if (item.jibunAddress) {
          htmlAddresses.push('[지번 주소] ' + item.jibunAddress);
      }

      if (item.englishAddress) {
          htmlAddresses.push('[영문명 주소] ' + item.englishAddress);
      }

      marker = new naver.maps.Marker({
        map: map,
        position: point
    });

      contentString = [
        '<div class="">',
        '   <h5>'+ address +'</h5>',
        '   <a href="https://map.naver.com/v5/search/%EC%B6%A9%EB%B6%81%EB%8C%80%ED%95%99%EA%B5%90%20%EA%B7%BC%EC%B2%98%20%EB%A7%9B%EC%A7%91/place/1784557064?placePath=%3Fentry=pll%26from=nx%26fromNxList=true&c=15,0,0,0,dh">'+ '클릭해주세요' +'</a>',
        '</div>'
    ].join('');

      infowindow = new naver.maps.InfoWindow({
      content: contentString,
      maxWidth: 300,
      backgroundColor: "#eee",
      borderColor: "#A4A4A4",
      borderRadius:"30px",
      borderWidth: 2,
      disableAnchor:true,
      anchorColor: "#A4A4A4",
      pixelOffset: new naver.maps.Point(10, -10)
  });

  naver.maps.Event.addListener(marker, "click", function(e) {
    if (infowindow.getMap()) {
      infowindow.close();
    } else {
      infowindow.open(map, marker);
    }
  });

      map.setCenter(point);
  });
}

naver.maps.Event.addListener(marker, "click", function(e) {
  if (infowindow.getMap()) {
    infowindow.close();
  } else {
    infowindow.open(map, marker);
  }
});

function hasArea(area) {
  return !!(area && area.name && area.name !== '');
}

function hasData(data) {
  return !!(data && data !== '');
}

function checkLastString (word, lastString) {
  return new RegExp(lastString + '$').test(word);
}

function hasAddition (addition) {
  return !!(addition && addition.value);
}

naver.maps.onJSContentLoaded = initGeocoder;