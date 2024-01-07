## 要点

- 每个外设使用前都需要激活该设备的时钟。
- Code、RO、RW占用Flash；RW、ZI占用SRAM。
- EXTIx只能对应一个PAx，若同时设置PAx、PBx，则响应结果不定。
- 若不点开registers选项卡，则keil的调试时间不会动。
- MSP（MCU Support Package）回调机制：手动调用HAL_PPP_Init() -> 回调HAL_PPP_MSPInit()

## STm32启动（内部Flash启动）

reset -> 获取MSP（用户Flash + 0），获取PC（用户Flash + 4，其值为Reset_Handler）-> 调用Reset_Handler（复位中断向量）

-> 启动文件 -> main()

### 启动文件

初始化MSP（初值存放在用户Flash + 0）、PC（用户Flash + 4）；设置堆栈大小；初始化中断向量表；调用初始化函数，如SystemInit；调用__main。



### 启动模式

| BOOT0 | BOOT1 | 启动模式                 |
| ----- | ----- | ------------------------ |
| 0     | 0/1   | 主闪存存储器             |
| 1     | 0     | 系统存储器，用于串口下载 |
| 1     | 1     | 内置SRAM                 |

### GPIO的8种模式

| 模式     | 简称 | 应用                           |
| -------- | ---- | ------------------------------ |
| 输入浮空 |      | 默认状态不定                   |
| 输入上拉 |      | 默认高电平，用于检测输入低电平 |
| 输入下拉 |      | 默认低电平，用于检测输入高电平 |
| 模拟     |      | ADC、DAC                       |
| 开漏输出 |      | 低电平或高阻态。通信、5V       |
| 推挽输出 |      | 驱动设备                       |
| 开漏复用 |      | 片上外设（IIC）                |
| 推挽复用 |      | 片上外设（SPI）                |

### GPIO寄存器

| CRL                    | CRH  | IDR  | ODR  | BSRR        | BRR    | LCKR   |
| ---------------------- | ---- | ---- | ---- | ----------- | ------ | ------ |
| 配置工作模式、输出速度 |      | 输入 | 输出 | 设置ODR的值 | F4没有 | 不常用 |



## 系统时钟配置

配置HSE_VALUE，外部晶振频率，于stm32_hal_conf.h

调用SystemInit()，可选，定义于system_stm32.c

选择时钟源，配置PLL，HAL_RCC_OscConfig()

选择系统时钟源（SYSCLK, HCLK, AHB, APBx），配置总线分频器，HAL_RCC_ClockConfig()

配置扩展外设时钟（可选，H7），HAL_ECCEx_PeriphCLKConfig()

![image-20240101123139109](C:\Users\kieru\AppData\Roaming\Typora\typora-user-images\image-20240101123139109.png)

HAL_RCC_ClockConfig()的LATENCY时延参数，匹配IO速度

| 等待状态        | 适用                    |
| --------------- | ----------------------- |
| FLASH_LATENCY_0 | SYSCLK <= 24MHz         |
| FLASH_LATENCY_1 | 24MHz < SYSCLK <= 48MHz |
| FLASH_LATENCY_2 | 48MHz < SYSCLK <= 72MHz |



## GPIO外中断

->GPIO->AFIO->EXTI（屏蔽，上升沿、下降沿）->NVIC（使能中断、优先级分组、优先级）->中断处理

### NVIC（嵌套向量中断控制器）

优先级、使能。

F103：内中断10个、外中断60个、优先级16个

中断向量表：4B表项

| 寄存器                                       | 位数 | 个数 | 备注 |
| -------------------------------------------- | ---- | ---- | ---- |
| 中断使能寄存器（ISER）                       | 32   | 8    |      |
| 中断失能寄存器（ICER）                       | 32   | 8    |      |
| 应用程序中断及复位控制寄存器（AIRCR）[10: 8] | 32   | 1    |      |
| 中断优先级寄存器（IPR）                      | 8    | 240  |      |

#### 优先级

数值小则优先。

抢占优先级（pre抢占式） > 响应优先级（sub非抢占） > 自然优先级（非抢占）

| 优先级分组 | AIRCR[10: 8] | IPRx[7: 4]分配 | 结果              |
| ---------- | ------------ | -------------- | ----------------- |
| 0          | 111          | None: [7: 4]   | 留0位给抢占优先级 |
| 1          | 110          | [7: 7]: [6: 4] | 留1位给抢占优先级 |
| 2          | 101          | [7: 6]: [5: 4] | 留2位             |
| 3          | 100          | [7: 5]: [4: 4] | 留3位             |
| 4          | 011          | [7: 4]: None   | 留4位             |

一个工程中，一般仅设置一次优先级。

#### NVIC使用

设置中断分组（AIRCR[10: 8]） -> 设置中断优先级（IPRx[7: 4]） -> 使能中断（ISERx）

### EXTI（外部（扩展）中断事件控制器）

中断屏蔽、触发方式。

20个产生事件/中断请求的边沿检测器，F1共20条EXTI线（16（GPIO）+1（PVD输出）+1（RTC闹钟事件）+1（USB、OTG、FS唤醒事件）+1（以太网不一定有））。

中断：NVIC，CPU处理。

