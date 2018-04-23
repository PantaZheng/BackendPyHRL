# HC-SR04超声波传感器与树莓派的远程控制实验

## HC-SR04

### 简介

* 超声波距离传感器可以使用超声波来测量源与目标之间的距离。超声波对于人耳来说是无法听见的，它在短距离内的测量数据相对精确并且不会引起干扰。
* HC-SR04是一种常用的非接触式地距离测量模块，适用于2cm至400cm的距离。它使用超声波（也是蝙蝠和海豚所使用的）的高精度和稳定的读数来测量距离。它由超声波发射器、接收器和控制电路组成。发射器发射短波超声波信号并由接收器接收目标反射的信号。通过计算超声波信号的发送和接收之间的时间差，使用声速和“速度=距离/时间”公式，可以很容易地计算源和目标之间的距离。
* HC-SR04 ![HC-SR04](https://raw.githubusercontent.com/RaphaelZheng/BackendPyHRL/master/resource/HC-SR04-Ultrasonic-Sensor.jpg)

* HC-SR04超声波距离传感器模块有四个引脚：
    * VCC - 5V，输入功率
    * TRIG - 触发器输入
    * ECHO - 回声输出
    * GND - 接地

### 电气参数

电气参数|HC-SR04超声波模块
-|-
工作电压|DC 5V
工作电流|15mA
工作频率|40HZ
最远射程|4m
最近射程|2cm
测量角度|15度
输入触发信号|\>10&mu;的TTL脉冲
输出回响信号|输出TTL电平信号，与射程成比例
规格尺寸|45\*20\*15mm

### 工作原理 

* 工作原理图 ![模块操作](https://raw.githubusercontent.com/RaphaelZheng/BackendPyHRL/master/resource/Ultrasonic-Module-Operation.jpg)

1. 采用IO口对TRIG提供触发信号，给至少10us持续时间的高电平信号；
1. 模块自动发送8个40khz的超声波信号
1. 如果模块前方存在障碍物，就会反射这些超声波
1. 如果信号返回， 则模块的ECHO端输出将在发送和接收信号之间的时间内为高电平。根据目标障碍物到源传感器的距离，脉冲宽度范围为150&mu;s到25ms之间，如果没有障碍物，脉冲宽度约为38ms。

* 树莓派与HC-SR04 连接示意图 ![连接图](https://raw.githubusercontent.com/RaphaelZheng/BackendPyHRL/master/resource/Interfacing-Raspberry-Pi-with-HC-SR04.jpg)

### 距离计算

* 超声波脉冲所用时间其实就是来回超声波信号的传播时间，所以我们只需要利用一半的时间就能计算距离。
* 距离公式实际为：s=v*t/2
    * 超声波声速为： 343m/s或34300cm/s
    * 最终距离公式：s=17150*t (cm)

---

## 树莓派相关

### 树莓派引脚模式-编号对应表

![对应表](https://raw.githubusercontent.com/RaphaelZheng/BackendPyHRL/master/resource/20161230104544903.png)

### 实验样机图片

![样机](https://raw.githubusercontent.com/RaphaelZheng/BackendPyHRL/master/resource/树莓派超声波实验样机.jpg)



