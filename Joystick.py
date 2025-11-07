#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/SpiderPi/')
import os
import time
import json
import pygame
import asyncio
import threading
import websockets
import HiwonderSDK.Board as Board
import Functions.kinematics as kinematics
import HiwonderSDK.ActionGroupControl as AGC
import Functions.Robot_dance as dance

#ps2手柄控制动作, 已以system方式自启动，无需再开启

key_map = {"PSB_CROSS":2, "PSB_CIRCLE":1, "PSB_SQUARE":3, "PSB_TRIANGLE":0,
        "PSB_L1": 4, "PSB_R1":5, "PSB_L2":6, "PSB_R2":7,
        "PSB_SELECT":8, "PSB_START":9, "PSB_L3":10, "PSB_R3":11};
action_map = ["CROSS", "CIRCLE", "", "SQUARE", "TRIANGLE", "L1", "R1", "L2", "R2", "SELECT", "START", "", "L3", "R3"]


ik = kinematics.IK()
ik.stand(ik.initial_pos) # 立正
servo21,servo22,servo23,servo24,servo25 = 500,705,90,330,500 
Board.setBusServoPulse(21, servo21, 1000)
Board.setBusServoPulse(22, servo22, 1000)
Board.setBusServoPulse(23, servo23, 1000)
Board.setBusServoPulse(24, servo24, 1000)
Board.setBusServoPulse(25, servo25, 1000)
time.sleep(1)
                    
def setBuzzer(s):
    Board.setBuzzer(1)  # 打开
    time.sleep(s)  # 延时
    Board.setBuzzer(0)  #关闭

def joystick_init():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.display.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        js=pygame.joystick.Joystick(0)
        js.init()
        jsName = js.get_name()
        print("Name of the joystick:", jsName)
        jsAxes=js.get_numaxes()
        print("Number of axif:",jsAxes)
        jsButtons=js.get_numbuttons()
        print("Number of buttons:", jsButtons);
        jsBall=js.get_numballs()
        print("Numbe of balls:", jsBall)
        jsHat= js.get_numhats()
        print("Number of hats:", jsHat)
  
  
async def call_rpc(method, params=None):
    websocket = None
    try:
        websocket = await websockets.connect('ws://192.168.149.1:7788/up')
        call = dict(jsonrpc='2.0', method=method)
        if params is not None:
            call['params'] = params
        await websocket.send(json.dumps(call))
        await websocket.close()
    except Exception as e:
        if websocket is not None:
            await websocket.close()

async def run_action_set(action_set_name, repeat):
    await call_rpc('run_action_set', [action_set_name, repeat])

async def stop(action_set_name=None):
    await call_rpc('stop')
    if action_set_name is not None:
        await run_action_set(action_set_name, 1)  


async def kinematics_control(name):
    await call_rpc('kinematics_control', [name])
     
  
