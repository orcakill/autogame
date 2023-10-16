# @Time: 2023年10月16日 12:20
# @Author: orcakill
# @File: arrange.py
# @Description: 自动部署

import os

import paramiko
import py7zr

from src.utils import utils_path
from utils.my_logger import my_logger as logger

if __name__ == '__main__':
    project_path = utils_path.get_project_path()
    # 指定要压缩的文件夹路径
    folder_path = os.path.join(project_path, 'src')
    # 指定压缩包保存的路径和名称
    rar_path = os.path.join(project_path, 'src.rar')
    # 创建RAR压缩包对象并添加文件
    logger.debug("正在压缩文件夹")
    with py7zr.SevenZipFile(rar_path, mode='w') as rar:
        rar.writeall(folder_path, os.path.basename(folder_path))
    logger.debug("压缩文件夹完成")
    server = utils_path.get_server()
    # SSH连接参数
    host = server['ip']
    port = server['port']
    username = server['username']
    password = server['password']
    # 连接SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    # 上传压缩包到服务器
    logger.debug("正在上传")
    sftp = ssh.open_sftp()
    remote_rar_path = 'C:/projects/autogame/src.rar'  # 服务器上的目标压缩包路径
    sftp.put(rar_path, remote_rar_path)
    sftp.close()
    logger.debug("上传完成")
    # # 在服务器上解压缩文件（覆盖已有文件）
    # logger.debug("正在服务器解压缩")
    # # 构建解压缩命令
    # unrar_cmd = f'unrar.exe x -o+ C:\projects\autogame1\src.rar C:\projects\autogame1\''
    # ssh.exec_command(unrar_cmd)
    # logger.debug("服务器解压缩完成")
    # 关闭SSH连接
    ssh.close()
    logger.debug("自动化部署完成")


