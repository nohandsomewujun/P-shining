import math
import socket

class ChatSocket:
    # ���췽��
    def __init__(self):
        print("��ʼ��tcp�ͻ���")
        # ���������ͬʱ���ᴴ�����ӷ�������socket
        self.client_socket = socket.socket()  # ����socket
        self.client_socket.connect(('127.0.0.1', 5000))  # �������ӷ�����

    # �����¼����
    def login_type(self, user_name, password):
        # ���������½��Ǹ�������
        self.client_socket.sendall(bytes("1", "utf-8"))
        # ���ε���ʵ������������������û���������
        self.send_string_with_length(user_name)
        self.send_string_with_length(password)
        # ����ʵ��������ȡ�������ķ���ֵ��"1"����ͨ������0������ͨ��
        check_result = self.recv_string_by_length(1)  # ���ô˶����ʵ��������ȡ����������Ϣ
        return check_result  # True�����¼����ͨ����False�����¼����ʧ��

    # ����ע������
    def register_user(self, user_name, password, file_name):
        # ��������ע���Ǹ�������
        self.client_socket.sendall(bytes("2", "utf-8"))
        # ����ʵ���������η����û�������ͷ��·������������
        self.send_string_with_length(user_name)
        self.send_string_with_length(password)
        self.send_string_with_length(file_name)
        # ����ʵ��������ȡ����ֵ
        # "0"����ͨ������1�����������û���, "2"������������
        return self.recv_string_by_length(1)

    # ������Ϣ����
    def send_message(self, message, chat_user):
        # ������Ϣ���
        self.client_socket.sendall(bytes("3", "utf-8"))
        # ����ʵ�����������������Ĭ��ΪȺ��
        self.send_string_with_length(chat_user)
        # ���ô˶���ʵ������������Ϣ���ݸ�������
        self.send_string_with_length(message)

    # ����ˢ���û��б�����
    def send_refurbish_mark(self):
        # ����ˢ���û��б��Ǹ�������
        self.client_socket.sendall(bytes("4", "utf-8"))

    # =============== ��װһЩ���ͽ������ݵķ��� =================
    # ���ʹ����ȵ��ַ���
    def send_string_with_length(self, content):
        # �ȷ������ݵĳ���
        self.client_socket.sendall(bytes(content, encoding='utf-8').__len__().to_bytes(4, byteorder='big'))
        # �ٷ�������
        self.client_socket.sendall(bytes(content, encoding='utf-8'))

    # ��ȡ�����������Ķ����ַ���
    def recv_string_by_length(self, len):
        return str(self.client_socket.recv(len), "utf-8")

    # ��ȡ����˴����ı䳤�ַ�������������·��������ȴ�һ������ֵ
    def recv_all_string(self):
        length = int.from_bytes(self.client_socket.recv(4), byteorder='big')  # ��ȡ��Ϣ����
        b_size = 3 * 1024  # ע��utf8�����к���ռ3�ֽڣ�Ӣ��ռ1�ֽ�
        times = math.ceil(length / b_size)
        content = ''
        for i in range(times):
            if i == times - 1:
                seg_b = self.client_socket.recv(length % b_size)
            else:
                seg_b = self.client_socket.recv(b_size)
            content += str(seg_b, encoding='utf-8')
        return content

    # ��ȡ���������������û�����
    def recv_number(self):
        return int.from_bytes(self.client_socket.recv(4), byteorder='big')