mode = 'move'
stand_ti = time.time()
stand_st = False
th = None
last_status = ''
connected = False
while True:
    if os.path.exists("/dev/input/js0") is True:
        if connected is False:
            joystick_init()
            jscount =  pygame.joystick.get_count()
            if jscount > 0:
                try:
                    js=pygame.joystick.Joystick(0)
                    js.init()
                    connected = True
                except Exception as e:
                    print(e)
            else:
                pygame.joystick.quit()
    else:
        if connected is True:
            connected = False
            js.quit()
            pygame.joystick.quit()
    if connected is True:
        pygame.event.pump()     
        actName = None
        times = 1
        try:
            if js.get_button(key_map["PSB_SELECT"]):
                time.sleep(0.08)
                if js.get_button(key_map["PSB_SELECT"]):
                    if mode == 'move':
                        setBuzzer(0.1)
                        time.sleep(0.1)
                        setBuzzer(0.1)
                        mode = 'arm'
                    else:
                        setBuzzer(0.1)
                        mode = 'move'
                    time.sleep(1)
                
            if mode == 'move':
                if js.get_button(key_map["PSB_R1"]):
                    asyncio.run(kinematics_control('dance'))
                    dance.dance()
                if js.get_button(key_map["PSB_R2"]):
                    asyncio.run(kinematics_control('turn_right'))
                    ik.turn_right(ik.initial_pos, 2, 20, 100, 1)  # 原地右转30读
                    stand_st = True
                    stand_ti = time.time()
                if js.get_button(key_map["PSB_L2"]):
                    asyncio.run(kinematics_control('turn_left'))
                    ik.turn_left(ik.initial_pos, 2, 20, 100, 1)  # 原地左转30度
                    stand_st = True
                    stand_ti = time.time()
                if js.get_button(key_map["PSB_SQUARE"]): #正方形
                    actName = 'wave'
                if js.get_button(key_map["PSB_CIRCLE"]): #圈
                    actName = 'kick'
                if js.get_button(key_map["PSB_TRIANGLE"]): #三角
                    actName = 'attack'
                if js.get_button(key_map["PSB_CROSS"]): #叉
                    actName = 'twist'
                if js.get_button(key_map["PSB_START"]):
                    AGC.stopAction()
                    time.sleep(0.5)
                    ik.stand(ik.initial_pos) # 立正      
                    
                lx = js.get_axis(0)
                ly = js.get_axis(1)
                if lx < -0.5:
                    asyncio.run(kinematics_control('left_move'))
                    ik.left_move(ik.initial_pos, 2, 50, 80, 1)  # 左移50mm
                    stand_ti = time.time()
                    stand_st = True
                elif lx > 0.5:
                    asyncio.run(kinematics_control('right_move'))
                    ik.right_move(ik.initial_pos, 2, 50, 80, 1)  # 右移50mm
                    stand_ti = time.time()
                    stand_st = True
                if ly < -0.5:
                    asyncio.run(kinematics_control('go_forward'))
                    ik.go_forward(ik.initial_pos, 2, 50, 80, 1)  # 朝前直走50mm
                    stand_ti = time.time()
                    stand_st = True
                elif ly > 0.5:
                    asyncio.run(kinematics_control('back'))
                    ik.back(ik.initial_pos, 2, 50, 80, 1)  # 朝后直走50mm
                    stand_ti = time.time()
                    stand_st = True
                
                if stand_st and time.time()-stand_ti >= 0.1:
                    stand_st = False
                    stand_ti = time.time()
                    asyncio.run(kinematics_control('stand'))
                    ik.stand(ik.initial_pos, 500) # 立正   
                    
                if th is not None:
                    if actName is not None:
                        if not th.is_alive():
                            asyncio.run(run_action_set(actName, 1))
                            th = threading.Thread(target=AGC.runActionGroup, args=(actName, times), daemon=True)
                            th.start()
                else:
                    asyncio.run(run_action_set(actName, 1))
                    th = threading.Thread(target=AGC.runActionGroup, args=(actName, times), daemon=True)
                    th.start()
                    
            elif mode == 'arm':
                if js.get_button(key_map["PSB_R2"]):
                    servo25 -= 5
                    servo25 = 200 if servo25 < 200 else servo25
                    Board.setBusServoPulse(25, servo25, 30)
                    time.sleep(0.03)
                if js.get_button(key_map["PSB_L2"]):
                    servo25 += 5
                    servo25 = 700 if servo25 > 700 else servo25
                    Board.setBusServoPulse(25, servo25, 30)
                    time.sleep(0.03)
                if js.get_button(key_map["PSB_SQUARE"]): #正方形
                    servo23 -= 5
                    Board.setBusServoPulse(23, servo23, 30)
                    time.sleep(0.03)
                if js.get_button(key_map["PSB_TRIANGLE"]): #三角
                    servo23 += 5
                    Board.setBusServoPulse(23, servo23, 30)
                    time.sleep(0.03)
                if js.get_button(key_map["PSB_CIRCLE"]): #圈
                    servo24 += 5
                    Board.setBusServoPulse(24, servo24, 30)
                    time.sleep(0.03)
                if js.get_button(key_map["PSB_CROSS"]): #叉
                    servo24 -= 5
                    Board.setBusServoPulse(24, servo24, 30)
                    time.sleep(0.03)
                if js.get_button(key_map["PSB_START"]):
                    servo21,servo22,servo23,servo24,servo25 = 500,705,90,330,500
                    Board.setBusServoPulse(21, servo21, 1000)
                    Board.setBusServoPulse(22, servo22, 1000)
                    Board.setBusServoPulse(23, servo23, 1000)
                    Board.setBusServoPulse(24, servo24, 1000)
                    Board.setBusServoPulse(25, servo25, 1000)
                    time.sleep(1)
                    
                lx = js.get_axis(0)
                ly = js.get_axis(1)
                if lx < -0.5:
                    servo21 += 5
                    Board.setBusServoPulse(21, servo21, 30)
                    time.sleep(0.03)
                elif lx > 0.5:             
                    servo21 -= 5
                    Board.setBusServoPulse(21, servo21, 30)
                    time.sleep(0.03)
                if ly < -0.5:
                    servo22 += 5
                    Board.setBusServoPulse(22, servo22, 30)
                    time.sleep(0.03)
                elif ly > 0.5:
                    servo22 -= 5
                    Board.setBusServoPulse(22, servo22, 30)
                    time.sleep(0.03)
                    
        except Exception as e:
            print(e)
            connected = False          
    time.sleep(0.01)
