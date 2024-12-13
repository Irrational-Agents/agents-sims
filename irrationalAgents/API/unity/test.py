'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2024-12-13 14:35:42
LastEditors: ephie && ephiewangyf@gmail.com
LastEditTime: 2024-12-13 18:04:43
FilePath: /Agents-Sim/irrationalAgents/API/unity/test.py
Description: 
'''
import asyncio
from API.unity.request import UnityRequest
from API.unity.unity import UnityServer
import threading

import socketio
import asyncio
import json
from datetime import datetime
from logger_config import setup_logger
logger = setup_logger('API-unity-test')

class TestClient:
    def __init__(self):
        self.sio = socketio.AsyncClient()
        
        # 设置事件处理器
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('response', self.on_response)
        self.sio.on('error', self.on_error)
        
    async def connect(self, url='http://0.0.0.0:5001'):
        await self.sio.connect(url)
        print(f"Connected to server: {url}")

    async def disconnect(self):
        await self.sio.disconnect()
        print("Disconnected from server")

    async def on_connect(self):
        print("Connection established")

    async def on_disconnect(self):
        print("Disconnected from server")

    async def on_response(self, data):
        print("\nReceived response:")
        print(json.dumps(data, indent=2))

    async def on_error(self, data):
        print("\nReceived error:")
        print(json.dumps(data, indent=2))

    async def test_get_npc_info(self, npc_id: str):
        await self.sio.emit('command', {
            'command': 'command.npc.GetNPCInfo',
            'parameters': {
                'NPCID': npc_id
            },
            'request_id': f'test_{datetime.now().timestamp()}'
        })
    async def test_get_npcs(self):
       """测试获取NPC列表的各种场景"""
       test_cases = [
        #    # 测试1: 获取所有NPCs的简略信息
        #    {
        #        'parameters': {
        #            'names': [],
        #            'isDetails': False
        #        },
        #        'description': 'Get all NPCs with basic info'
        #    },
           
        #    # 测试2: 获取所有NPCs的详细信息
        #    {
        #        'parameters': {
        #            'names': [],
        #            'isDetails': True
        #        },
        #        'description': 'Get all NPCs with detailed info'
        #    },
           
        #    # 测试3: 获取指定NPCs的简略信息
        #    {
        #        'parameters': {
        #            'names': ['zhang_san', 'Li Si'],
        #            'isDetails': False
        #        },
        #        'description': 'Get specific NPCs with basic info'
        #    },
           
        #    # 测试4: 获取不存在的NPC
        #    {
        #        'parameters': {
        #            'names': ['Invalid NPC'],
        #            'isDetails': False
        #        },
        #        'description': 'Get invalid NPC'
        #    },
           
        #    # 测试5: 混合有效和无效的NPC请求
        #    {
        #        'parameters': {
        #            'names': ['Zhang San', 'Invalid NPC'],
        #            'isDetails': True
        #        },
        #        'description': 'Get mixed valid and invalid NPCs'
        #    }
       ]

       for test_case in test_cases:
           logger.info(f"\nExecuting test: {test_case['description']}")
           await self.sio.emit('command', {
               'command': 'command.npc.GetNPCs',
               'parameters': test_case['parameters'],
               'request_id': f'test_{datetime.now().timestamp()}'
           })
           await asyncio.sleep(1)  # 等待响应




async def main():
    client = TestClient()
    
    try:
        # 连接服务器
        await client.connect()
        
        # 测试获取NPC信息
        print("\nTesting GetNPCInfo command...")
        await client.test_get_npc_info('zhang_san')
        
        # 等待响应
        await asyncio.sleep(2)
        
        # 测试不存在的NPC
        # print("\nTesting GetNPCInfo with invalid NPC...")
        # await client.test_get_npc_info('invalid_npc')

        logger.info("\nStarting NPC API tests...")
        await client.test_get_npcs()
        
        # 等待响应
        await asyncio.sleep(2)
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await client.disconnect()

# if __name__ == "__main__":
#     asyncio.run(main())



    # test_request.py

async def test_map_town():
    # 启动服务器（如果还没启动）
    server = UnityServer()
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()

    # 等待服务器启动
    await asyncio.sleep(2)
    
    # 创建请求对象
    request = UnityRequest(server.sio, server.current_client_sid)
    
    # 等待客户端连接
    retries = 0
    while not server.current_client_sid and retries < 5:
        logger.info("Waiting for client connection...")
        await asyncio.sleep(1)
        retries += 1

    if not server.current_client_sid:
        logger.error("No client connected")
        return

    # 发送请求并等待响应
    result = await request.get_map_town()
    logger.info(f"Result: {result}")

if __name__ == '__main__':
    try:
        asyncio.run(test_map_town())
    except KeyboardInterrupt:
        logger.info("Test stopped by user")
    except Exception as e:
        logger.error(f"Test error: {str(e)}")