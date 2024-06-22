import io

from skytrak import parser

def test_parse_exported_csv():
    sample_csv = """,,,,,,,,,,,,,,,
  PRACTICE: 6/19/2023 5:39 PM,,,,,,,,,,,,,,,
  PLAYER: BENRADY,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,
SHOT,HAND,BALL SPEED,LAUNCH,BACK,SIDE,SIDE,OFFLINE,CARRY,ROLL,TOTAL,FLIGHT,DSCNT,HEIGHT,CLUB SPEED,SMASH
#,L/R,MPH,DEG,RPM,RPM,DEG,YD,YD,YD,YD,SEC,DEG,YD,MPH,SCORE
GW ,,,,,,,,,,,,,,,
1,R,81,30,9318,-533,1,-2,95,1,96,5.2,49.0,24,73,1.10
2,R,78,31,8552,-367,-2,-6,91,1,92,5.1,49.1,22,73,1.07
3,R,80,32,8437,-121,0,-1,94,1,95,5.3,50.6,25,73,1.09
4,R,83,32,8217,-1062,2,-3,98,2,100,5.4,51.7,26,73,1.13
5,R,79,32,8840,-506,-1,-6,91,1,92,5.2,50.0,24,75,1.05
AVG,,80,31,8673,-518,0,-4,94,1,95,5.2,50.0,24,73,1.09"""
    club_data = parser.parse(io.StringIO(sample_csv))
    assert club_data == {} # TODO