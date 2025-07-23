"""
초음파 센서값에 따른 거북이 제어

초음파센서값이일정 거리 이하로 떨어지면 거북이를 90도 회전시키는 코드
1. 장애물회피값을 불타입데이터로 지정
2. 거리값이 특정거리 이하이고 장애물 회피값이 False면 90도 회전이후 장애물회피값을 True로 변겅
3. 거리값이 특정거리 이상이고 장애물 회피값이 True면 터틀을 직진시키고 장애물 회피값을 False로 변경해 다음 장애물을 회피할수있게 변경
4. 거리값이 특정거리 이상이고 장애물 회피값이 False면 직진
5. 2번 조건으로 인해 회전이후에도 거리값이 특정거리 이상으로 안올라가면 터틀이 정지된다
"""
import serial
import time
import turtle

# 스크린 생성
s = turtle.getscreen()
s.setup(width=900, height=900)

# 거북이 변수 지정
t = turtle.Turtle()
t.shapesize(2,2,2)
t.shape('turtle')
t.color("green", "blue")
t.pensize(5)

t.penup()
t.goto(-350,-350)
t.pendown()

connection = None
current_distance = 0
# 💡 핵심 추가: 장애물 회피 중임을 나타내는 플래그
is_avoiding_obstacle = False 

def connect_sensor(port='COM3'):
    global connection
    try:
        connection = serial.Serial(port, 9600, timeout=1) 
        time.sleep(2)
        print(f"센서 연결 성공! 포트: {port}")
        connection.flushInput()
        return True
    except serial.SerialException as e:
        print(f"센서 연결 실패: {e}")
        return False
    except Exception as e:
        print(f"알 수 없는 오류로 연결 실패: {e}")
        return False
    
def read_distance():
    global connection, current_distance
    if connection and connection.in_waiting > 0:
        data = connection.readline().decode().strip()
        try:
            distance = float(data)
            current_distance = distance
            return distance
        except ValueError:
            return None
        except Exception as e:
            print(f"데이터 읽기 중 오류 발생: {e}")
            return None
    return None

def main(t):
    global is_avoiding_obstacle # 전역 변수 사용 선언
    
    if connect_sensor():
        print("터틀 자동 주행 시작!")
        while True:
            dist = read_distance()

            if dist is not None:
                print(f"현재 거리: {dist:.2f} cm, 회피 모드: {is_avoiding_obstacle}") 

                # 💡 핵심 로직: 장애물 감지 and (아직 회피 중이 아닐 때만)
                if dist < 20.0 and not is_avoiding_obstacle:
                    print(f"장애물 감지! ({dist:.2f} cm). 90도 좌회전 및 회피 시작.")
                    t.lt(90) # 딱 한 번 좌회전
                    t.forward(50) # 장애물을 벗어날 충분한 거리 전진 (조절 필요)
                    is_avoiding_obstacle = True # 회피 모드 진입
                    
                    # 💡 선택 사항: 회피 후 바로 직진 경로로 돌아오고 싶다면 추가
                    # t.rt(90) 
                    
                elif dist >= 20.0 and is_avoiding_obstacle:
                    # 💡 회피 중이었는데 장애물을 벗어났을 경우
                    print(f"장애물 회피 완료! 현재 거리: {dist:.2f} cm.")
                    is_avoiding_obstacle = False # 회피 모드 해제
                    t.fd(5) # 장애물 벗어난 후 다시 직진 시작 (선택 사항: 굳이 필요없을수도 있음)
                    
                elif not is_avoiding_obstacle:
                    # 💡 평소에는 직진 (회피 중이 아닐 때)
                    t.fd(5) 
                
                # elif is_avoiding_obstacle and dist < 20.0:
                #     # 💡 회피 중인데 아직 장애물 안에 있다면 계속 전진만 (회전 없음)
                #     # 이 부분은 t.forward(50) 후에 루프가 돌면서 자연스럽게 처리됩니다.
                #     # 명시적으로 추가한다면 t.forward(5) 등을 넣을 수 있지만,
                #     # t.forward(50)만으로 충분하다면 이 블록은 필요 없습니다.
                #     t.fd(5) # 회피 중에도 계속 전진
                
            else:
                print("센서 값을 읽을 수 없습니다. 다시 시도합니다.")

            time.sleep(0.1) 
            
    else:
        print("센서 연결에 실패하여 프로그램을 종료합니다.")
        
if __name__ == "__main__":
    main(t)
    turtle.done()