事件：不进入NVIC，硬件自动控制。如DMA。

#### AFIO

复用功能IO。调试IO配置、重映射配置、外部中断映射配置。

外部中断配置，AFIO_EXTICR1-4，配置EXTI中断线0-15对应到具体IO口。

使用前要使能AFIO时钟。



### 中断实现

主要配置NVIC、中断服务函数。

GPIO设置输入模式 -> AFIO设置EXTI触发方式（HAL_GPIO_Init自动配置） -> NVIC设置中断分组（在stm32_hal.c中设置一次即可） -> NVIC设置优先级 -> NVIC使能中断 -> 中断服务函数

GPIO时钟，GPIO输入模式，AFIO时钟，EXTIx与PAx对应，设置EXTI屏蔽、触发方式，设置NVIC（优先级分组、优先级、使能中断），中断服务函数。

stm32，EXTI0-4独立中断，EXTI5-9共用中断，EXTI10-15共用中断。

#### NVIC配置

优先级、使能中断请求（IRQ）。

```cpp
HAL_NVIC_SetPriority(EXTI0_IRQn, 2, 0);
HAL_NVIC_EnableIRQ(EXTI0_IRQn);
```

#### 中断服务函数

实现EXTIx_IRQHandler调用公共处理函数（固定）；实现回调函数的用户逻辑。

```cpp
void EXTI0_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0);
    __HAL_GPIO_EXTI_CLEAR_IT(GPIO_PIN_0);
}

void HAL_GPIO_EXTI_Callback(uint16_t pin)
{
	if (pin == GPIO_PIN_0) {
		cb();
	}
}
```





## 存储器映射

32位地址空间，均分为8块，每块512MB

| 块                                 | 功能               |
| ---------------------------------- | ------------------ |
| Block0 (0x0000 0000 - 0x1FFF FFFF) | Code (Flash)       |
| Block1 (0x2000 0000 - 0x3FFF FFFF) | SRAM               |
| Block2 (0x4000 0000 - 0x5FFF FFFF) | 片上外设           |
| Block3                             | FSMC Bank1、2      |
| Block4                             | FSMC Bank3、4      |
| Block5                             | FSMC 寄存器        |
| Block6                             | 保留               |
| Block7                             | Cortex M3 内部外设 |

### Block0 功能划分

| 功能                        | 地址                               |
| --------------------------- | ---------------------------------- |
| Flash，系统存储器           | 0x0000 0000 - 0x0007 FFFF（512KB） |
| 保留                        |                                    |
| 用户 Flash，用户代码        | 0x0800 0000 - 0x0807 FFFF          |
| 保留                        |                                    |
| 系统存储器，出厂 BootLoader |                                    |
| 选项，配置读保护等          |                                    |
| 保留                        |                                    |

### Block1 (SRAM)

SRAM：0x2000 0000 - 0x2000 FFFF（64KB）

其余保留。

存放堆栈等。

### Block2 (外设)

| 功能 | 地址范围                  |
| ---- | ------------------------- |
| APB1 | 0x4000 0000 - 0x4000 77FF |
| 保留 |                           |
| APB2 | 0x4001 0000 - 0x4000 3FFF |
| 保留 |                           |
| AHB  | 0x4001 8000 - 0x4002 33FF |
| 保留 |                           |



## 寄存器映射

GPIOx 在 AHB2，其余看手册。



## USART/UART 通信

### 中断回调

![image-20240103120239979](C:\Users\kieru\AppData\Roaming\Typora\typora-user-images\image-20240103120239979.png)

### 时序配置

启动位，1位低电平；有效数据位，小端序；校验位，不需要；停止位，1位高电平。

### 异步通信配置

串口工作参数配置，HAL_UART_Init()

串口初始化，HAL_UART_MspInit()，配置GPIO、NVIC、CLOCK

开启串口异步接收中断，HAL_UART_Receive_IT()

中断NVIC配置

传送，HAL_UART_Transmit()

## IWDG独立看门狗

能产生系统复位信号的独立计数器（由独立的RC振荡器提供）。

自减到0时产生复位信号，在停止和待机模式中仍能工作。喂狗。

外界电磁干扰、硬件异常（内中断）处理。

高稳定性产品，时间精度低，保命手段。

```cpp
HAL_IWDG_Init();
HAL_IWDG_Refresh();	// 喂狗
```



## WWDG窗口看门狗

#### 特性

能产生系统**复位信号**和**提前唤醒中断**的计数器。

从0x40自减到0x3f时复位（即T6位跳变到0时复位）；

计时器的值大于W[6: 0]时喂狗则复位；

提前唤醒中断（EWI），当值为0x40时可产生重载值，防止复位。

#### 作用

监测单片机程序运行时效是否精准，检测软件异常；精准检测程序运行时间。

## 定时器

![image-20240104102700518](C:\Users\kieru\AppData\Roaming\Typora\typora-user-images\image-20240104102700518.png)

![image-20240104171716708](C:\Users\kieru\AppData\Roaming\Typora\typora-user-images\image-20240104171716708.png)

### SysTick

时钟源（HCLK）->分频（1/, 8/）->VAL（24位自减计数器），等于0时重载VAL=LOAD、COUNTFLAG=1。
