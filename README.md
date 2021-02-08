# Local Weather RSS Sensor (기상청 동네예보 RSS)

![HAKC][hakc-shield]
![HACS][hacs-shield]
![Version v1.0.1][version-shield]

Local Weather RSS Sensor for Home Assistant<br>
기상청 동네예보 RSS를 활용한 Home Assistant Sensor 입니다.<br>
- 동네예보RSS와 동네예보RSS속성, 두가지 형태의 센서를 생성합니다.<br>
- 예상강수량(3h/6h/12h)은 R06/2로 3시간 단위의 예상강수량을 누적해서 R03, R06H, R12H로 제공합니다.<br>
- 기상청 동네얘보 RSS는 02, 05, 08, 11, 14, 17, 20, 23시 (1일 8회)에 발표됩니다.<br>

![screenshot_3](https://github.com/miumida/local_weather_rss/blob/master/local_weather_rss_screenshot_3.png)<br>
![screenshot_1](https://github.com/miumida/local_weather_rss/blob/master/local_weather_rss_screenshot_1.png)<br>

![screenshot_2](https://github.com/miumida/local_weather_rss/blob/master/local_weather_rss_screenshot_2.png)<br>
<br><br>
## Installation
- HA 설치 경로 아래 custom_components 에 파일을 넣어줍니다.<br>
  `<config directory>/custom_components/local_weather_rss/__init__.py`<br>
  `<config directory>/custom_components/local_weather_rss/manifest.json`<br>
  `<config directory>/custom_components/local_weather_rss/sensor.py`<br>
- configuration.yaml 파일에 설정을 추가합니다.<br>
- Home-Assistant 를 재시작합니다<br>
<br><br>
## Usage
### configuration
- HA 설정에 Local Weather RSS sensor를 추가합니다.<br>
```yaml
sensor:
  - platform: local_weather_rss
    localcode: 지역코드
```
<br><br>
### 지역코드
- 기상청 RSS 서비스로 접속하여 원하는 지역의 선택하여 지역코드를 찾습니다.<br>
  동네예보에서 지역1,2,3을 선택하고 RSS 버튼을 눌러주면 RSS 주소가 나옵니다.<br>
  RSS 주소(`http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=1159068000`)에 포함된 숫자(**1159068000**)가 지역코드.<br>
![kma_rss_service](https://github.com/miumida/local_weather_rss/blob/master/kma_rss_service.png)<br>
<br><br>
## History
##### 2019-09-30 수정사항
- 구름 조금/구름 많이 mdi icon 변경 ( 0.98.1 이후 버전만 적용필요)<br>mdi:weather-partlycloudy -> mdi:weather-partly-cloudy<br>
##### 2019-09-19 수정사항
- 최저/최대 기온 -999.0인 경우, 이전 값 유지하도록 수정<br>
- 예상적설량 3h/6h/12h 추가(snow_prediction_3h/snow_prediction_6h/snow_prediction_12h)<br>
- 풍속/풍향 추가(wind_speed/wind_direction)<br>
- 기타 소소한 수정<br>
<br><br>
## 참조 링크
[1] 기상청 RSS 서비스 : <https://web.kma.go.kr/weather/lifenindustry/sevice_rss.jsp><br>
~~[2] 기상청 동네예보 XML 정보 : <http://www.kma.go.kr/images/weather/lifenindustry/timeseries_XML.pdf>~~<br>
[3] 기상청 동네예보 RSS 정의 : <https://web.kma.go.kr/images/weather/lifenindustry/dongnaeforecast_rss.pdf>

[version-shield]: https://img.shields.io/badge/version-v1.0.1-orange.svg
[hakc-shield]: https://img.shields.io/badge/HAKC-Enjoy-blue.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg
