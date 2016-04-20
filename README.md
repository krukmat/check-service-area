Sample API docstring:

""" Returns whether location is supported (can provide a recommendation). We derive the location in this way:
1. Use latlng, if given
2. Use hotel address, if given
3. Try to find the hotel given the hotel_name that is close to the airport_code
4. Use airport_code

:param latlon: latitude/longitude, as comma separated string: "37.775,-122.4183333"
:param address: Address location as a string
:param airport_code: Airport code location as a string
:param hotel_name: Name of hotel as a string
:return: :json:`{"is_region_supported": boolean}`

:raises
"""

Installation:
============
   * docker-compose build

Execution:
=========
   * docker-compose up web

Tests:
======
   * docker-compose run web python manage.py test
   * benchmark: docker-compose run benchmark (it's needed run in a different terminal)
   * coverage:
        * docker-compose run coverage
        * docker-compose run report

Benchmark conclusions:
=====================
   * Running 30s test @ http://192.168.99.100:6666/query?airport_address=2100%20NW%2042nd%20Ave.%20Miami,%20Fl&hotel_name=Coral+Creek+Plaza
      12 threads and 400 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     1.86s    94.05ms   2.00s    55.56%
        Req/Sec     3.25      4.64    30.00     82.89%
      443 requests in 30.07s, 80.27KB read
      Socket errors: connect 0, read 488, write 0, timeout 434
    Requests/sec:     14.73
    Transfer/sec:      2.67KB
   * The requests per second are between, (min: 3.25 - max: 30.00).
   * So the range hourly would be (min: 11.7K - max: 27K).
   * And daily: (304.2K, 648K)