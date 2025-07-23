import serial
import time
import turtle

connection = None
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
    
def read_serial_print():
    global connection
    if connection and connection.in_waiting > 0:
        data = connection.readline().decode('utf-8').strip()
        try:
            if data == '1':
                return 1 # '1'이면 정수 1 반환
        except ValueError:
            return None
        except Exception as e:
            print(f"데이터 읽기 중 오류 발생: {e}")
            return None
    return None

def main(t):
    while True:
        serial_value = read_serial_print()
        if serial_value == 1:
            t.fd(100)
            serial_value = 0

if __name__ == "__main__":
    if connect_sensor(port='COM3'):
        print("터틀 그래픽을 시작합니다. Ctrl+C로 종료하세요.")
        main(t)
        turtle.done()