import logging
import requests
import voluptuous as vol
import xml.etree.ElementTree

import homeassistant.helpers.config_validation as cv

from datetime import timedelta
from datetime import datetime
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, CONF_API_KEY, CONF_ICON)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

CONF_NAME  = 'name'
CONF_LOCAL_CODE = 'localcode'
CONF_TYPE = 'type'

KMA_BSE_URL = 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone={}'

_WEATHER_PROPERTIES = {
  'PUB_DATE': ['public_date', None, 'mdi:clock-outline'],
  'CATEGORY': ['location', None, 'mdi:map-marker'],
  'DAY': ['day', None, 'mdi:calendar-today'],
  'HOUR': ['hour', 'h', 'mdi:clock-outline'],
  'REH': ['humidity', '%', 'mdi:water-percent'],
  'R03': ['rain_prediction_3h', 'mm', 'mdi:water'],
  'R06H': ['rain_perdiction_6h', 'mm', 'mdi:water'],
  'R12H': ['rain_prediction_12h', 'mm', 'mdi:water'],
  'POP': ['rain_percent', '%', 'mdi:water-percent'],
  'S03': ['snow_prediction_3h','cm','mdi:snowflake'],
  'S06H': ['snow_prediction_6h', 'cm', 'mdi:snowflake'],
  'S12H': ['snow_prediction_12h', 'cm', 'mdi:snowflake'],
  'TEMP': ['temperature', '°C', 'mdi:thermometer'],
  'TMX': ['temperature_max', '°C', 'mdi:thermometer'],
  'TMN': ['temperature_min', '°C', 'mdi:thermometer'],
  'WFKOR': ['weather_forecast', None, None],
  'WS': ['wind_speed', 'm/s', 'mdi:weather-windy'],
  'WDKOR': ['wind_direction', None, 'mdi:weather-windy'],
}

_WEATHER_DAY = {
  '0': '오늘',
  '1': '내일',
  '2': '모레',
}

FORMAT_TEMP = '{} °C'
FORMAT_PERCENT = '{} %'
FORMAT_MM = '{} mm'
FORMAT_CM = '{} cm'

DEFAULT_NAME = 'local_weather_rss'
DEFAULT_ICON = 'mdi:weather-partlycloudy'
DEFAULT_TYPE = '3'

MIN_TIME_BETWEEN_API_UPDATES    = timedelta(seconds=1800) #
MIN_TIME_BETWEEN_SENSOR_UPDATES = timedelta(seconds=1800) #

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_LOCAL_CODE): cv.string,
    vol.Optional(CONF_TYPE, default=DEFAULT_TYPE): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    name  = config.get(CONF_NAME)
    local = config.get(CONF_LOCAL_CODE)
    type  = config.get(CONF_TYPE)

    sensors = []

    rss = RSSWeatherAPI(name, local)

    rssSensor = rssWeatherSensor( name, rss )
    rssSensor.update()

    #동네예보RSS 센서 생성
    sensors += [rssSensor]

    # Weater Properties Sensor Add : _WEATHER_PROPERTIES에 정의된 것만 추가
    for key, value in rssSensor.data.items():
        if key in _WEATHER_PROPERTIES:
            sensors += [ weatherPropertySensor(key, value, rss) ]

    add_entities(sensors, True)

#WFKOR 또는 WFEN으로 아이콘 가져오기
def get_icon(wfcode):
    if wfcode == '맑음' or wfcode == 'Clear':
        return 'mdi:weather-sunny'
    if wfcode == '구름 조금' or wfcode == 'Partly Cloudy':
        return 'mdi:weather-partly-cloudy'
    if wfcode == '구름 많음' or wfcode == 'Mostly Cloudy':
        return 'mdi:weather-partly-cloudy'
    if wfcode == '흐림' or wfcode == 'Cloudy':
        return 'mdi:weather-cloudy'
    if wfcode == '비' or wfcode == 'Rain':
        return 'mdi:weather-pouring'
    if wfcode == '눈/비' or wfcode == 'Snow/Rain':
        return 'mdi:weather-snowy-rainy'
    if wfcode == '눈' or wfcode == 'Snow':
        return 'mdi:weather-snowy'

class RSSWeatherAPI:

    def __init__(self, name, local):
        """Initialize the RSS Weather API."""
        self._name      = name
        self._local     = local
        self.result     = {}

    @Throttle(MIN_TIME_BETWEEN_API_UPDATES)
    def update(self):
        """Update function for updating api information."""
        try:
            dt = datetime.now()
            syncDate = dt.strftime("%Y-%m-%d %H:%M:%S")

            url = KMA_BSE_URL.format(self._local)

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            page = response.content.decode('utf-8')

            root = xml.etree.ElementTree.fromstring(page)

            #동네예보 지역
            category = root.find('channel').find('item').find('category').text

            #발표시간
            tm = root.find('channel').find('item').find('description').find('header').find('tm').text

            #발표시간 출력형태 변경 : YYYYMMDDHH24MIHH -> YYYY-MM-DD HH24:MI:00
            pubDate = '{}-{}-{} {}:{}:00'.format(tm[0:4], tm[4:6], tm[6:8], tm[8:10],tm[10:12])

            dictBuf = {}

            # R06/2로 계산한 R03을 누적해서 계산하기 위한 변수 초기화
            rain_accu_6h  = 0
            rain_accu_12h = 0

            # S06/2로 계산한 S03을 누적해서 계산하기 위한 변수 초기화
            snow_accu_6h  = 0
            snow_accu_12h = 0

            for element in root.getiterator("data"):
                seq = element.attrib['seq']

                # 동네예보 12시간 이내 정보만 사용
                if int(seq) > 3:
                    break

                ATTR_HOUR = element.findtext('hour')
                ATTR_DAY = element.findtext('day')
                ATTR_TEMP = element.findtext('temp')
                ATTR_TMX = element.findtext('tmx')
                ATTR_TMN = element.findtext('tmn')
                ATTR_SKY = element.findtext('sky')
                ATTR_PTY = element.findtext('pty')
                ATTR_WFKOR = element.findtext('wfKor')
                ATTR_WFEN = element.findtext('wfEn')
                ATTR_POP = element.findtext('pop')

                ATTR_R12 = element.findtext('r12')
                ATTR_S12 = element.findtext('s12')

                ATTR_WS = element.findtext('ws')
                ATTR_WD = element.findtext('wd')
                ATTR_WDKOR = element.findtext('wdKor')
                ATTR_WDEN = element.findtext('wdEn')
                ATTR_REH = element.findtext('reh')
                ATTR_R06 = element.findtext('r06')
                ATTR_S06 = element.findtext('s06')

                # 6시간 예상강우량/적설량이기 때문에 2로 나눠서 3시간 예상강수량/적설량을 계산
                ATTR_R03 = 0.0 if float(ATTR_R06) == 0 else float(ATTR_R06)/2
                ATTR_S03 = 0.0 if float(ATTR_S06) == 0 else float(ATTR_S06)/2

                # 6시간 강수량/적설량을 누해적서 6시간 예상강수량/적설량 계산
                if int(seq) < 3:
                    rain_accu_6h += ATTR_R03
                    snow_accu_6h += ATTR_S03

                # 3시간 강수량/적설량을 누적해서 12시간 예상강수량/적설량 계산
                rain_accu_12h += ATTR_R03
                snow_accu_12h += ATTR_S03

                # 최근 1건에 대한 동네예보를 기준으로 표시
                if seq == '0':
                    dictBuf['HOUR'] = ATTR_HOUR
                    dictBuf['DAY'] = ATTR_DAY

                    dictBuf['TEMP'] = ATTR_TEMP
                    dictBuf['TMX'] = ATTR_TMX
                    dictBuf['TMN'] = ATTR_TMN
                    dictBuf['SKY'] = ATTR_SKY
                    dictBuf['PTY'] = ATTR_PTY

                    dictBuf['WFKOR'] = ATTR_WFKOR
                    dictBuf['WFEN']  = ATTR_WFEN

                    dictBuf['POP']   = ATTR_POP
                    dictBuf['WS']    = '{:.1f}'.format(float(ATTR_WS))
                    dictBuf['WD']    = ATTR_WD
                    dictBuf['WDKOR'] = ATTR_WDKOR
                    dictBuf['WDEN']  = ATTR_WDEN

                    dictBuf['REH'] = ATTR_REH
                    dictBuf['R06'] = ATTR_R06
                    dictBuf['S06'] = ATTR_S06
                    dictBuf['R03'] = ATTR_R03
                    dictBuf['S03'] = ATTR_S03

                    dictBuf['CATEGORY'] = category
                    dictBuf['PUB_DATE'] = pubDate

		    # -999 인 경우, 이전에 가지고 있던 값을 유지
                    if ATTR_TMX == '-999.0':
                        dictBuf['TMX'] = self.result.get('TMX', ATTR_TMX)

                    if ATTR_TMN == '-999.0':
                        dictBuf['TMN'] = self.result.get('TMN', ATTR_TMN)

            #R06/2로 계산하여 누적한 예상 강수량 추가(6H, 12H)
            dictBuf['R06H'] = rain_accu_6h
            dictBuf['R12H'] = rain_accu_12h
            #S06/2로 계산하여 누적한 예상 적설량 추가(6H, 12H)
            dictBuf['S06H'] = snow_accu_6h
            dictBuf['S12H'] = snow_accu_12h

            self.result = dictBuf
            #_LOGGER.debug('RSS Weather API Request Result: %s', self.result)
        except Exception as ex:
            _LOGGER.error('Failed to update RSS Weather API status Error: %s', ex)
            raise

class rssWeatherSensor(Entity):
    def __init__(self, name, api):
        self._name      = name
        self._api       = api
        self._icon      = DEFAULT_ICON
        self._state     = None
        self.data       = {}

    @property
    def entity_id(self):
        """Return the entity ID."""
        return 'sensor.{}'.format(self._name)

    @property
    def name(self):
        """Return the name of the sensor, if any."""
        return '동네예보RSS'

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        self._icon = get_icon(self.data.get('WFKOR', '-'))
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.data.get('WFKOR','-')

    @property
    def attribution(self):
        """Return the attribution."""
        return 'Powered by miumida'

    @Throttle(MIN_TIME_BETWEEN_SENSOR_UPDATES)
    def update(self):
        """Get the latest state of the sensor."""
        if self._api is None:
            return

        self._api.update()
        rss_dict = self._api.result

        self.data = rss_dict

    @property
    def device_state_attributes(self):
        """Attributes."""

        dict = { 'public_date': self.data['PUB_DATE']
               , 'location'   : self.data['CATEGORY']
               , 'day' : _WEATHER_DAY[self.data['DAY']]
               , 'hour': '{} h'.format(self.data['HOUR'])
               # 기온/습도
               , 'temperature'    : FORMAT_TEMP.format(self.data['TEMP'])
               , 'temperature_max': FORMAT_TEMP.format(self.data['TMX'])
               , 'temperature_min': FORMAT_TEMP.format(self.data['TMN'])
               , 'humidity': FORMAT_PERCENT.format(self.data['REH'])
               # 강수확률/강수량/적설량
               , 'rain_percent'       : FORMAT_PERCENT.format(self.data['POP'])
               , 'rain_prediction_3h' : FORMAT_MM.format(self.data['R03'])
               , 'rain_prediction_6h' : FORMAT_MM.format(self.data['R06H'])
               , 'rain_prediction_12h': FORMAT_MM.format(self.data['R12H'])
               , 'snow_prediction_3h' : FORMAT_CM.format(self.data['S03'])
               , 'snow_prediction_6h' : FORMAT_CM.format(self.data['S06H'])
               , 'snow_prediction_12h': FORMAT_CM.format(self.data['S12H'])
               #바람 관련
               , 'wind_speed'    : '{} m/s'.format(self.data['WS'])
               , 'wind_direction': self.data['WDKOR'] }

        return dict

# 날씨 속성 Sensor
class weatherPropertySensor(Entity):
    """Representation of a Weather Property Sensor."""

    def __init__(self, name, value, api):
        """Initialize the Weather Property sensor."""
        self._name        = name
        self._value       = value

        self._state       = None
        self._icon        = None
        self._api         = api

    @property
    def entity_id(self):
        """Return the entity ID."""
        return 'sensor.localweather_rss_{}'.format(self._name.lower())

    @property
    def name(self):
        """Return the name of the sensor, if any."""
        return _WEATHER_PROPERTIES[self._name][0]

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        self._icon = _WEATHER_PROPERTIES[self._name][2]

        if self._name == 'WFKOR':
            self._icon = get_icon(self._value)

        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return _WEATHER_DAY[self._value] if self._name == 'DAY' else self._value

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return '' if _WEATHER_PROPERTIES[self._name][1] is None else _WEATHER_PROPERTIES[self._name][1]

    @Throttle(MIN_TIME_BETWEEN_SENSOR_UPDATES)
    def update(self):
        """Get the latest state of the sensor."""
        if self._api is None:
            return

        self._api.update()

        self._value = self._api.result[self._name]
