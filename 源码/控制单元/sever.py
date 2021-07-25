import socket

def main():
    '''
    socket communication between Windows and Linux
    '''
    #服务端
    new_socket = socket.socket()         # 创建 socket 对象
    ip = "192.168.149.1"          # 获取本地主机名
    port = 22               # 设置端口
    new_socket.bind((ip, port))        # 绑定端口
    new_socket.listen(20)                 # 等待客户端连接并设置最大连接数
    while True:
        init_position()
        new_cil, addr = new_socket.accept()     # 建立客户端连接。
        print('新进来的客户端的地址：', addr)
        t = new_cil.recv(1024).decode()
        t = t.split(',')
        put_chess(int(t[0]),int(t[1]))
        if(int(t[2]==0)):
            new_cil.close()                # 关闭连接
    
main()
             