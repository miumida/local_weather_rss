# Local Weather RSS Sensor (기상청 동네예보 RSS)

![HAKC][hakc-shield]
![HACS][hacs-shield]
![Version v1.1.8][version-shield]

기상청 RSS 서비스 종료(2025.02)로 정상동작 하지 않습니다.<br>

Local Weather RSS Sensor for Home Assistant<br>
기상청 동네예보 RSS를 활용한 Home Assistant Sensor 입니다.<br>
- 동네예보RSS와 동네예보RSS속성, 두가지 형태의 센서를 생성합니다.<br>
- 예상강수량(3h/6h/12h)은 R06/2로 3시간 단위의 예상강수량을 누적해서 R03, R06H, R12H로 제공합니다.<br>
- 기상청 동네얘보 RSS는 02, 05, 08, 11, 14, 17, 20, 23시 (1일 8회)에 발표됩니다.<br>

![screenshot_1](https://github.com/miumida/local_weather_rss/blob/master/images/local_weather_rss_1.png)<br>
![screenshot_2](https://github.com/miumida/local_weather_rss/blob/master/images/local_weather_rss_2.png)<br>
![screenshot_3](https://github.com/miumida/local_weather_rss/blob/master/images/local_weather_rss_3.png)<br>
<br><br>

## Version history
| Version | Date        | 내용              |
| :-----: | :---------: | ----------------------- |
| v1.0.0  | 2019.09.19  | First version  |
| v1.0.1  | 2019.09.30  | - 구름 조금/구름 많이 mdi icon 변경 |
| v1.1.0  | 2021.02.10  | - 통합구성요소 추가<br>- 일부 아이콘 변경<br>- async 적용<br>- 속성센서 방식 변경 |
| v1.1.1  | 2021.03.05  | manifest.json 파일 version 정보  |
| v1.1.2  | 2021.07.10  | iterator() -> iter() 변경  |
| v1.1.3  | 2021.12.12  | 2021.12.0 HTTP_OK fix  |
| v1.1.4  | 2021.12.15  | 2021.12.0 Fixed bug  |
| v1.1.5  | 2023.07.20  | Fixed bug |
| v1.1.7  | 2023.08.07  | Fixed bug |

<br>

## Installation
### Manual
- HA 설치 경로 아래 custom_components 에 파일을 넣어줍니다.<br>
  `<config directory>/custom_components/local_weather_rss/__init__.py`<br>
  `<config directory>/custom_components/local_weather_rss/manifest.json`<br>
  `<config directory>/custom_components/local_weather_rss/sensor.py`<br>
- configuration.yaml 파일에 설정을 추가합니다.<br>
- Home-Assistant 를 재시작합니다<br>
### HACS
- HACS > Integretions > 우측상단 메뉴 > Custom repositories 선택
- 'https://github.com/miumida/local_weather_rss' 주소 입력, Category에 'integration' 선택 후, 저장
- HACS > Integretions 메뉴 선택 후, local_weather_rss 검색하여 설치

<br>

## Usage
### configuration
- HA 설정에 Local Weather RSS sensor를 추가합니다.<br>
```yaml
sensor:
  - platform: local_weather_rss
    name: local_weather_rss
    localcode: 지역코드
    properties: False
```

### 기본 설정값

|옵션|내용|
|--|--|
|platform| (필수) local_weather_rss  |
|name| (옵션) default(loca_weather_rss) |
|localcode| (필수) 원하는 지역 |
|properties| (옵션) 속성센서 사용여부 |

<br>

### 지역코드
- 기상청 RSS 서비스로 접속하여 원하는 지역의 선택하여 지역코드를 찾습니다.<br>
  동네예보에서 지역1,2,3을 선택하고 RSS 버튼을 눌러주면 RSS 주소가 나옵니다.<br>
  RSS 주소(`http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=1159068000`)에 포함된 숫자(**1159068000**)가 지역코드.<br>
![kma_rss_service](https://github.com/miumida/local_weather_rss/blob/master/kma_rss_service.png)<br>

<br>

## 참조 링크
[1] 기상청 RSS 서비스 : <https://web.kma.go.kr/weather/lifenindustry/sevice_rss.jsp><br>
~~[2] 기상청 동네예보 XML 정보 : <http://www.kma.go.kr/images/weather/lifenindustry/timeseries_XML.pdf>~~<br>
[3] 기상청 동네예보 RSS 정의 : <https://web.kma.go.kr/images/weather/lifenindustry/dongnaeforecast_rss.pdf>

[version-shield]: https://img.shields.io/badge/version-v1.1.8-orange.svg
[hakc-shield]: https://img.shields.io/badge/HAKC-Enjoy-blue.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg
