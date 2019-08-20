from __future__ import absolute_import

import logging
log = logging.getLogger(__name__)

from . _base import *


class Webcam(HttpPublisher):
   '''
   Publishes weather data to the pwsweather.com servers. See module
   documentation for additional information and usage idioms.
   '''

   def __init__(self, url, user, password):
      super(Webcam,self).__init__(user,password)
      self.server = url
      self.user = user
      self.password = password
      self.args = {  'action':'updateraw',
                     'softwaretype':self.SOFTWARE
                    }

   def set( self, pressure='NA', dewpoint='NA', humidity='NA', tempf='NA',
         rainin='NA', rainday='NA', rainmonth='NA', rainyear='NA',
         dateutc='NA', windgust='NA', windspeed='NA', winddir='NA',
         weather='NA', *args, **kw):
      '''
      Useful for defining weather data published to the server. Parameters not
      sent will be cleared and not set to server. Unknown keyword args will be
      silently ignored, so be careful. This is necessary for publishers that
      support more fields than others.
      '''
      # unused, but valid, parameters are:
      #   solarradiation, UV
      self.args.update( {
            'baromin':pressure,
            'dailyrainin':rainday,
            'dateutc':dateutc,
            'dewptf':dewpoint,
            'humidity':humidity,
            'monthrainin':rainmonth,
            'rainin':rainin,
            'tempf':tempf,
            'weather':weather,
            'winddir':winddir,
            'windgustmph':windgust,
            'windspeedmph':windspeed,
            'yearrainin':rainyear,
          } )
          
      log.debug( self.args )

   def real_publish(self, args, server):
      from httplib import HTTPConnection
      from urllib import urlencode
      import requests

      args = dict((k,v) for k,v in args.items() if v != 'NA')
      #http://server/path?3&4&800
      url = server + "?" + str(args['winddir']) + "&" +  str(args['windspeedmph']) + "&" + str(args['tempf'])

      log.debug(url)

      http = requests.get(url, timeout=5, auth=(self.user, self.password))

      data = (http.status_code, http.reason, http.text)
      if not (data[0] == 200 and data[1] == 'OK'):
         raise PublishException('Server returned invalid status: %d %s %s'
                 % data)
      return data

   def publish(self):
      http = self.real_publish(self.args, self.server)
      if not http[2].find('Logged and posted') >= 0:
         raise PublishException('Server returned invalid status: %d %s %s'
              % http)
      return http


