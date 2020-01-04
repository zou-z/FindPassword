import sqlite3
import os

class Main:
    def __init__(self):
        self.db_path="Account.db"
        self.table_name="account"
        self.key=None
        self.conn=None
        self.db=None
        self.data=None

    def check_db(self):
        while not os.path.exists(self.db_path):
            print("[×] 文件{0}不存在".format(self.db_path))
            self.db_path=input("请输入数据库文件地址(exit:退出):")
            if self.db_path=="exit":
                exit(0)
        self.conn=sqlite3.connect(self.db_path)
        self.db=self.conn.cursor()
        print("[√] 已打开数据库{0}".format(self.db_path))

    def display_a_result(self,res,index):
        length=[-12,-25,-20,-30,-50]
        for j in range(5):
            for k in res[j]:
                if '\u4e00'<=k<='\u9fff':
                    length[j]+=1
        print("%4s %{0}s%{1}s%{2}s%{3}s%{4}s".format(length[0],length[1],length[2],length[3],length[4])%('['+str(index)+']',res[0],res[1],res[2],res[3],res[4]))

    def get_all_account(self):
        cursor=self.db.execute("select * from "+self.table_name)
        self.data=cursor.fetchall()
        print("[√] 已获取所有账户信息:")
        print("%5s%-10s%-23s%-17s%-28s%-46s"%("","名称(Name)","地址(Address)","用户名(User)","密码(Psw)","详细信息(Detail)"))
        index=1
        for i in self.data:
            self.display_a_result(i,index)
            index+=1

    def cmd_help(self):
        print("%12s help"%("帮助"))
        print("%10s all"%("所有账户"))
        print("%12s find (名称)"%("搜索"))
        print("%12s decode (索引)"%("解密"))
        print("%10s additem (名称) (地址) (用户名) (原始密码) (详细信息)"%("添加项目"))
        print("%10s rmitem (索引)"%("删除项目"))
        print("%10s update name (索引) (新的名称)"%("修改名称"))
        print("%10s update address (索引) (新的地址)"%("修改地址"))
        print("%9s update user (索引) (新的用户名)"%("修改用户名"))
        print("%10s update psw (索引) (新的原始密码)"%("修改密码"))
        print("%8s update detail (索引) (新的详细信息)"%("修改详细信息"))
        print("%7s key"%("查看现在的密钥"))
        print("%10s newkey (新密钥)           //修改输入的密钥"%("修改密钥"))
        print("%10s rekey (旧密钥) (新密钥)   //以新密钥重新存储所有的密码,且修改输入的密钥"%("更换密钥"))
        print("%12s exit"%("退出"))

    def main_process(self):
        while True:
            cmd=input(">").split(' ')
            if cmd[0]=="help":
                self.cmd_help()
            elif cmd[0]=="exit":
                self.conn.close()
                exit(0)
            elif cmd[0]=="all":
                self.get_all_account()
            elif cmd[0]=="find":
                try:
                    self.main_process_find(cmd[1])
                except IndexError:
                    print("[×] 指令错误!")
                    print("[!] 格式为:find (名称)")
            elif cmd[0]=="decode":
                try:
                    try:
                        index=int(cmd[1])-1
                        if 0<=index<len(self.data):
                            tmp=self.main_process_decode(index)
                            print("[{0}][{1}]".format(self.data[index][2],tmp))
                        else:
                            print("[x] 索引范围应在[{0},{1}]".format(1,len(self.data)))
                    except ValueError:
                        print("[×] 指令错误!索引值为整数")
                except IndexError:
                    print("[×] 指令错误!")
                    print("[!] 格式为:decode (索引)")
            elif cmd[0]=="update":
                try:
                    try:
                        index=int(cmd[2])-1
                        if 0<=index<len(self.data):
                            if cmd[1]=="name":
                                self.db.execute('update account set Name="{0}" where Name="{1}"'.format(cmd[3],self.data[index][0]))
                            elif cmd[1]=="address":
                                self.db.execute('update account set Address="{0}" where Name="{1}"'.format(cmd[3],self.data[index][0]))
                            elif cmd[1]=="user":
                                self.db.execute('update account set User="{0}" where Name="{1}"'.format(cmd[3],self.data[index][0]))
                            elif cmd[1]=="psw":
                                encode_psw=self.main_process_encode(cmd[3])
                                self.db.execute('update account set Psw="{0}" where Name="{1}"'.format(encode_psw,self.data[index][0]))
                            elif cmd[1]=="detail":
                                self.db.execute('update account set Detail="{0}" where Name="{1}"'.format(cmd[3],self.data[index][0]))
                            else:
                                print("[×] 指令错误!")
                                print("[!] 格式为:update name (索引) (新的名称)")
                                print("[!] 格式为:update address (索引) (新的地址)")
                                print("[!] 格式为:update user (索引) (新的用户名)")
                                print("[!] 格式为:update psw (索引) (新的原始密码)")
                                print("[!] 格式为:update detail (索引) (新的详细信息)")
                                continue
                            self.conn.commit()
                            print("[√] 完成!")
                        else:
                            print("[x] 索引范围应在[{0},{1}]".format(1,len(self.data)))
                    except ValueError:
                        print("[×] 指令错误!索引值为整数")
                except IndexError:
                    print("[×] 指令错误!")
                    print("[!] 格式为:update name (索引) (新的名称)")
                    print("[!] 格式为:update address (索引) (新的地址)")
                    print("[!] 格式为:update user (索引) (新的用户名)")
                    print("[!] 格式为:update psw (索引) (新的原始密码)")
                    print("[!] 格式为:update detail (索引) (新的详细信息)")
            elif cmd[0]=="additem":
                try:
                    encode_psw=self.main_process_encode(cmd[4])
                    self.db.execute('insert into account values("{0}","{1}","{2}","{3}","{4}")'.format(cmd[1],cmd[2],cmd[3],encode_psw,cmd[5]))
                    self.conn.commit()
                    print("[√] 完成!")
                except IndexError:
                    print("[×] 指令错误!")
                    print("[!] 格式为:additem (名称) (地址) (用户名) (原始密码) (详细信息)")
            elif cmd[0]=="rmitem":
                try:
                    try:
                        index=int(cmd[1])-1
                        if 0<=index<len(self.data):
                            self.db.execute('delete from account where Name="{0}"'.format(self.data[index][0]))
                            self.conn.commit()
                            print("[√] 完成!")
                        else:
                            print("[x] 索引范围应在[{0},{1}]".format(1,len(self.data)))
                    except ValueError:
                        print("[×] 指令错误!索引值为整数")
                except IndexError:
                    print("[×] 指令错误!")
                    print("[!] 格式为:rmitem (索引)")
            elif cmd[0]=="key":
                if self.key==None:
                    print("[!] 未设置密钥!")
                else:
                    print("[{0}]".format(self.key))
            elif cmd[0]=="newkey":
                try:
                    self.key=cmd[1]
                except IndexError:
                    print("[×] 指令错误!")
                    print("[!] newkey (新密钥)")
            elif cmd[0]=="rekey":
                try:
                    self.key=cmd[1]
                    print("[*] 正在执行...")
                    self.main_process_rekey(cmd[2])
                    print("[√] 完成!")
                except IndexError:
                    print("[×] 指令错误!")
                    print("[!] rekey (旧密钥) (新密钥)")
            else:
                print("[×] 指令错误!")
                self.cmd_help()

    def main_process_find(self,name):
        print("%5s%-10s%-23s%-17s%-28s%-46s"%("","名称(Name)","地址(Address)","用户名(User)","密码(Psw)","详细信息(Detail)"))
        for i in self.data:
            if name in i[0]:
                self.display_a_result(i,self.data.index(i)+1)

    def main_process_decode(self,index):
        enc_psw=self.data[index][3]
        if self.key==None:
            self.key=input("请输入密钥:")
        dec_psw=""
        for i in range(0,len(enc_psw),2):
            tmp=int(enc_psw[i:i+2],16)-ord(self.key[int(i/2)%len(self.key)])
            dec_psw+=chr(tmp)
        return dec_psw

    def main_process_encode(self,psw):
        if self.key==None:
            self.key=input("请输入密钥:")
        enc_psw=""
        for i in range(len(psw)):
            tmp=ord(psw[i])+ord(self.key[i%len(self.key)])
            enc_psw+=hex(tmp)[2:].upper()
        return enc_psw

    def main_process_rekey(self,rekey):
        psw=[self.main_process_decode(i) for i in range(len(self.data))]
        self.key=rekey
        enc_psw=[self.main_process_encode(i) for i in psw]
        for i in range(len(self.data)):
            self.db.execute("update account set Psw=\""+enc_psw[i]+"\" where Name=\""+self.data[i][0]+"\"")
            self.conn.commit()

    def start(self):
        self.check_db()
        self.get_all_account()
        self.main_process()
     
if __name__=="__main__":
    main=Main()
    main.start()
    