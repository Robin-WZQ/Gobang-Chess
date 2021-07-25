import socket
new_socket = socket.socket() #创建socket对象
ip = "192.168.149.1"          # 树莓派地址
port = 22               # 设置默认端口
new_socket.connect((ip,port))
i=0
while 1:
    x = input()
    y= input()
    z = input()
    t = x+","+y+","+z
    new_socket.send(t.encode())
    i+=1
    if i==4:
        back_str = new_socket.recv(1024).decode() #结束数据
        break
new_socket.close() #关闭客户端
print("客户端结束运行")