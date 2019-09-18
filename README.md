# Local Weather RSS Sensor (기상청 동네예보 RSS)
Local Weather RSS Sensor for Home Assistant<br>
기상청 동네예보 RSS를 활용한 Home Assistant Sensor 입니다.<br>
<br>
![screenshot_1](https://github.com/miumida/local_weather_rss/blob/master/local_weather_rss_screenshot_1.png)<br>
![screenshot_2](https://github.com/miumida/local_weather_rss/blob/master/local_weather_rss_screenshot_2.png)
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
### 지역코드(localcode)
- 기상청 RSS 서비스로 접속하여 원하는 지역의 선택하여 지역코드를 찾습니다.
  `http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=`__1159068000__
<br><br>
## 참조 링크
[1] 기상청 RSS 서비스 : <https://web.kma.go.kr/weather/lifenindustry/sevice_rss.jsp><br>
[2] 기상청 동네예보 XML 정보 : <http://www.kma.go.kr/images/weather/lifenindustry/timeseries_XML.pdf>
